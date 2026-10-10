"""Apresenta a situação financeira por aluno e suas parcelas de origem."""
import streamlit as st
from core.database import carregar_dados_auditados
from core.analise import preparar_dados, resumo_alunos, ALUNO
from views.componentes import filtros, tabela, brl

st.title('Financeira por Aluno')
df = preparar_dados(carregar_dados_auditados())
if df.empty:
    st.info('Nenhuma base carregada. Solicite uma sincronização ao administrador.')
    st.stop()
selecionado, referencia = filtros(df, 'alunos')
resumo = resumo_alunos(selecionado, referencia)
status = st.radio('Situação financeira do aluno', ['Todos', 'Inadimplente', 'Em dia'], horizontal=True)
if status != 'Todos':
    resumo = resumo.loc[resumo.StatusAluno.eq(status)]
st.caption('Cada aluno é contado uma vez por unidade e matrícula. A situação financeira considera todas as parcelas do período e dos cursos selecionados, antes do filtro de situação da parcela.')
c1, c2, c3, c4 = st.columns(4)
c1.metric('Alunos', len(resumo))
c2.metric('Previsto', brl(resumo.Previsto.sum()))
c3.metric('Recebido', brl(resumo.Recebido.sum()))
c4.metric('A receber', brl(resumo.Pendente.sum()))
st.subheader('Resumo por aluno')
tabela(resumo, 'alunos_resumo', origem=selecionado, vinculos=ALUNO, referencia=referencia)
st.subheader('Parcelas e turmas dos alunos selecionados')
st.caption('A bolsa do ERP tem prioridade. A estimativa compara os valores cobrados com a tabela anual, sem atribuir nome de convênio. Pacotes inferidos e correspondências ambíguas devem ser conferidos.')
detalhe = selecionado.merge(resumo[ALUNO], on=ALUNO, how='inner', validate='many_to_one')
campos = ['unidade', 'NumeroMatricula', 'Sacado', 'AnoLetivo', 'SemestreReferencia',
          'Curso', 'Estagio', 'Turma', 'NumeroParcela', 'DataVencimento',
          'SituacaoParcela', 'ValorComDesconto', 'ValorPago', 'Bolsa', 'BolsaConvenio',
          'DescontoEstimado', 'PacoteEstimado', 'ParcelamentoEstimado', 'ResultadoEstimativa']
tabela(detalhe[campos], 'alunos_parcelas', agrupar=True, origem=detalhe)
