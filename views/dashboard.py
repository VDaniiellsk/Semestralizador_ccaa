"""Apresenta a visão geral de receitas, recebimentos e parcelas vencidas."""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from core.database import carregar_dados_auditados
from core.analise import preparar_dados, contar_alunos
from views.componentes import filtros
import plotly.express as px
import plotly.graph_objects as go

def format_brl(val):
    """Formata um valor para apresentação em reais no painel."""
    if pd.isna(val):
        return "R$ 0,00"
    return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

ano_referencia = st.session_state.get("ano_referencia", datetime.now().year)

st.title("Visão Geral")

df = preparar_dados(carregar_dados_auditados())
if df.empty:
    st.info("Nenhuma base carregada. Solicite uma sincronização ao administrador.")
    st.stop()
df_f, _ = filtros(df, 'geral')
st.divider()

hoje = pd.Timestamp(datetime.now().date())
is_quitada = df_f['IsQuitada']
is_vencida = df_f['IsVencida']

total_geral = df_f['ValorPrevisto'].sum()
total_recebido = df_f.loc[is_quitada, 'ValorPago'].sum()
total_inadimplente_real = df_f.loc[is_vencida, 'ValorPrevisto'].sum()
taxa_inadimplencia = (total_inadimplente_real / total_geral * 100) if total_geral > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Volume Faturado Previsto", format_brl(total_geral))
m2.metric("Caixa Real (Efetivado)", format_brl(total_recebido))
m3.metric("Passivo Vencido", format_brl(total_inadimplente_real), delta_color="inverse")
m4.metric("Taxa de Inadimplência", f"{taxa_inadimplencia:.1f}%", delta_color="inverse")

p1, p2 = st.columns(2)
p1.metric("A receber", format_brl(df_f['ValorPendente'].sum()))
p2.metric("Alunos devedores", contar_alunos(df_f.loc[df_f.IsVencida]))

st.divider()

# ---------------------------------------------------------
# SISTEMA DE ABAS (NAVEGAÇÃO ANALÍTICA)
# ---------------------------------------------------------
tab_geral, tab_curso, tab_cobranca, tab_historico = st.tabs([
    "• Visão Geral & Risco", 
    "• Análise por Curso", 
    "• Formas de Cobrança", 
    "• Histórico de Matrículas"
])

with tab_geral:
    st.subheader("Análise Estratégica de Risco e Fluxo")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("#### Curva de Fluxo de Caixa (Mês a Mês)")
        if not df_f.empty and 'DataVencimento' in df_f.columns:
            df_previsto = df_f.copy()
            df_previsto['Mes_Ano'] = df_previsto['DataVencimento'].dt.to_period('M').astype(str)
            agrup_previsto = df_previsto.groupby('Mes_Ano')['ValorPrevisto'].sum().reset_index(name='Previsto')
            
            df_realizado = df_f[df_f['IsQuitada']].copy()
            df_realizado['Mes_Ano'] = df_realizado['DataPagamento'].dt.to_period('M').astype(str)
            agrup_realizado = df_realizado.groupby('Mes_Ano')['ValorPago'].sum().reset_index(name='Realizado')
            
            fluxo = pd.merge(agrup_previsto, agrup_realizado, on='Mes_Ano', how='outer').fillna(0).sort_values('Mes_Ano')
            
            fig_fluxo = px.line(fluxo, x='Mes_Ano', y=['Previsto', 'Realizado'], 
                                labels={'value': 'Montante (R$)', 'Mes_Ano': 'Mês de Referência', 'variable': 'Fluxo'},
                                color_discrete_map={'Previsto': '#636EFA', 'Realizado': '#00CC96'},
                                markers=True)
            st.plotly_chart(fig_fluxo, use_container_width=True)

    with col_g2:
        st.markdown("#### Inadimplência por Curso")
        if not df_f.empty and 'Curso' in df_f.columns:
            df_vencidos = df_f[is_vencida].copy()
            if not df_vencidos.empty:
                agrup_curso_venc = df_vencidos.groupby('Curso')['ValorPrevisto'].sum().reset_index().sort_values('ValorPrevisto', ascending=False)
                fig_curso_venc = px.bar(agrup_curso_venc, x='ValorPrevisto', y='Curso', orientation='h',
                                   labels={'ValorPrevisto': 'Passivo Vencido (R$)', 'Curso': ''},
                                   color='ValorPrevisto', color_continuous_scale='Reds')
                fig_curso_venc.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_curso_venc, use_container_width=True)
            else:
                st.info("Nenhuma inadimplência detectada no escopo filtrado.")

    st.subheader("Matriz Operacional por Unidade")
    if not df_f.empty:
        resumo_uni = df_f.groupby('unidade').agg(
            Total_Parcelas=('ValorPrevisto', 'count'),
            Faturado_Previsto=('ValorPrevisto', 'sum'),
            Caixa_Real=('ValorPago', lambda x: x[df_f.loc[x.index, 'IsQuitada']].sum()),
            Inadimplencia=('ValorPrevisto', lambda x: x[is_vencida.reindex(x.index, fill_value=False)].sum())
        ).reset_index()
        
        resumo_uni['Faturado_Previsto'] = resumo_uni['Faturado_Previsto'].map(format_brl)
        resumo_uni['Caixa_Real'] = resumo_uni['Caixa_Real'].map(format_brl)
        resumo_uni['Inadimplencia'] = resumo_uni['Inadimplencia'].map(format_brl)
        st.dataframe(resumo_uni, use_container_width=True, hide_index=True)

