import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from core.database import carregar_dados_auditados

def format_brl(val):
    if pd.isna(val):
        return "R$ 0,00"
    return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("Matriz de Valores")

df = carregar_dados_auditados()

if df.empty:
    st.warning("Nenhuma base financeira carregada. Vá até a aba 'Upload & Sincronização'.")
    st.stop()

# ---------------------------------------------------------
# HIGIENIZAÇÃO E ENGENHARIA DE FEATURES
# ---------------------------------------------------------
cols_num = ['ValorComDesconto', 'ValorComJuros', 'ValorPago']
for c in cols_num:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

# Remoção do dayfirst=True para respeitar o padrão ISO do banco
date_cols = ['DataVencimento', 'DataPagamento', 'DataInicio', 'DataTermino']
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

# Reconstrução do Ano Letivo
if 'DataInicio' in df.columns:
    df['MesInicio'] = df['DataInicio'].dt.month.fillna(1)
    df['AnoInicio'] = df['DataInicio'].dt.year.fillna(datetime.now().year)
    df['AnoLetivo'] = np.where(df['MesInicio'] >= 11, df['AnoInicio'] + 1, df['AnoInicio'])
else:
    df['AnoLetivo'] = datetime.now().year

# ---------------------------------------------------------
# FILTROS DE PESQUISA
# ---------------------------------------------------------
st.markdown("### Filtros de Pesquisa")
f1, f2, f3 = st.columns(3)
f4, f5 = st.columns(2)

with f1:
    lista_uni = ['Todas'] + sorted(df['unidade'].dropna().unique().tolist()) if 'unidade' in df.columns else ['Todas']
    uni_sel = st.selectbox("Unidade:", lista_uni)

with f2:
    lista_sem = ['Todos'] + sorted(df['SemestreReferencia'].dropna().astype(str).unique().tolist()) if 'SemestreReferencia' in df.columns else ['Todos']
    sem_sel = st.selectbox("Semestre Ref:", lista_sem)

with f3:
    anos_validos = sorted([int(x) for x in df['AnoLetivo'].dropna().unique() if int(x) > 2000])
    ano_padrao = anos_validos[-1] if anos_validos else 2026
    lista_ano = ['Todos'] + anos_validos
    ano_sel = st.selectbox("Ano Letivo:", lista_ano, index=lista_ano.index(ano_padrao) if ano_padrao in lista_ano else 0)

with f4:
    if 'DataVencimento' in df.columns and not df['DataVencimento'].dropna().empty:
        venc_validos = df['DataVencimento'].dropna()
        min_venc, max_venc = venc_validos.min().date(), venc_validos.max().date()
        venc_range = st.date_input("Range de Vencimento:", [min_venc, max_venc], format="DD/MM/YYYY")
    else:
        venc_range = []

with f5:
    if 'DataInicio' in df.columns and not df['DataInicio'].dropna().empty:
        contr_validos = df['DataInicio'].dropna()
        min_contr, max_contr = contr_validos.min().date(), contr_validos.max().date()
        contr_range = st.date_input("Range de Data do Contrato (Início):", [min_contr, max_contr], format="DD/MM/YYYY")
    else:
        contr_range = []

# ---------------------------------------------------------
# APLICAÇÃO DOS FILTROS
# ---------------------------------------------------------
df_f = df.copy()

if uni_sel != 'Todas' and 'unidade' in df_f.columns:
    df_f = df_f[df_f['unidade'] == uni_sel]

if sem_sel != 'Todos' and 'SemestreReferencia' in df_f.columns:
    df_f = df_f[df_f['SemestreReferencia'] == sem_sel]

if ano_sel != 'Todos':
    df_f = df_f[df_f['AnoLetivo'] == int(ano_sel)]

if len(venc_range) == 2 and 'DataVencimento' in df_f.columns:
    df_f = df_f[(df_f['DataVencimento'] >= pd.to_datetime(venc_range[0])) & 
                (df_f['DataVencimento'] <= pd.to_datetime(venc_range[1]))]

if len(contr_range) == 2 and 'DataInicio' in df_f.columns:
    df_f = df_f[(df_f['DataInicio'] >= pd.to_datetime(contr_range[0])) & 
                (df_f['DataInicio'] <= pd.to_datetime(contr_range[1]))]

st.divider()

if df_f.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ---------------------------------------------------------
# MÉTRICAS DO FILTRO ATIVO
# ---------------------------------------------------------
total_filtrado = df_f['ValorComDesconto'].sum() if 'ValorComDesconto' in df_f.columns else 0.0
t1, t2 = st.columns([2, 4])
t1.metric("Valor Total (Filtrado)", format_brl(total_filtrado))
t2.metric("Total de Parcelas Selecionadas", f"{len(df_f):,} parcelas".replace(",", "."))

# ---------------------------------------------------------
# MATRIZ FINANCEIRA CONSOLIDADA (PIVOT TABLE)
# ---------------------------------------------------------
if 'unidade' in df_f.columns and 'SemestreReferencia' in df_f.columns and 'Situacao' in df_f.columns:
    pivot = df_f.pivot_table(
        index=['unidade', 'SemestreReferencia'],
        columns='Situacao',
        values='ValorComDesconto',
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
        'unidade', 'Sacado', 'Turma', 'Curso', 'DataVencimento', 'DataInicio',
        'ValorComDesconto', 'ValorComJuros', 'ValorPago', 'Situacao'
    ]
    cols_existentes = [c for c in cols_ex if c in df_f.columns]
    df_exibicao = df_f[cols_existentes].copy()

    if 'DataVencimento' in df_exibicao.columns:
        df_exibicao['DataVencimento'] = df_exibicao['DataVencimento'].dt.strftime('%d/%m/%Y').fillna('-')
    if 'DataInicio' in df_exibicao.columns:
        df_exibicao['DataInicio'] = df_exibicao['DataInicio'].dt.strftime('%d/%m/%Y').fillna('-')

    cols_moeda = ['ValorComDesconto', 'ValorComJuros', 'ValorPago']
    for c in cols_moeda:
        if c in df_exibicao.columns:
            df_exibicao[c] = df_exibicao[c].map(format_brl)

    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)