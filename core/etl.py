"""
Módulo de Extração, Transformação e Carga (ETL) para dados financeiros do Sponte.

Este módulo aplica regras de higienização monetária, normalização de datas,
identificação de bolsistas via valor pago zero e classificação de contratos.
"""

import pandas as pd
import numpy as np
import re

from core.config import UNIDADES_VALIDAS

def clean_currency(val) -> float:
    """Converte strings de moeda em formato brasileiro para float nativo."""
    if pd.isna(val) or val is None or val == '': return 0.0
    if isinstance(val, (int, float)): return float(val)
    val_str = str(val).replace('R$', '').replace(' ', '').strip()
    if ',' in val_str and '.' in val_str: val_str = val_str.replace('.', '').replace(',', '.')
    elif ',' in val_str: val_str = val_str.replace(',', '.')
    try: return float(val_str)
    except: return 0.0

def find_column(dataframe: pd.DataFrame, patterns: list):
    """Mapeia dinamicamente colunas baseadas em padrões de texto esperados."""
    for pat in patterns:
        for col in dataframe.columns:
            col_str = str(col).lower()
            if pat == col_str or (len(pat) > 3 and pat in col_str):
                return col
    return None

def process_contas_receber(filepath_or_buffer, unidade: str, ano_referencia: int) -> pd.DataFrame:
    df = pd.read_excel(filepath_or_buffer, header=3)
    if sum('unnamed' in str(c).lower() for c in df.columns) > len(df.columns) / 2:
        df = pd.read_excel(filepath_or_buffer)

    # 1. Padronização de Nomes Brutos (Conforme exportação exata do Sponte)
    colunas_exigidas = [
        'NumeroParcela', 'Sacado', 'NumeroMatricula', 'ValorComDesconto', 
        'DataVencimento', 'DataPagamento', 'ValorComJuros', 'ValorPago', 
        'Bolsa', 'FormaCobranca', 'Situacao', 'SituacaoAluno', 'Turma', 
        'Curso', 'NomeAtendente', 'DataInicio', 'DataTermino', 'NomeOperadoraCartao'
    ]
    
    # Mapeamento para garantir a captura das colunas corretas ignorando case/espaços
    cols_map = {str(c).replace(' ', '').lower(): c for c in df.columns}
    rename_dict = {}
    for col_exigida in colunas_exigidas:
        col_lower = col_exigida.lower()
        if col_lower in cols_map:
            rename_dict[cols_map[col_lower]] = col_exigida
            
    df.rename(columns=rename_dict, inplace=True)
    
    # Mantém apenas as colunas exigidas que foram encontradas
    colunas_presentes = [c for c in colunas_exigidas if c in df.columns]
    df = df[colunas_presentes].copy()

    # 2. Higienização de Tipos
    for col in ['ValorComDesconto', 'ValorComJuros', 'ValorPago']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('R$', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0.0)

    for col in ['DataVencimento', 'DataPagamento', 'DataInicio', 'DataTermino']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
    # 3. Regra de Bolsista 100%
    if 'Situacao' in df.columns and 'ValorPago' in df.columns and 'Bolsa' in df.columns:
        df['Situacao'] = df['Situacao'].astype(str).str.strip().str.title()
        is_bolsista = (df['Situacao'] == 'Quitada') & (df['ValorPago'] == 0.0)
        df.loc[is_bolsista, 'Bolsa'] = 'Bolsista'

    # 4. Mapeamento de Cursos
    if 'Turma' in df.columns:
        df['Turma'] = df['Turma'].astype(str)
        condicoes_curso = [
            df['Turma'].str.contains('Español', case=False, na=False),
            df['Turma'].str.contains('English', case=False, na=False),
            df['Turma'].str.contains('Kids', case=False, na=False),
            df['Turma'].str.contains('Preteen', case=False, na=False),
            df['Turma'].str.contains('TEACHER', case=False, na=False),
            df['Turma'].str.contains('baby', case=False, na=False)
        ]
        escolhas_curso = [
            'Español', 'English Course', 'Kids Course', 
            'Preteen Course', "TEACHER'S COURSE", 'Baby Course'
        ]
        df['Curso'] = np.select(condicoes_curso, escolhas_curso, default=df.get('Curso', 'S/I'))

    # 5. Classificação de Contratos e Semestralidade
    if 'DataInicio' in df.columns and 'Sacado' in df.columns:
        df['mes_inicio'] = df['DataInicio'].dt.month
        df['total_parcelas'] = df.groupby('Sacado')['Sacado'].transform('count')
        
        def definir_contrato(row):
            mes = row['mes_inicio']
            tot = row['total_parcelas']
            
            if pd.isna(mes): return 'Semestral'
            
            regras = {
                11: 8, 12: 7, 1: 6, 2: 5, 3: 4, 4: 3
            }
            
            if mes in regras:
                return 'Anual' if tot >= regras[mes] else 'Semestral'
            elif 5 <= mes <= 10:
                return 'Semestral'
            return 'Semestral'
            
        df['TipoContrato'] = df.apply(definir_contrato, axis=1)
        
        # Atribuição do Semestre
        limite_s1 = pd.to_datetime(f"{ano_referencia}-06-30")
        
        def definir_semestre(row):
            venc = row['DataVencimento']
            mes_ini = row['mes_inicio']
            
            if row['TipoContrato'] == 'Anual':
                if pd.notna(venc) and venc <= limite_s1:
                    return '1º Semestre'
                return '2º Semestre'
            else:
                if 5 <= mes_ini <= 10:
                    return '2º Semestre'
                return '1º Semestre'
                
        df['SemestreReferencia'] = df.apply(definir_semestre, axis=1)
        df.drop(columns=['mes_inicio', 'total_parcelas'], inplace=True)

    # =====================================================================
    # 6. EXPURGO BASEADO NA NOMENCLATURA DA TURMA
    # =====================================================================
    if 'Turma' in df.columns:
        # Extrai estritamente um bloco de 4 dígitos (ex: 2024, 2025, 2026) da string
        ano_turma = df['Turma'].astype(str).str.extract(r'(20\d{2})')[0]
        
        # Converte para numérico. Se a turma não tiver ano na string (ex: "English Kids"), 
        # assume o ano_referencia provisoriamente para não deletar a linha por engano.
        ano_turma = pd.to_numeric(ano_turma, errors='coerce').fillna(ano_referencia)
        
        # Sobrescreve o DataFrame mantendo APENAS o qu
        # e bate com o ano do extrator
        df = df[ano_turma == ano_referencia].copy()
    df['unidade'] = unidade
    return df