"""Componentes compartilhados de filtros, tabelas e totais.

Agrupar separa os registros em tabelas, sem transformar suas colunas.
Os totais consultam as parcelas de origem para evitar duplicação de alunos."""
import pandas as pd
import streamlit as st
from core.analise import filtrar_dados, separar_grupos, totais_tabela, NAO_INFORMADO

ROTULOS = {
    'unidade': 'Unidade', 'NumeroMatricula': 'Matrícula', 'Sacado': 'Aluno / Sacado',
    'Turma': 'Turma', 'Curso': 'Curso', 'Estagio': 'Estágio', 'AnoLetivo': 'Ano letivo',
    'SemestreReferencia': 'Semestre', 'SituacaoParcela': 'Situação da parcela',
    'NumeroParcela': 'Número da parcela', 'Situacao': 'Situação no ERP',
    'DataInicio': 'Início do contrato', 'DataTermino': 'Término do contrato',
    'DataVencimento': 'Vencimento', 'DataPagamento': 'Pagamento',
    'ValorComDesconto': 'Valor com desconto', 'ValorPago': 'Valor pago no ERP',
    'ValorComJuros': 'Valor com juros', 'TipoContrato': 'Tipo do contrato',
    'Bolsa': 'Bolsa / Convênio', 'FormaCobranca': 'Forma de cobrança',
    'NomeAtendente': 'Atendente', 'NomeOperadoraCartao': 'Operadora do cartão',
    'SituacaoAluno': 'Situação acadêmica', 'Previsto': 'Previsto',
    'Recebido': 'Recebido', 'Pendente': 'A receber', 'Vencido': 'Vencido',
    'ParcelasVencidas': 'Parcelas vencidas', 'StatusAluno': 'Situação financeira',
    'DescontoEstimado': 'Desconto estimado (%)', 'PacoteEstimado': 'Pacote estimado',
    'ParcelamentoEstimado': 'Parcelamento estimado', 'ResultadoEstimativa': 'Resultado da estimativa',
    'FonteEstimativa': 'Referência de preços', 'BolsaConvenio': 'Bolsa / Convênio ou estimativa',
    'Alunos': 'Alunos', 'Devedores': 'Devedores', 'Parcelas': 'Parcelas'}
MOEDAS = ['Previsto', 'Recebido', 'Pendente', 'Vencido', 'ValorComDesconto',
          'ValorPago', 'ValorComJuros', 'ValorPrevisto', 'ValorRecebido', 'ValorPendente', 'ValorVencido']


def brl(value):
    """Formata um valor para apresentação em reais, sem mudar o número usado nos cálculos."""
    return f'R$ {float(value):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notna(value) else '-'


def filtros(df, prefixo, mostrar_situacao=True):
    """Monta os filtros e devolve o recorte exibido e a referência anterior ao filtro de situação."""
    st.subheader('Filtros de pesquisa')
    st.caption('Parcelas canceladas não entram nos totais financeiros.')
    desconhecidas = int(df['SituacaoParcela'].eq('Não informada').sum())
    if desconhecidas:
        st.warning(f'{desconhecidas} parcelas têm situação não reconhecida. Confira a origem antes de avaliar os totais.')
    escolhas = {}
    campos = ['unidade', 'AnoLetivo', 'SemestreReferencia', 'Curso', 'Estagio', 'Turma']
    for inicio in (0, 3):
        for col, campo in zip(st.columns(3), campos[inicio:inicio+3]):
            if campo == 'AnoLetivo':
                valores = sorted(int(v) for v in df[campo].dropna().unique())
                if df[campo].isna().any():
                    valores.append(NAO_INFORMADO)
            else:
                valores = sorted(df[campo].dropna().unique().tolist())
            escolhas[campo] = col.selectbox(ROTULOS[campo], ['Todos'] + valores, key=f'{prefixo}_{campo}')
    busca = st.text_input('Aluno ou matrícula', key=f'{prefixo}_busca')
    referencia = filtrar_dados(df, busca=busca, **escolhas)
    if mostrar_situacao:
        situacao = st.selectbox('Situação da parcela', ['Todos', 'Paga', 'Pendente', 'Cancelada', 'Não informada'], key=f'{prefixo}_situacao')
        return filtrar_dados(referencia, SituacaoParcela=situacao), referencia
    return referencia, referencia


