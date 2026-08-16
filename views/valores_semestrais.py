import streamlit as st
import pandas as pd
from core.database import carregar_dados_auditados

def format_brl(val):
    if pd.isna(val):
        return "R$ 0,00"
    return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("📅 Matriz de Valores e Auditoria Avançada")

df = carregar_dados_auditados()

if df.empty:
    st.warning("Nenhuma base financeira carregada. Vá até a aba 'Upload & Sincronização'.")
    st.stop()

# ---------------------------------------------------------
# HIGIENIZAÇÃO DE TIPOS E DATAS
# ---------------------------------------------------------
cols_num = ['valor', 'valor_com_desconto', 'valor_com_juros', 'valor_pago']
for c in cols_num:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

date_cols = ['data_vencimento', 'data_contrato', 'data_pagamento', 'data_matricula', 'data_termino']
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], dayfirst=True, errors='coerce')

# ---------------------------------------------------------
# FILTROS DE PESQUISA
# ---------------------------------------------------------
st.markdown("### Filtros de Pesquisa")
f1, f2, f3 = st.columns(3)
f4, f5 = st.columns(2)

with f1:
    if 'unidade' in df.columns:
        lista_uni = ['Todas'] + sorted(df['unidade'].dropna().unique().tolist())
    else:
        lista_uni = ['Todas']
    uni_sel = st.selectbox("Unidade:", lista_uni)

with f2:
    if 'semestre_ref' in df.columns:
        lista_sem = ['Todos'] + sorted(df['semestre_ref'].dropna().astype(str).unique().tolist())
    else:
        lista_sem = ['Todos']
    sem_sel = st.selectbox("Semestre Ref:", lista_sem)

with f3:
    if 'ano_ref' in df.columns:
        anos_validos = sorted([int(x) for x in df['ano_ref'].dropna().unique() if int(x) > 2000])
        ano_padrao = anos_validos[-1] if anos_validos else 2026
        lista_ano = ['Todos'] + anos_validos
        ano_sel = st.selectbox("Ano Ref:", lista_ano, index=lista_ano.index(ano_padrao) if ano_padrao in lista_ano else 0)
    else:
        ano_sel = 'Todos'

with f4:
    if 'data_vencimento' in df.columns and not df['data_vencimento'].dropna().empty:
        venc_validos = df['data_vencimento'].dropna()
        min_venc, max_venc = venc_validos.min().date(), venc_validos.max().date()
        venc_range = st.date_input("Range de Vencimento:", [min_venc, max_venc], format="DD/MM/YYYY")
    else:
        venc_range = []

with f5:
    if 'data_contrato' in df.columns and not df['data_contrato'].dropna().empty:
        contr_validos = df['data_contrato'].dropna()
        min_contr, max_contr = contr_validos.min().date(), contr_validos.max().date()
        contr_range = st.date_input("Range de Data de Contrato:", [min_contr, max_contr], format="DD/MM/YYYY")
    else:
        contr_range = []

# ---------------------------------------------------------
# APLICAÇÃO DOS FILTROS
# ---------------------------------------------------------
df_f = df.copy()

if uni_sel != 'Todas' and 'unidade' in df_f.columns:
    df_f = df_f[df_f['unidade'] == uni_sel]

if sem_sel != 'Todos' and 'semestre_ref' in df_f.columns:
    df_f = df_f[df_f['semestre_ref'] == sem_sel]

if ano_sel != 'Todos' and 'ano_ref' in df_f.columns:
    df_f = df_f[pd.to_numeric(df_f['ano_ref'], errors='coerce') == int(ano_sel)]

if len(venc_range) == 2 and 'data_vencimento' in df_f.columns:
    df_f = df_f[(df_f['data_vencimento'] >= pd.to_datetime(venc_range[0])) & 
                (df_f['data_vencimento'] <= pd.to_datetime(venc_range[1]))]

if len(contr_range) == 2 and 'data_contrato' in df_f.columns:
    df_f = df_f[(df_f['data_contrato'] >= pd.to_datetime(contr_range[0])) & 
                (df_f['data_contrato'] <= pd.to_datetime(contr_range[1]))]

st.divider()

if df_f.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ---------------------------------------------------------
# MÉTRICAS DO FILTRO ATIVO
# ---------------------------------------------------------
total_filtrado = df_f['valor_com_desconto'].sum() if 'valor_com_desconto' in df_f.columns else 0.0
t1, t2 = st.columns([2, 4])
t1.metric("Valor Total (Filtrado)", format_brl(total_filtrado))
t2.metric("Total de Parcelas Selecionadas", f"{len(df_f):,} parcelas".replace(",", "."))

# ---------------------------------------------------------
# MATRIZ FINANCEIRA CONSOLIDADA (PIVOT TABLE)
# ---------------------------------------------------------
if 'unidade' in df_f.columns and 'semestre_ref' in df_f.columns and 'situacao' in df_f.columns:
    pivot = df_f.pivot_table(
        index=['unidade', 'semestre_ref'],
        columns='situacao',
        values='valor_com_desconto',
        aggfunc='sum',
        fill_value=0.0
    )
    pivot['Total Líquido'] = pivot.sum(axis=1)

    st.subheader("Matriz Financeira Consolidada")
    st.dataframe(pivot.style.format(format_brl), use_container_width=True)

# ---------------------------------------------------------
# DETALHAMENTO ANALÍTICO
# ---------------------------------------------------------
with st.expander("Ver Detalhamento Analítico (Com Juros e Multas)"):
    cols_ex = [
        'unidade', 'sacado', 'turma', 'curso', 'data_vencimento', 'data_contrato',
        'valor', 'valor_com_desconto', 'valor_com_juros', 'valor_pago', 'situacao'
    ]
    cols_existentes = [c for c in cols_ex if c in df_f.columns]
    df_exibicao = df_f[cols_existentes].copy()

    if 'data_vencimento' in df_exibicao.columns:
        df_exibicao['data_vencimento'] = df_exibicao['data_vencimento'].dt.strftime('%d/%m/%Y').fillna('-')
    if 'data_contrato' in df_exibicao.columns:
        df_exibicao['data_contrato'] = df_exibicao['data_contrato'].dt.strftime('%d/%m/%Y').fillna('-')

    cols_moeda = ['valor', 'valor_com_desconto', 'valor_com_juros', 'valor_pago']
    for c in cols_moeda:
        if c in df_exibicao.columns:
            df_exibicao[c] = df_exibicao[c].map(format_brl)

    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)