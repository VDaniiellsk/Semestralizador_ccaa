"""Compara parcelas com a tabela privada de preços para estimar descontos.

O resultado é uma hipótese financeira, não uma confirmação de contrato ou
convênio. Os dados originais do ERP permanecem intactos."""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json
import re
import unicodedata
import pandas as pd

CAMPOS=('DescontoEstimado','PacoteEstimado','ParcelamentoEstimado','ResultadoEstimativa','FonteEstimativa')
CONFIG_DIR=Path(__file__).resolve().parents[1]/'config'
CENTAVO=Decimal('0.01')

def _normalizar(value):
    """Padroniza o texto para comparação, sem alterar o dado original exibido."""
    text=unicodedata.normalize('NFKD',str(value))
    return ''.join(c for c in text if not unicodedata.combining(c)).casefold().strip()

def carregar_precos(ano):
    """Lê a referência privada de preços do ano; indisponibilidade não deve inventar uma estimativa."""
    path=CONFIG_DIR/f'precos_{ano}.json'
    if not path.exists():return None
    referencia=json.loads(path.read_text(encoding='utf-8'))
    if referencia.get('ano')!=int(ano) or not isinstance(referencia.get('regioes'),dict):
        raise ValueError('Referência de preços inválida.')
    return referencia

def _estagio(value):
    """Chave de preço: preserva níveis combinados e diferencia VIP."""
    text=_normalizar(value)
    if 'vip' in text:return 'VIP'
    if re.search(r'\bteacher',text):return 'TEACHERS'
    if re.search(r'\benglish',text):
        if re.search(r'\bc\s*1\s*-\s*2\b',text):return 'English C 1-2'
        m=re.search(r'english\s*(?:[at]\s*)?(?:i\s*)?(\d{1,2})(?!\d)',text)
        if m and 1<=int(m[1])<=11:return f'English {int(m[1])}'
    for family,maximum in [('Español',9),('Kids',8),('Baby',6),('Preteen',2)]:
        token=_normalizar(family)
        m=re.search(token+r'\s*(\d+)(?!\d)',text)
        if m and 1<=int(m[1])<=maximum:return f'{family} {int(m[1])}'
    return None

def _preco(estagio,precos):
    """Consulta o preço aplicável ao estágio e à região da unidade."""
    if estagio in ('VIP','TEACHERS','English C 1-2'):return precos.get(estagio)
    family,level=estagio.rsplit(' ',1);level=int(level)
    if family=='English':key='English 1-3' if level<=3 else 'English 4-6' if level<=6 else 'English 7-9' if level<=9 else 'English 10-11'
    else:key=family
    return precos.get(key)

def _pacotes(estagios,regiao):
    """Gera os pacotes candidatos para comparação, incluindo combinações anuais previstas."""
    precos=regiao['precos'];chaves=[]
    for family,maximum in [('English',11),('Español',9),('Kids',8),('Baby',6),('Preteen',2)]:
        chaves += [f'{family} {i}' for i in range(1,maximum+1)]
    chaves += ['English C 1-2','TEACHERS']
    if 'VIP' in precos:chaves.append('VIP')
    # Um estágio: hipótese semestral. Dois estágios: hipótese anual.
    if len(estagios)==1:
        e=next(iter(estagios));price=_preco(e,precos)
        if price is not None:
            yield 'Semestral', (e,), Decimal(price), regiao.get('parcelas_vip',[]) if e=='VIP' else regiao['parcelas_semestrais']
    pairs=[]
    for family,maximum in [('English',11),('Español',9),('Kids',8),('Baby',6),('Preteen',2)]:
        pairs += [(f'{family} {i}',f'{family} {i+1}') for i in range(1,maximum)]
    pairs += [('English C 1-2','English 3'),('English 11','TEACHERS')]
    for pair in pairs:
        if estagios and estagios.issubset(set(pair)):
            prices=[_preco(e,precos) for e in pair]
            if all(p is not None for p in prices):
                yield 'Anual',pair,sum((Decimal(p) for p in prices),Decimal(0)),regiao['parcelas_anuais']

