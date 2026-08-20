import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from core.database import carregar_dados_auditados
import plotly.express as px
import plotly.graph_objects as go

def format_brl(val):
    if pd.isna(val):
        return "R$ 0,00"
    return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

ano_referencia = st.session_state.get("ano_referencia", datetime.now().year)

st.title(f"Dashboard {ano_referencia}")

df = carregar_dados_auditados()

if df.empty:
    st.warning("Nenhuma base financeira carregada. Vá até a aba de Sincronização.")
    st.stop()

# ---------------------------------------------------------
# HIGIENIZAÇÃO E CORREÇÃO DE ESTRUTURA
# ---------------------------------------------------------
for c in ['ValorComDesconto', 'ValorPago']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

for c in ['DataVencimento', 'DataPagamento', 'DataInicio']:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

# Adicionada FormaCobranca na sanitização para evitar falhas de agrupamento
for c in ['unidade', 'SemestreReferencia', 'Situacao', 'Curso', 'FormaCobranca']:
    if c not in df.columns:
        df[c] = 'S/I'
    else:
        df[c] = df[c].fillna('S/I').astype(str).str.strip()

# ---------------------------------------------------------
# ENGENHARIA DE FEATURES (RECONSTRUÇÃO DO ANO LETIVO)
# ---------------------------------------------------------
if 'DataInicio' in df.columns:
    df['MesInicio'] = df['DataInicio'].dt.month.fillna(1)
    df['AnoInicio'] = df['DataInicio'].dt.year.fillna(datetime.now().year)
    df['AnoLetivo'] = np.where(df['MesInicio'] >= 11, df['AnoInicio'] + 1, df['AnoInicio'])
else:
    df['AnoLetivo'] = datetime.now().year

# Blindagem da identificação de pagamento
df['IsQuitada'] = df['Situacao'].str.lower().str.contains('quitada', na=False)

# ---------------------------------------------------------
# FILTROS GLOBAIS
# ---------------------------------------------------------
st.markdown("### Filtros Globais")
c1, c2, c3 = st.columns(3)

with c1:
    lista_uni = ['Todas'] + sorted(df['unidade'].dropna().unique().tolist())
    uni_sel = st.selectbox("Unidade:", lista_uni)

with c2:
    lista_sem = ['Todos'] + sorted(df['SemestreReferencia'].dropna().unique().tolist())
    sem_sel = st.selectbox("Semestre Ref:", lista_sem)

with c3:
    anos_validos = sorted([int(x) for x in df['AnoLetivo'].dropna().unique() if int(x) > 2000])
    ano_padrao = anos_validos[-1] if anos_validos else datetime.now().year
    lista_ano = ['Todos'] + anos_validos
    ano_sel = st.selectbox("Ano Letivo:", lista_ano, index=lista_ano.index(ano_padrao) if ano_padrao in lista_ano else 0)

df_f = df.copy()
if uni_sel != 'Todas':
    df_f = df_f[df_f['unidade'] == uni_sel]
if sem_sel != 'Todos':
    df_f = df_f[df_f['SemestreReferencia'] == sem_sel]
if ano_sel != 'Todos':
    df_f = df_f[df_f['AnoLetivo'] == int(ano_sel)]

st.divider()

# ---------------------------------------------------------
# KPIs PRINCIPAIS (CAIXA REAL VS PREVISTO)
# ---------------------------------------------------------
hoje = pd.Timestamp(datetime.now().date())
is_quitada = df_f['IsQuitada']
is_vencida = (~is_quitada) & (df_f['DataVencimento'] <= hoje)

