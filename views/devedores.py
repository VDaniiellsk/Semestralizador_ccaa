"""Apresenta os alunos com parcelas vencidas, seus valores e detalhamento."""
import streamlit as st
from core.database import carregar_dados_auditados
from core.analise import preparar_dados, resumo_alunos, ALUNO
from views.componentes import filtros, tabela, brl

st.title('Devedores Gerais')
st.caption('Aluno inadimplente: possui pelo menos uma parcela não paga, com vencimento até hoje. Parcelas canceladas não geram dívida.')
df = preparar_dados(carregar_dados_auditados())
if df.empty:
    st.info('Nenhuma base carregada. Solicite uma sincronização ao administrador.')
    st.stop()
selecionado, _ = filtros(df, 'devedores', mostrar_situacao=False)
resumo = resumo_alunos(selecionado)
resumo = resumo.loc[resumo.StatusAluno.eq('Inadimplente')]
c1, c2, c3 = st.columns(3)
c1.metric('Alunos devedores', len(resumo))
c2.metric('Valor vencido', brl(resumo.Vencido.sum()))
c3.metric('Parcelas vencidas', int(resumo.ParcelasVencidas.sum()))
tabela(resumo, 'devedores_resumo', origem=selecionado, vinculos=ALUNO)
st.subheader('Parcelas vencidas')
detalhe = selecionado.loc[selecionado.IsVencida].merge(resumo[ALUNO], on=ALUNO, validate='many_to_one')
campos = ['unidade', 'NumeroMatricula', 'Sacado', 'AnoLetivo', 'SemestreReferencia',
          'Curso', 'Estagio', 'Turma', 'NumeroParcela', 'DataVencimento', 'ValorComDesconto']
tabela(detalhe[campos], 'devedores_parcelas', agrupar=True, origem=detalhe)
st.caption('A base contém a última sincronização. Para consultar outro ano que não esteja disponível, sincronize esse ano primeiro.')