def tabela(df, chave, agrupar=True, grupos=None, origem=None, vinculos=None, referencia=None):
    """Exibe registros, ordenação, agrupamentos separados e totais de cada tabela.

    origem e vinculos permitem calcular os totais a partir das parcelas, mesmo
    quando a tabela é um resumo. A referência mantém a situação real dos alunos."""
    if df.empty:
        st.info('Nenhum registro encontrado para os filtros selecionados.')
        return
    d = df.copy()
    grupos = list(grupos or [])
    with st.expander('Organizar tabela'):
        if agrupar:
            grupos = st.multiselect('Agrupar por', list(d.columns), format_func=lambda c: ROTULOS.get(c, c), key=f'{chave}_grupos')

        ordem_key = f'{chave}_ordem'
        if ordem_key in st.session_state:
            st.session_state[ordem_key] = [c for c in st.session_state[ordem_key] if c in d.columns]
        ordem = st.multiselect('Ordenar por', list(d.columns), format_func=lambda c: ROTULOS.get(c, c), key=f'{chave}_ordem')
        crescente = st.checkbox('Ordem crescente', value=True, key=f'{chave}_crescente')
    if ordem:
        d = d.sort_values(ordem, ascending=crescente, kind='stable', na_position='last')
    # Formatação nativa mantém números ordenáveis e não tem o limite do Styler.
    configuracao = {}
    for c in d.columns:
        rotulo = ROTULOS.get(c, c)
        if c in MOEDAS:
            configuracao[rotulo] = st.column_config.NumberColumn(rotulo, format="R$ %.2f")
        elif c == 'DescontoEstimado':
            configuracao[rotulo] = st.column_config.NumberColumn(rotulo, format='%.2f%%')
        elif c == 'ParcelamentoEstimado':
            configuracao[rotulo] = st.column_config.NumberColumn(rotulo, format='%d')
        elif c == 'AnoLetivo':
            configuracao[rotulo] = st.column_config.NumberColumn(rotulo, format="%d")
    for c in d.select_dtypes(include=['datetime']).columns:
        rotulo = ROTULOS.get(c, c)
        configuracao[rotulo] = st.column_config.DateColumn(rotulo, format="DD/MM/YYYY")
    partes = list(separar_grupos(d, grupos))
    inicio, fim = 0, len(partes)
    if len(partes) > 20:
        paginas = (len(partes) + 19) // 20
        pagina_key = f'{chave}_pagina_grupos'
        if pagina_key in st.session_state:
            st.session_state[pagina_key] = min(st.session_state[pagina_key], paginas)
        pagina = st.number_input('Página de grupos', min_value=1, max_value=paginas,
                                 value=1, step=1, key=pagina_key)
        inicio = (pagina - 1) * 20
        fim = min(inicio + 20, len(partes))
        st.caption(f'Grupos {inicio + 1} a {fim} de {len(partes)}')
    for valores, parte in partes[inicio:fim]:
        if grupos:
            titulo = []
            for campo, valor in zip(grupos, valores):
                if pd.isna(valor):
                    texto = NAO_INFORMADO
                elif campo in MOEDAS:
                    texto = brl(valor)
                elif isinstance(valor, pd.Timestamp):
                    texto = valor.strftime('%d/%m/%Y')
                else:
                    texto = str(valor)
                titulo.append(f'{ROTULOS.get(campo, campo)}: {texto}')
            st.subheader(' · '.join(titulo))
        if origem is not None:
            totais = totais_tabela(parte, origem, vinculos, referencia)
            colunas = st.columns(5)
            for col, campo, rotulo in zip(colunas,
                    ['Alunos', 'Pendente', 'Recebido', 'Vencido', 'Devedores'],
                    ['Total de alunos', 'Total a receber', 'Total recebido', 'Valor inadimplente', 'Alunos inadimplentes']):
                valor = brl(totais[campo]) if campo in MOEDAS else totais[campo]
                col.metric(rotulo, valor)
        st.dataframe(parte.rename(columns=ROTULOS), column_config=configuracao,
                     use_container_width=True, hide_index=True)