total_geral = df_f['ValorComDesconto'].sum()
total_recebido = df_f.loc[is_quitada, 'ValorPago'].sum()
total_inadimplente_real = df_f.loc[is_vencida, 'ValorComDesconto'].sum()
taxa_inadimplencia = (total_inadimplente_real / total_geral * 100) if total_geral > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Volume Faturado Previsto", format_brl(total_geral))
m2.metric("Caixa Real (Efetivado)", format_brl(total_recebido))
m3.metric("Passivo Vencido", format_brl(total_inadimplente_real), delta_color="inverse")
m4.metric("Taxa de Calote", f"{taxa_inadimplencia:.1f}%", delta_color="inverse")

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
            agrup_previsto = df_previsto.groupby('Mes_Ano')['ValorComDesconto'].sum().reset_index(name='Previsto')
            
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
        st.markdown("#### Mapa de Risco: Calote por Curso")
        if not df_f.empty and 'Curso' in df_f.columns:
            df_vencidos = df_f[is_vencida].copy()
            if not df_vencidos.empty:
                agrup_curso_venc = df_vencidos.groupby('Curso')['ValorComDesconto'].sum().reset_index().sort_values('ValorComDesconto', ascending=False)
                fig_curso_venc = px.bar(agrup_curso_venc, x='ValorComDesconto', y='Curso', orientation='h',
                                   labels={'ValorComDesconto': 'Passivo Vencido (R$)', 'Curso': ''},
                                   color='ValorComDesconto', color_continuous_scale='Reds')
                fig_curso_venc.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_curso_venc, use_container_width=True)
            else:
                st.info("Nenhuma inadimplência detectada no escopo filtrado.")

    st.subheader("Matriz Operacional por Unidade")
    if not df_f.empty:
        resumo_uni = df_f.groupby('unidade').agg(
            Total_Parcelas=('ValorComDesconto', 'count'),
            Faturado_Previsto=('ValorComDesconto', 'sum'),
            Caixa_Real=('ValorPago', lambda x: x[df_f.loc[x.index, 'IsQuitada']].sum()),
            Inadimplencia=('ValorComDesconto', lambda x: x[is_vencida.reindex(x.index, fill_value=False)].sum())
        ).reset_index()
        
        resumo_uni['Faturado_Previsto'] = resumo_uni['Faturado_Previsto'].map(format_brl)
        resumo_uni['Caixa_Real'] = resumo_uni['Caixa_Real'].map(format_brl)
        resumo_uni['Inadimplencia'] = resumo_uni['Inadimplencia'].map(format_brl)
        st.dataframe(resumo_uni, use_container_width=True, hide_index=True)

with tab_curso:
    st.subheader("Desempenho Financeiro por Curso")
    if not df_f.empty and 'Curso' in df_f.columns:
        agrup_curso = df_f.groupby('Curso').agg(
            Faturado=('ValorComDesconto', 'sum'),
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
            Faturado=('ValorComDesconto', 'sum'),
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
    st.markdown("Mede a entrada de volume financeiro e contratos baseado na **Data de Início**.")
    if not df_f.empty and 'DataInicio' in df_f.columns:
        df_historico = df_f.copy()
        # Filtra registros com DataInicio válida
        df_historico = df_historico[df_historico['DataInicio'].notna()]
        
        if not df_historico.empty:
            df_historico['Mes_Matricula'] = df_historico['DataInicio'].dt.to_period('M').astype(str)
            agrup_matricula = df_historico.groupby('Mes_Matricula').agg(
                Contratos=('NumeroMatricula', 'nunique'),
                Faturado_Gerado=('ValorComDesconto', 'sum')
            ).reset_index().sort_values('Mes_Matricula')
            
            fig_hist = px.bar(agrup_matricula, x='Mes_Matricula', y='Faturado_Gerado', text='Contratos',
                              labels={'Mes_Matricula': 'Mês de Início', 'Faturado_Gerado': 'Faturamento Gerado (R$)', 'Contratos': 'Novos Contratos'},
                              color='Faturado_Gerado', color_continuous_scale='Blues', title="Faturamento vs Contratos Fechados")
            
            fig_hist.update_traces(textposition='outside')
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Não há Datas de Início válidas para plotar o histórico nos filtros atuais.")