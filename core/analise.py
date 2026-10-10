"""Prepara os indicadores financeiros e os recortes usados nas telas.

Os valores partem das parcelas; os alunos são contados por unidade e matrícula.
O estado de inadimplência usa a base de referência anterior ao filtro de situação."""
import unicodedata
import pandas as pd

ALUNO = ['unidade', 'NumeroMatricula']
NAO_INFORMADO = 'Não informado'


def _normalizar(value):
    """Padroniza o texto para comparação, sem alterar o dado original exibido."""
    text = unicodedata.normalize('NFKD', str(value))
    return ''.join(c for c in text if not unicodedata.combining(c)).casefold().strip()


def preparar_dados(df, hoje=None):
    """Calcula os campos auxiliares de análise e atualiza as estimativas antes dos filtros."""
    d = df.copy().reset_index(drop=True)
    for c in ['unidade', 'NumeroMatricula', 'Sacado', 'Turma', 'Curso', 'Estagio',
              'Situacao', 'SemestreReferencia', 'Bolsa', 'FormaCobranca']:
        if c not in d:
            d[c] = NAO_INFORMADO
        d[c] = d[c].fillna(NAO_INFORMADO).astype(str).str.strip().replace('', NAO_INFORMADO)
    from core.catalogo import classificar
    classificar(d)
    d['Estagio'] = d['Estagio'].fillna(NAO_INFORMADO)
    for c in ['ValorComDesconto', 'ValorPago', 'ValorComJuros']:
        if c not in d:
            d[c] = 0.0
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0.0)
    for c in ['DataInicio', 'DataTermino', 'DataVencimento', 'DataPagamento']:
        if c not in d:
            d[c] = pd.NaT
        d[c] = pd.to_datetime(d[c], errors='coerce')
    # Calcula antes dos filtros também para a última carga existente.
    from core.descontos import estimar_descontos, bolsa_exibida
    d=estimar_descontos(d)
    d['BolsaConvenio']=bolsa_exibida(d)
    # O ano da turma tem precedência, como no filtro da sincronização atual.
    ano_turma = pd.to_numeric(d['Turma'].str.extract(r'(20\d{2})')[0], errors='coerce')
    inicio = d['DataInicio']
    ano_inicio = inicio.dt.year + inicio.dt.month.ge(11).astype(int)
    d['AnoLetivo'] = ano_turma.combine_first(ano_inicio).astype('Int64')
    situacao = d['Situacao'].map(_normalizar)
    cancelada = situacao.str.contains('cancel', regex=False)
    negativa = situacao.str.contains(r'nao\s+pag|a\s+pagar|pendente|em\s+aberto|vencid|atras', regex=True)
    paga = situacao.str.contains(r'quitad|liquid|\bpag(?:[ao]|$)|recebid', regex=True) & ~negativa & ~cancelada
    d['SituacaoParcela'] = 'Não informada'
    d.loc[negativa, 'SituacaoParcela'] = 'Pendente'
    d.loc[paga, 'SituacaoParcela'] = 'Paga'
    d.loc[cancelada, 'SituacaoParcela'] = 'Cancelada'
    d['IsQuitada'] = paga
    d['IsPendente'] = d['SituacaoParcela'].eq('Pendente')
    hoje = pd.Timestamp(hoje if hoje is not None else pd.Timestamp.today()).normalize()
    d['IsVencida'] = d['IsPendente'] & d['DataVencimento'].le(hoje)
    d['ValorPrevisto'] = d['ValorComDesconto'].where(~cancelada, 0.0)
    d['ValorRecebido'] = d['ValorPago'].where(paga, 0.0)
    d['ValorPendente'] = d['ValorComDesconto'].where(d['IsPendente'], 0.0)
    d['ValorVencido'] = d['ValorComDesconto'].where(d['IsVencida'], 0.0)
    return d