with tab_curso:
    st.subheader("Desempenho Financeiro por Curso")
    if not df_f.empty and 'Curso' in df_f.columns:
        agrup_curso = df_f.groupby('Curso').agg(
            Faturado=('ValorPrevisto', 'sum'),
            Realizado=('ValorPago', lambda x: x[df_f.loc[x.index, 'IsQuitada']].sum())
        ).reset_index()
        
        fig_cur = go.Figure()
        fig_cur.add_trace(go.Bar(x=agrup_curso['Curso'], y=agrup_curso['Faturado'], name='Faturado Previsto', marker_color='#636EFA'))
        fig_cur.add_trace(go.Bar(x=agrup_curso['Curso'], y=agrup_curso['Realizado'], name='Caixa Efetivado', marker_color='#00CC96'))
        fig_cur.update_layout(barmode='group', xaxis_title="Cursos", yaxis_title="Montante (R$)")
        st.plotly_chart(fig_cur, use_container_width=True)

with tab_cobranca:
    st.subheader("Distribuição por Forma de Cobrança")
    if not df_f.empty and 'FormaCobranca' in df_f.columns:
        agrup_cobranca = df_f.groupby('FormaCobranca').agg(
            Faturado=('ValorPrevisto', 'sum'),
            Realizado=('ValorPago', lambda x: x[df_f.loc[x.index, 'IsQuitada']].sum())
        ).reset_index().sort_values('Faturado', ascending=False)
        
        c_graf, c_tab = st.columns([6, 4])
        with c_graf:
            fig_cob = px.pie(agrup_cobranca, values='Faturado', names='FormaCobranca', hole=0.4, title="Participação no Faturamento Previsto")
            st.plotly_chart(fig_cob, use_container_width=True)
            
        with c_tab:
            st.markdown("##### Detalhamento")
            agrup_cobranca['Faturado (R$)'] = agrup_cobranca['Faturado'].map(format_brl)
            agrup_cobranca['Caixa (R$)'] = agrup_cobranca['Realizado'].map(format_brl)
            st.dataframe(agrup_cobranca[['FormaCobranca', 'Faturado (R$)', 'Caixa (R$)']], hide_index=True, use_container_width=True)

with tab_historico:
    st.subheader("Tração Operacional: Curva de Matrículas")
    st.markdown("Distribuição dos alunos e valores pela data de início do contrato.")
    if not df_f.empty and 'DataInicio' in df_f.columns:
        df_historico = df_f.copy()
        # Filtra registros com DataInicio válida
        df_historico = df_historico[df_historico['DataInicio'].notna()]
        
        if not df_historico.empty:
            df_historico['Mes_Matricula'] = df_historico['DataInicio'].dt.to_period('M').astype(str)
            df_historico['_Aluno'] = list(zip(df_historico['unidade'], df_historico['NumeroMatricula']))
            agrup_matricula = df_historico.groupby('Mes_Matricula').agg(
                Alunos=('_Aluno', 'nunique'),
                Faturado_Gerado=('ValorPrevisto', 'sum')
            ).reset_index().sort_values('Mes_Matricula')
            
            fig_hist = px.bar(agrup_matricula, x='Mes_Matricula', y='Faturado_Gerado', text='Alunos',
                              labels={'Mes_Matricula': 'Mês de Início', 'Faturado_Gerado': 'Faturamento Gerado (R$)', 'Alunos': 'Alunos'},
                              color='Faturado_Gerado', color_continuous_scale='Blues', title="Valores previstos e alunos")
            
            fig_hist.update_traces(textposition='outside')
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Não há Datas de Início válidas para plotar o histórico nos filtros atuais.")