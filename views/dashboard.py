import streamlit as st
import pandas as pd
from datetime import datetime
from core.database import carregar_dados_auditados

def format_brl(val):
    if pd.isna(val):
        return "R$ 0,00"
    return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("📊 Dashboard Financeiro Consolidado")

df = carregar_dados_auditados()

if df.empty:
    st.warning("Nenhuma base financeira carregada. Vá até a aba de Sincronização.")
    st.stop()

# Higienização
for c in ['valor', 'valor_com_desconto', 'valor_pago']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

date_cols = ['data_vencimento', 'data_pagamento']
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], dayfirst=True, errors='coerce')

for c in ['unidade', 'semestre_ref', 'situacao']:
    if c not in df.columns:
        df[c] = 'S/I'
    else:
        df[c] = df[c].fillna('S/I').astype(str).str.strip()

# ---------------------------------------------------------
# FILTROS GLOBAIS
# ---------------------------------------------------------
st.markdown("### Filtros Globais")
c1, c2, c3 = st.columns(3)

with c1:
    lista_uni = ['Todas'] + sorted(df['unidade'].dropna().unique().tolist())
    uni_sel = st.selectbox("Unidade:", lista_uni)

with c2:
    lista_sem = ['Todos'] + sorted(df['semestre_ref'].dropna().unique().tolist())
    sem_sel = st.selectbox("Semestre Ref:", lista_sem)

with c3:
    if 'ano_ref' in df.columns:
        anos_validos = sorted([int(x) for x in df['ano_ref'].dropna().unique() if int(x) > 2000])
        ano_padrao = anos_validos[-1] if anos_validos else 2026
        lista_ano = ['Todos'] + anos_validos
        ano_sel = st.selectbox("Ano Ref:", lista_ano, index=lista_ano.index(ano_padrao) if ano_padrao in lista_ano else 0)
    else:
        ano_sel = 'Todos'

df_f = df.copy()
if uni_sel != 'Todas':
    df_f = df_f[df_f['unidade'] == uni_sel]
if sem_sel != 'Todos':
    df_f = df_f[df_f['semestre_ref'] == sem_sel]
if ano_sel != 'Todos' and 'ano_ref' in df_f.columns:
    df_f = df_f[pd.to_numeric(df_f['ano_ref'], errors='coerce') == int(ano_sel)]

st.divider()

# ---------------------------------------------------------
# KPIs PRINCIPAIS
# ---------------------------------------------------------
hoje = pd.Timestamp(datetime.now().date())
is_quitada = df_f['situacao'].str.lower().str.contains('quitad|receb|pag|liquid', na=False)
is_vencida = ~is_quitada & (df_f['data_vencimento'] <= hoje)

total_geral = df_f['valor_com_desconto'].sum()
total_recebido = df_f.loc[is_quitada, 'valor_com_desconto'].sum()
total_inadimplente_real = df_f.loc[is_vencida, 'valor_com_desconto'].sum()

m1, m2, m3 = st.columns(3)
m1.metric("Volume Total Faturado", format_brl(total_geral))
m2.metric("Total Recebido (Efetivo + Bolsas)", format_brl(total_recebido))
m3.metric("Inadimplência Real (Vencida)", format_brl(total_inadimplente_real), delta_color="inverse")

st.divider()

# ---------------------------------------------------------
# GRÁFICOS RESTAURADOS
# ---------------------------------------------------------
st.subheader("📈 Visão Analítica Consolidada")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("#### Faturamento por Unidade")
    if not df_f.empty:
        df_uni = df_f.groupby('unidade')['valor_com_desconto'].sum().reset_index()
        df_uni.columns = ['Unidade', 'Valor']
        st.bar_chart(df_uni.set_index('Unidade'))

with col_g2:
    st.markdown("#### Status das Parcelas")
    if not df_f.empty:
        df_sit = df_f.groupby('situacao')['valor_com_desconto'].sum().reset_index()
        df_sit.columns = ['Situação', 'Valor']
        st.bar_chart(df_sit.set_index('Situação'))

st.divider()

st.subheader("Desempenho Financeiro Detalhado por Unidade")
if not df_f.empty:
    resumo_uni = df_f.groupby('unidade').agg(
        Total_Parcelas=('valor', 'count'),
        Valor_Previsto=('valor_com_desconto', 'sum'),
        Valor_Recebido=('valor_com_desconto', lambda x: x[df_f.loc[x.index, 'situacao'].str.lower().str.contains('quitad|receb|pag|liquid', na=False)].sum())
    ).reset_index()
    resumo_uni['Valor_Previsto'] = resumo_uni['Valor_Previsto'].map(format_brl)
    resumo_uni['Valor_Recebido'] = resumo_uni['Valor_Recebido'].map(format_brl)
    st.dataframe(resumo_uni, use_container_width=True, hide_index=True)