def filtrar_dados(df, busca='', **filtros):
    """Aplica os critérios selecionados e devolve apenas os registros correspondentes."""
    d = df.copy()
    for coluna, valor in filtros.items():
        if valor is None or valor == 'Todos':
            continue
        if coluna == 'AnoLetivo' and valor == NAO_INFORMADO:
            d = d.loc[d[coluna].isna()]
        else:
            d = d.loc[d[coluna].eq(valor)]
    if busca.strip():
        termo = _normalizar(busca)
        mask = d['Sacado'].map(_normalizar).str.contains(termo, regex=False)
        mask |= d['NumeroMatricula'].str.contains(busca.strip(), regex=False, case=False)
        d = d.loc[mask]
    return d.copy()


def contar_alunos(df):
    """Conta alunos distintos pela combinação de unidade e matrícula."""
    return len(df[ALUNO].drop_duplicates())


def resumo_alunos(df, referencia=None):
    """Resume valores por aluno e consulta a referência completa para determinar sua situação."""
    resumo = df.groupby(ALUNO, as_index=False, dropna=False).agg(
        Sacado=('Sacado', 'first'),
        Previsto=('ValorPrevisto', 'sum'), Recebido=('ValorRecebido', 'sum'),
        Pendente=('ValorPendente', 'sum'), Vencido=('ValorVencido', 'sum'),
        ParcelasVencidas=('IsVencida', 'sum'), Parcelas=('NumeroParcela', 'size'),
        BolsaConvenio=('BolsaConvenio',lambda s:'; '.join(sorted(set(s.dropna().astype(str))))))
    referencia = df if referencia is None else referencia
    status = referencia.groupby(ALUNO, as_index=False, dropna=False)['IsVencida'].any()
    resumo = resumo.merge(status, on=ALUNO, how='left', validate='one_to_one')
    resumo['StatusAluno'] = resumo['IsVencida'].fillna(False).map({True: 'Inadimplente', False: 'Em dia'})
    return resumo.drop(columns='IsVencida')


def resumo_grupos(df, grupos):
    """Consolida parcelas por campos escolhidos sem contar o mesmo aluno duas vezes no grupo."""
    if not grupos:
        raise ValueError('Selecione pelo menos um campo para agrupar.')
    d = df.copy()
    # Matrículas iguais em unidades diferentes continuam sendo alunos distintos.
    d['_Aluno'] = list(zip(d['unidade'], d['NumeroMatricula']))
    d['_Devedor'] = d['_Aluno'].where(d['IsVencida'])
    return d.groupby(grupos, as_index=False, dropna=False).agg(
        Alunos=('_Aluno', 'nunique'), Devedores=('_Devedor', 'nunique'),
        Parcelas=('NumeroParcela', 'size'), Previsto=('ValorPrevisto', 'sum'),
        Recebido=('ValorRecebido', 'sum'), Pendente=('ValorPendente', 'sum'),
        Vencido=('ValorVencido', 'sum'))



def separar_grupos(df, campos):
    """Divide as linhas para exibição, preservando colunas e valores."""
    campos = list(dict.fromkeys(campos))
    if not campos:
        yield (), df
        return
    missing = set(campos) - set(df.columns)
    if missing:
        raise ValueError('Campos de agrupamento inexistentes: ' + ', '.join(sorted(missing)))
    chave = campos[0] if len(campos) == 1 else campos
    for valores, linhas in df.groupby(chave, dropna=False, sort=False, observed=True):
        yield (valores,) if len(campos) == 1 else valores, linhas


def totais_tabela(parte, origem, vinculos=None, referencia=None):
    """Totais das linhas exibidas; alunos são distintos dentro de cada tabela."""
    if vinculos:
        chaves=parte[list(vinculos)].drop_duplicates()
        base=origem.merge(chaves,on=list(vinculos),how='inner',validate='many_to_one')
    else:
        base=origem.loc[parte.index]
    devedores=base
    if referencia is not None:
        if vinculos:
            devedores=referencia.merge(chaves,on=list(vinculos),how='inner',validate='many_to_one')
        else:
            devedores=referencia
        devedores=devedores.merge(base[ALUNO].drop_duplicates(),on=ALUNO,how='inner',validate='many_to_one')
    return dict(Alunos=contar_alunos(base),
                Pendente=float(base['ValorPendente'].sum()),
                Recebido=float(base['ValorRecebido'].sum()),
                Devedores=contar_alunos(devedores.loc[devedores['IsVencida']]),
                Vencido=float(base['ValorVencido'].sum()))
