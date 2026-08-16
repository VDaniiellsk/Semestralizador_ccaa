import pandas as pd
import numpy as np
import re

UNIDADES_VALIDAS = [
    "Paralela",
    "Matatu de Brotas",
    "Iguatemi",
    "Simões Filho",
    "Periperi",
    "Cajazeiras"
]

def clean_currency(val):
    if pd.isna(val) or val is None or val == '': return 0.0
    if isinstance(val, (int, float)): return float(val)
    val_str = str(val).replace('R$', '').replace(' ', '').strip()
    if ',' in val_str and '.' in val_str: val_str = val_str.replace('.', '').replace(',', '.')
    elif ',' in val_str: val_str = val_str.replace(',', '.')
    try: return float(val_str)
    except: return 0.0

def find_column(dataframe: pd.DataFrame, patterns: list):
    for pat in patterns:
        for col in dataframe.columns:
            col_str = str(col).lower()
            if pat == col_str or (len(pat) > 3 and pat in col_str):
                return col
    return None

def process_contas_receber(filepath_or_buffer, unidade: str, ano_referencia: int) -> pd.DataFrame:
    try:
        df = pd.read_excel(filepath_or_buffer, header=3)
        if sum('unnamed' in str(c).lower() for c in df.columns) > len(df.columns) / 2:
            df = pd.read_excel(filepath_or_buffer)
    except:
        df = pd.read_excel(filepath_or_buffer)

    df.columns = df.columns.astype(str).str.strip().str.lower()
    df = df.loc[:, ~df.columns.duplicated(keep='first')]

    # 1. Identificação Primária
    mapa_colunas = {
        'sacado': find_column(df, ['sacado', 'nome do sacado', 'aluno', 'cliente']),
        'numero_matricula': find_column(df, ['matrícula', 'matricula', 'código', 'codigo', 'ra']),
        'situacao_aluno': find_column(df, ['situação do aluno', 'situacao do aluno', 'situação aluno', 'situacao aluno']),
        'data_inicio': find_column(df, ['data início', 'data inicio', 'dt. inicio', 'dt inicio', 'início', 'inicio']),
        'data_termino': find_column(df, ['data término', 'data termino', 'dt. termino', 'dt termino', 'término', 'termino', 'fim']),
        'bolsa': find_column(df, ['bolsa', 'convênio', 'convenio', 'desconto', 'desc. bolsa']),
        'data_vencimento': find_column(df, ['vencimento', 'dt. venc', 'dt venc', 'venc']),
        'data_pagamento': find_column(df, ['data pagamento', 'dt. pag', 'pagamento', 'pagto', 'liquida']),
        'valor': find_column(df, ['valor título', 'valor titulo', 'vlr nominal', 'nominal', 'valor']),
        'valor_com_desconto': find_column(df, ['valor líquido', 'valor liquido', 'com desconto', 'líquido', 'liquido']),
        'valor_pago': find_column(df, ['valor pago', 'valor recebido', 'recebido', 'pago']),
        'situacao': find_column(df, ['situação da parcela', 'situacao da parcela', 'situação', 'situacao', 'status']),
        'turma': find_column(df, ['turma']),
        'curso': find_column(df, ['curso']),
        'numero_parcela': find_column(df, ['nº parcela', 'parcela', 'parc'])
    }

    colunas_vitais_padronizadas = list(mapa_colunas.keys()) + ['unidade']

    rename_dict = {source: target for target, source in mapa_colunas.items() if source and source in df.columns and source != target}
    df.rename(columns=rename_dict, inplace=True)
    df = df.loc[:, ~df.columns.duplicated(keep='first')]
    df['unidade'] = unidade

    # 2. Expurgo do Lixo Desnecessário
    lixo = [
        'telefone', 'celular', 'numerorecibo', 'numeroboleto', 'planocontaid', 'nomeatendente', 'complemento', 
        'cidadealuno', 'cpfresponsavel', 'nomeresponsavel', 'enderecoresponsavel', 'cepresponsavel', 
        'bairroresponsavel', 'complementoresponsavel', 'celularresponsavel', 'emailresponsavel', 
        'rgresponsavel', 'foneresponsavel', 'fonecomercialresponsavel', 'estadoresponsavel', 
        'parentescoresponsavel', 'datanascimentoresponsavel', 'cnabnome', 'banco', 'conta', 'carteira', 
        'cnabdescricao', 'layoutcobranca', 'numerocheque', 'titularcheque', 'bancocheque', 'agenciacheque', 
        'contacheque', 'bomparacheque', 'status'
    ]
    
    cols_to_drop = [
        c for c in df.columns 
        if c not in colunas_vitais_padronizadas 
        and (str(c).replace(' ', '').lower() in lixo or str(c).lower() in lixo)
    ]
    df.drop(columns=cols_to_drop, errors='ignore', inplace=True)

    # 3. Tratamento Monetário
    for c in ['valor', 'valor_com_desconto', 'valor_pago']:
        if c in df.columns:
            serie = df[c].iloc[:, 0] if isinstance(df[c], pd.DataFrame) else df[c]
            df[c] = serie.apply(clean_currency)
        else:
            df[c] = 0.0

    df['valor_com_desconto'] = np.where(df['valor_com_desconto'] > 0, df['valor_com_desconto'], df['valor'])
    df['valor_com_juros'] = df['valor_com_desconto']

    if 'bolsa' not in df.columns: 
        df['bolsa'] = 'S/I'
    else: 
        serie_b = df['bolsa'].iloc[:, 0] if isinstance(df['bolsa'], pd.DataFrame) else df['bolsa']
        df['bolsa'] = serie_b.fillna('S/I').astype(str).str.strip().replace(['nan', 'None', '', '0', '0.0', '-'], 'S/I')

    # 4. Tratamento Blindado da Situação (Padroniza maiúsculas/minúsculas)
    if 'situacao' in df.columns:
        serie_sit = df['situacao'].iloc[:, 0] if isinstance(df['situacao'], pd.DataFrame) else df['situacao']
        df['situacao'] = serie_sit.fillna('Pendente').astype(str).str.strip().str.title()
    else:
        df['situacao'] = 'Pendente'

    # Expurgo de Inativos Pendentes
    if 'situacao_aluno' in df.columns:
        is_inativo_pendente = (df['situacao_aluno'].astype(str).str.lower().str.contains('inativo', na=False)) & (df['situacao'].str.lower() == 'pendente')
        df = df[~is_inativo_pendente]

    # 5. Tratamento de Datas
    for c in ['data_inicio', 'data_termino', 'data_vencimento', 'data_pagamento']:
        if c in df.columns:
            serie = df[c].iloc[:, 0] if isinstance(df[c], pd.DataFrame) else df[c]
            df[c] = pd.to_datetime(serie, dayfirst=True, errors='coerce')

    # 6. Ancoragem Estrita pelo Ano
    if 'data_termino' in df.columns:
        df = df[df['data_termino'].dt.year == ano_referencia].copy()
    else:
        df = df[df['data_vencimento'].dt.year == ano_referencia].copy()

    df['ano_ref'] = ano_referencia

    # 7. Regra de Negócio do Semestre Comercial
    dt_inicio = pd.Series([pd.NaT] * len(df), index=df.index)
    if 'data_inicio' in df.columns:
        dt_inicio = dt_inicio.fillna(df['data_inicio'])
    if 'data_vencimento' in df.columns:
        dt_inicio = dt_inicio.fillna(df['data_vencimento'])
        
    mes_inicio = dt_inicio.dt.month.fillna(1)
    
    if 'data_vencimento' in df.columns:
        mes_venc = df['data_vencimento'].dt.month.fillna(1)
        ano_venc = df['data_vencimento'].dt.year.fillna(ano_referencia)
    else:
        mes_venc = pd.Series([1] * len(df), index=df.index)
        ano_venc = pd.Series([ano_referencia] * len(df), index=df.index)

    is_capta_s2 = (mes_inicio >= 5) & (mes_inicio <= 8)
    is_venc_s2 = (mes_venc >= 7) & (ano_venc >= ano_referencia)

    df['semestre_num'] = np.where(is_capta_s2 | is_venc_s2, 2, 1)
    df['semestre_ref'] = df['semestre_num'].astype(str) + "/" + str(ano_referencia)

    # 8. Limpeza Final
    subset_dedup = [c for c in ['unidade', 'sacado', 'data_vencimento', 'valor', 'numero_parcela'] if c in df.columns]
    if subset_dedup:
        df = df.drop_duplicates(subset=subset_dedup, keep='first')

    return df