def estimar_descontos(df,ano_referencia=None,referencia=None):
    """Preserva linhas; datas delimitam um possível contrato, não sua identidade."""
    d=df.copy()
    for c in CAMPOS:d[c]=pd.Series(None,index=d.index,dtype=object)
    d['ResultadoEstimativa']='Dados insuficientes'
    required={'unidade','NumeroMatricula','NumeroParcela','Estagio','DataInicio','DataTermino','ValorComDesconto'}
    if d.empty or not required.issubset(d.columns):return d
    anos=pd.to_numeric(d['Turma'].astype(str).str.extract(r'(20\d{2})')[0],errors='coerce') if 'Turma' in d else pd.Series(float('nan'),index=d.index)
    if ano_referencia is not None:anos=anos.fillna(int(ano_referencia))
    inicio=pd.to_datetime(d['DataInicio'],errors='coerce')
    anos=anos.fillna(inicio.dt.year+inicio.dt.month.ge(11).astype(int))
    trabalho=d.assign(_Ano=anos,_Inicio=inicio,_Termino=pd.to_datetime(d['DataTermino'],errors='coerce'))
    refs={}
    for _,g in trabalho.groupby(['unidade','NumeroMatricula','_Inicio','_Termino','_Ano'],dropna=False,sort=False):
        idx=g.index
        # Registra o motivo da estimativa nas linhas do grupo analisado.
        def estado(msg):d.loc[idx,'ResultadoEstimativa']=msg
        ano=g['_Ano'].iloc[0]
        if pd.isna(ano):estado('Ano de referência não identificado');continue
        ano=int(ano)
        if ano not in refs:
            try:refs[ano]=referencia if referencia is not None and referencia.get('ano')==ano else carregar_precos(ano)
            except (OSError,ValueError,TypeError):refs[ano]=None
        ref=refs[ano]
        if ref is None:estado('Tabela de preços indisponível para o ano');continue
        regiao=next((r for r in ref['regioes'].values() if any(_normalizar(u)==_normalizar(g['unidade'].iloc[0]) for u in r['unidades'])),None)
        if regiao is None:estado('Unidade sem tabela de preços');continue
        d.loc[idx,'FonteEstimativa']=f"{ano} — {ref.get('fonte','Tabela de preços')}"
        start=g['_Inicio'].iloc[0];end=g['_Termino'].iloc[0]
        if pd.isna(start) or pd.isna(end):estado('Datas do contrato incompletas');continue
        if end<start:estado('Datas do contrato inconsistentes');continue
        if start.year+int(start.month>=11)!=ano:estado('Contrato de outro período de preços');continue
        nums=pd.to_numeric(g['NumeroParcela'],errors='coerce')
        if nums.isna().any() or (nums%1!=0).any() or nums.duplicated().any():
            estado('Ambíguo: parcelas repetidas ou contratos misturados');continue
        n=len(g)
        if set(nums.astype(int))!=set(range(1,n+1)):estado('Sequência de parcelas incompleta');continue
        if 'Situacao' in g and g['Situacao'].map(_normalizar).str.contains('cancel',regex=False).any():
            estado('Parcelas canceladas: conferir contrato');continue
        estagios=g['Estagio'].map(_estagio)
        if estagios.isna().any():estado('Estágio sem referência de preço');continue
        stages=set(estagios)
        if len(stages)>2:estado('Ambíguo: mais de dois estágios');continue
        vals=pd.to_numeric(g['ValorComDesconto'],errors='coerce')
        if vals.isna().any() or vals.le(0).any():estado('Valores insuficientes para estimativa');continue
        amounts=[Decimal(str(v)).quantize(CENTAVO,rounding=ROUND_HALF_UP) for v in vals]
        matches=set()
        for tipo,pair,integral,parcelamentos in _pacotes(stages,regiao):
            if n not in parcelamentos:continue
            # Uma duração claramente anual não pode virar semestral por uma carga parcial.
            if tipo=='Semestral' and (end-start).days>240:continue
            if tipo=='Anual' and (end-start).days<240:continue
            for percentual in ([0] if pair==('VIP',) else regiao['descontos']):
                total=integral*(Decimal(100)-Decimal(str(percentual)))/Decimal(100)
                parcela=(total/n).quantize(CENTAVO,rounding=ROUND_HALF_UP)
                desvios=[abs(a-parcela) for a in amounts]
                # Permite ajuste da última parcela, sem aceitar mensalidades/taxas distintas.
                grandes=[i for i,v in enumerate(desvios) if v>CENTAVO]
                ultima=int(nums.idxmax()) if isinstance(nums.index[0],int) else nums.idxmax()
                ultima_pos=list(g.index).index(ultima)
                if grandes and (grandes!=[ultima_pos] or desvios[ultima_pos]>CENTAVO*n):continue
                if abs(sum(amounts)-total)>CENTAVO*n:continue
                matches.add((float(percentual),tipo,pair,n))
        if len(matches)==1:
            desconto,tipo,pair,n=next(iter(matches))
            d.loc[idx,'DescontoEstimado']=desconto
            d.loc[idx,'PacoteEstimado']=tipo+' — '+' + '.join(pair)
            d.loc[idx,'ParcelamentoEstimado']=n
            estado('Correspondência encontrada' if stages==set(pair) else 'Correspondência encontrada; segundo estágio inferido')
        elif len(matches)>1:estado('Correspondência ambígua')
        else:estado('Sem correspondência na tabela')
    return d

def bolsa_exibida(df):
    """A informação do ERP tem prioridade; percentual não recebe nome de convênio."""
    bolsa=df['Bolsa'] if 'Bolsa' in df else pd.Series(None,index=df.index)
    valid=bolsa.notna() & ~bolsa.astype(str).map(_normalizar).isin(['','s/i','nao informado','nan','none'])
    estimado=df['DescontoEstimado'] if 'DescontoEstimado' in df else pd.Series(None,index=df.index)
    labels=estimado.map(lambda v:f'Desconto estimado: {float(v):g}%' if pd.notna(v) else 'Não identificado')
    return bolsa.where(valid,labels)
