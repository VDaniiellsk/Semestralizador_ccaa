"""Apresenta a matriz financeira por unidade e semestre com detalhamento."""
import streamlit as st
from core.database import carregar_dados_auditados
from core.analise import preparar_dados, resumo_grupos
from views.componentes import filtros, tabela, brl

st.title('Matriz de Valores')
df = preparar_dados(carregar_dados_auditados())
if df.empty:
    st.info('Nenhuma base carregada. Solicite uma sincronização ao administrador.')
    st.stop()
selecionado, _ = filtros(df, 'matriz')
with st.expander('Filtrar por datas'):
    for campo, rotulo in [('DataVencimento', 'Vencimento'), ('DataInicio', 'Início do contrato')]:
        ativos = selecionado[campo].dropna()
        if not ativos.empty and st.checkbox(f'Usar intervalo de {rotulo.lower()}', key=f'matriz_usar_{campo}'):
            intervalo = st.date_input(rotulo, (ativos.min().date(), ativos.max().date()), format='DD/MM/YYYY', key=f'matriz_data_{campo}')
            if len(intervalo) == 2:
                selecionado = selecionado.loc[selecionado[campo].between(str(intervalo[0]), str(intervalo[1]))]
c1, c2, c3 = st.columns(3)
c1.metric('Previsto', brl(selecionado.ValorPrevisto.sum()))
c2.metric('Recebido', brl(selecionado.ValorRecebido.sum()))
c3.metric('A receber', brl(selecionado.ValorPendente.sum()))
st.subheader('Valores por unidade e semestre')
tabela(resumo_grupos(selecionado, ['unidade', 'AnoLetivo', 'SemestreReferencia']), 'matriz_resumo', origem=selecionado, vinculos=['unidade', 'AnoLetivo', 'SemestreReferencia'])
with st.expander('Detalhamento das parcelas'):
    campos = ['unidade', 'NumeroMatricula', 'Sacado', 'AnoLetivo', 'SemestreReferencia',
              'Curso', 'Estagio', 'Turma', 'NumeroParcela', 'DataInicio', 'DataVencimento',
              'ValorComDesconto', 'ValorComJuros', 'ValorPago', 'SituacaoParcela']
    tabela(selecionado[campos], 'matriz_parcelas', agrupar=True, origem=selecionado)
