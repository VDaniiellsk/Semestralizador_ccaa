"""Transforma o relatório de contas a receber em registros prontos para análise.

Normaliza valores e datas, deduz curso e estágio, aplica o recorte do ano e
valida a carga antes de permitir sua publicação."""
from decimal import Decimal,InvalidOperation,ROUND_HALF_UP
from datetime import date,datetime
import re
import unicodedata
import pandas as pd
from core.database import REQUIRED,validar_lote
OPTIONAL=('DataPagamento','ValorComJuros','Bolsa','FormaCobranca','SituacaoAluno',
          'NomeAtendente','DataTermino','NomeOperadoraCartao','Estagio')

def clean_currency(value):
    """Interpreta valores monetários do relatório com arredondamento para centavos."""
    if value is None or pd.isna(value) or str(value).strip() == '':
        raise ValueError('Valor monetário ausente.')
    text = str(value).replace('R$', '').replace(' ', '').strip()
    if ',' in text:
        text = text.replace('.', '').replace(',', '.')
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValueError('Valor monetário inválido.') from None
    if not amount.is_finite() or amount < 0:
        raise ValueError('Valor monetário deve ser válido e não negativo.')
    return float(amount.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP))

def _date(value):
    """Converte datas para o formato usado nesta camada e rejeita valores inválidos."""
    if value is None or pd.isna(value) or str(value).strip() == '':
        return pd.NaT
    if isinstance(value, (datetime, date)):
        return pd.Timestamp(value)
    text = str(value).strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}', text):
        return pd.Timestamp(text)
    return pd.to_datetime(text, dayfirst=True, errors='raise')

from core.catalogo import STAGE_COURSES, deduzir_estagio, normalizar_curso, classificar


def tratar_contas_receber(df,unidade,ano_referencia):
    """Trata um DataFrame do ERP, aplica as regras de classificação e valida o resultado."""
    canonical=REQUIRED+OPTIONAL
    mapping={c.lower():c for c in canonical}
    df=df.rename(columns={c:mapping.get(str(c).replace(' ','').lower(),c) for c in df.columns})
    if df.columns.duplicated().any():raise ValueError('A exportação contém colunas repetidas.')
    missing=set(REQUIRED)-{'unidade','SemestreReferencia','TipoContrato','Curso'}-set(df.columns)
    if missing:raise ValueError('Faltam campos na exportação: '+', '.join(sorted(missing)))
    df=df[[c for c in canonical if c in df.columns]].copy().reset_index(drop=True)
    for col in ('ValorComDesconto','ValorPago','ValorComJuros'):
        if col in df:
            df[col]=df[col].map(lambda v:None if col=='ValorComJuros' and (pd.isna(v) or str(v).strip()=='') else clean_currency(v))
    for col in ('DataInicio','DataVencimento','DataPagamento','DataTermino'):
        if col in df:df[col]=pd.to_datetime(df[col].map(_date))
    df['Situacao']=df['Situacao'].map(lambda v:str(v).strip().title() if pd.notna(v) else v)
    if 'Bolsa' not in df:df['Bolsa']=None
    df['Bolsa']=df['Bolsa'].astype(object)
    sem_bolsa=df['Bolsa'].isna() | df['Bolsa'].astype(str).str.strip().eq('')
    df.loc[sem_bolsa & (df['Situacao']=='Quitada') & (df['ValorPago']==0),'Bolsa']='Bolsista'
    classificar(df)
    turma=df['Turma'].fillna('').astype(str)
    # Classificação analítica herdada; não identifica contratos individuais.
    if 'TipoContrato' not in df:df['TipoContrato']=None
    missing_kind=df['TipoContrato'].isna() | df['TipoContrato'].astype(str).str.strip().eq('')
    totals=df.groupby('NumeroMatricula')['NumeroParcela'].transform('size')
    limits={11:8,12:7,1:6,2:5,3:4,4:3}
    kinds=[]
    for index,row in df.iterrows():
        value=row['TipoContrato']
        if missing_kind.loc[index]:
            if pd.isna(row['DataInicio']):value='Não informado'
            else:
                month=row['DataInicio'].month
                value='Anual' if month in limits and totals.loc[index]>=limits[month] else 'Semestral'
        kind=str(value).strip().title()
        kinds.append('Não informado' if kind.casefold()=='não informado' else kind)
    df['TipoContrato']=kinds
    limite=pd.Timestamp(year=int(ano_referencia),month=6,day=30)
    def semestre(row):
        """Aplica a regra temporal existente para classificar a parcela no semestre de referência."""
        if row['TipoContrato']=='Anual':
            return '1º Semestre' if row['DataVencimento']<=limite else '2º Semestre'
        if pd.isna(row['DataInicio']):return 'Não informado'
        return '2º Semestre' if 5<=row['DataInicio'].month<=10 else '1º Semestre'
    df['SemestreReferencia']=[semestre(row) for _,row in df.iterrows()]
    df['unidade']=unidade
    validar_lote(df,unidade)
    ano_turma=pd.to_numeric(turma.str.extract(r'(20\d{2})')[0],errors='coerce').fillna(ano_referencia)
    from core.descontos import estimar_descontos
    df=estimar_descontos(df.loc[ano_turma==ano_referencia].copy(),ano_referencia)
    validar_lote(df,unidade)
    return df

def process_contas_receber(filepath_or_buffer,unidade,ano_referencia):
    """Lê o arquivo exportado, encontra o cabeçalho e encaminha os registros ao tratamento."""
    df=pd.read_excel(filepath_or_buffer,header=3)
    names={str(c).replace(' ','').lower() for c in df.columns}
    if not {'numeroparcela','numeromatricula','turma'}<=names:
        if hasattr(filepath_or_buffer,'seek'):filepath_or_buffer.seek(0)
        df=pd.read_excel(filepath_or_buffer,header=0)
    return tratar_contas_receber(df,unidade,ano_referencia)
