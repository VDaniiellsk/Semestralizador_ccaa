"""Apresenta os totais por turma e curso e o detalhe dos alunos selecionados."""
import streamlit as st
from core.database import carregar_dados_auditados
from core.analise import preparar_dados, resumo_grupos, contar_alunos
from views.componentes import filtros, tabela, brl, ROTULOS

st.title('Turmas, Estágios e Cursos')
df = preparar_dados(carregar_dados_auditados())
if df.empty:
    st.info('Nenhuma base carregada. Solicite uma sincronização ao administrador.')
    st.stop()
selecionado, _ = filtros(df, 'turmas')
c1, c2, c3, c4 = st.columns(4)
c1.metric('Alunos distintos', contar_alunos(selecionado))
c2.metric('Recebido', brl(selecionado.ValorRecebido.sum()))
c3.metric('A receber', brl(selecionado.ValorPendente.sum()))
c4.metric('Vencido', brl(selecionado.ValorVencido.sum()))
padrao = ['unidade', 'AnoLetivo', 'SemestreReferencia', 'Curso', 'Estagio', 'Turma']
resumo = resumo_grupos(selecionado, padrao)
grupos = st.multiselect('Agrupar painel por', list(resumo.columns), default=[],
                       format_func=lambda c: ROTULOS.get(c, c), key='turmas_separar_painel')
st.caption('Cada grupo recebe uma tabela com as mesmas colunas. A contagem usa unidade e matrícula; um aluno pode aparecer em mais de uma turma.')
tabela(resumo, 'turmas_resumo', agrupar=False, grupos=grupos, origem=selecionado, vinculos=padrao)
st.subheader('Consultar alunos de uma turma')
opcoes = sorted(set(zip(selecionado['unidade'], selecionado['Turma'])))
chave = 'turmas_consulta_alunos'
if chave in st.session_state and st.session_state[chave] not in opcoes:
    st.session_state[chave] = None
turma = st.selectbox('Turma para consultar alunos', opcoes, index=None,
                     placeholder='Selecione uma turma', key=chave,
                     format_func=lambda item: f'{item[0]} — {item[1]}')
if turma is not None:
    alunos = selecionado.loc[selecionado.unidade.eq(turma[0]) & selecionado.Turma.eq(turma[1])]
    colunas = ['NumeroMatricula', 'Sacado', 'Curso', 'Estagio', 'SemestreReferencia']
    st.caption(f'{contar_alunos(alunos)} alunos na turma selecionada, conforme os filtros aplicados.')
    tabela(alunos[colunas].drop_duplicates(), 'turmas_alunos', agrupar=True, origem=alunos, vinculos=colunas)
else:
    st.info('Selecione uma turma para visualizar seus alunos.')
