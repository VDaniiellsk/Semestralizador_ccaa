import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from core.database import carregar_dados_auditados

def format_brl(val):
    if pd.isna(val):
        return "R$ 0,00"
    return f"R$ {float(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_perc(val):
    if pd.isna(val):
        return "0,00%"
    return f"{float(val):.2f}%".replace(".", ",")

st.title("🎓 Gestão Financeira por Aluno")

df = carregar_dados_auditados()

if df.empty:
    st.warning("Nenhuma base financeira carregada. Vá até a aba 'Upload & Sincronização'.")
    st.stop()

# Higienização
cols_num = ['valor', 'valor_com_desconto', 'valor_com_juros', 'valor_pago']
for c in cols_num:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

date_cols = ['data_vencimento', 'data_contrato', 'data_pagamento', 'data_inicio', 'data_termino']
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], dayfirst=True, errors='coerce')

for c in ['unidade', 'numero_matricula', 'sacado', 'turma', 'curso', 'bolsa', 'situacao']:
    if c not in df.columns:
        df[c] = 'S/I'
    else:
        df[c] = df[c].fillna('S/I').astype(str).str.strip()

# ---------------------------------------------------------
# FILTROS DE PESQUISA
# ---------------------------------------------------------
st.markdown("### Filtros de Pesquisa")
c_busca, c_uni, c_ano, c_sem = st.columns([3, 2, 1.5, 1.5])

with c_busca:
    busca_termo = st.text_input("🔍 Buscar por Nome do Sacado ou Matrícula:", placeholder="Ex: Maria Silva ou 12345")

with c_uni:
    lista_uni = ['Todas as Unidades'] + sorted([u for u in df['unidade'].unique() if u != 'S/I'])
    uni_sel = st.selectbox("Unidade:", lista_uni)

with c_ano:
    if 'ano_ref' in df.columns:
        anos_validos = sorted([int(x) for x in df['ano_ref'].dropna().unique() if int(x) > 2000])
        ano_padrao = anos_validos[-1] if anos_validos else 2026
        lista_ano = ['Todos'] + anos_validos
        ano_sel = st.selectbox("Ano Ref:", lista_ano, index=lista_ano.index(ano_padrao) if ano_padrao in lista_ano else 0)
    else:
        ano_sel = 'Todos'

with c_sem:
    lista_sem = ['Todos os Semestres', '1º Semestre', '2º Semestre']
    sem_sel = st.selectbox("Semestre:", lista_sem)

df_f = df.copy()

if busca_termo:
    termo_limpo = busca_termo.strip().lower()
    mascara_sacado = df_f['sacado'].str.lower().str.contains(termo_limpo, na=False)
    mascara_mat = df_f['numero_matricula'].str.lower().str.contains(termo_limpo, na=False)
    df_f = df_f[mascara_sacado | mascara_mat]

if uni_sel != 'Todas as Unidades':
    df_f = df_f[df_f['unidade'] == uni_sel]

if ano_sel != 'Todos' and 'ano_ref' in df_f.columns:
    df_f = df_f[pd.to_numeric(df_f['ano_ref'], errors='coerce') == int(ano_sel)]

if sem_sel == '1º Semestre' and 'semestre_ref' in df_f.columns:
    df_f = df_f[df_f['semestre_ref'].astype(str).str.startswith('1/')]
elif sem_sel == '2º Semestre' and 'semestre_ref' in df_f.columns:
    df_f = df_f[df_f['semestre_ref'].astype(str).str.startswith('2/')]

if df_f.empty:
    st.info("Nenhum registro encontrado para os filtros aplicados.")
    st.stop()

# ---------------------------------------------------------
# CONSOLIDAÇÃO VETORIZADA POR ALUNO
# ---------------------------------------------------------
cols_grp = ['unidade', 'numero_matricula', 'sacado', 'turma', 'curso']
hoje = pd.Timestamp(datetime.now().date())

# Identificação de parcelas quitadas baseada na coluna oficial do Sponte
is_quitada = df_f['situacao'].str.lower().str.contains('quitad|receb|pag|liquid', na=False)
is_pendente = ~is_quitada
is_vencida = is_pendente & (df_f['data_vencimento'] <= hoje)

# Se está quitada, o valor considerado pago ou baixado (bolsa 100%) é o valor com desconto
df_f['valor_pago_calc'] = np.where(is_quitada, df_f['valor_com_desconto'], 0.0)
df_f['valor_pendente_calc'] = np.where(is_pendente, df_f['valor_com_desconto'], 0.0)
df_f['is_vencida_flag'] = np.where(is_vencida, 1, 0)
df_f['valor_vencido_calc'] = np.where(is_vencida, df_f['valor_com_desconto'], 0.0)

def extrair_bolsas_agrupadas(series):
    validas = [str(x).strip() for x in series.unique() if str(x).strip() not in ['S/I', 'nan', 'None', '', '0', '0.0', '-']]
    return ", ".join(validas) if validas else 'S/I'

agg_dict = {
    'valor': ['count', 'sum'],
    'valor_com_desconto': 'sum',
    'valor_pago_calc': 'sum',
    'valor_pendente_calc': 'sum',
    'valor_vencido_calc': 'sum',
    'is_vencida_flag': 'sum',
    'bolsa': extrair_bolsas_agrupadas
}

df_alunos = df_f.groupby(cols_grp, as_index=False, dropna=False).agg(agg_dict)

df_alunos.columns = [
    'unidade', 'numero_matricula', 'sacado', 'turma', 'curso',
    'total_parcelas', 'valor_nominal', 'valor_previsto',
    'valor_pago', 'valor_pendente', 'valor_vencido', 'parcelas_vencidas', 'bolsa'
]

# Cálculo de Descontos
def calcular_descontos_linha(row):
    nom = row['valor_nominal']
    prev = row['valor_previsto']
    desc = nom - prev if nom >= prev else 0.0
    perc = (desc / nom * 100.0) if nom > 0 else 0.0
    return pd.Series({'valor_desconto': desc, 'perc_desconto': perc})

descontos_df = df_alunos.apply(calcular_descontos_linha, axis=1)
df_alunos['valor_desconto'] = descontos_df['valor_desconto']
df_alunos['perc_desconto'] = descontos_df['perc_desconto']

# Aluno só é inadimplente se tiver parcelas vencidas no passado
df_alunos['status_financeiro'] = df_alunos['parcelas_vencidas'].apply(
    lambda x: '🟢 Em Dia' if x == 0 else '🔴 Inadimplente'
)

# Filtro por Status
c_filtro_status, _ = st.columns([2, 4])
with c_filtro_status:
    status_sel = st.radio("Status do Aluno:", ["Todos", "Apenas Inadimplentes", "Apenas Em Dia"], horizontal=True)

if status_sel == "Apenas Inadimplentes":
    df_alunos = df_alunos[df_alunos['status_financeiro'] == '🔴 Inadimplente']
elif status_sel == "Apenas Em Dia":
    df_alunos = df_alunos[df_alunos['status_financeiro'] == '🟢 Em Dia']

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
total_alunos_unicos = len(df_alunos)
total_nominal_geral = df_alunos['valor_nominal'].sum()
total_previsto_geral = df_alunos['valor_previsto'].sum()
total_desconto_geral = df_alunos['valor_desconto'].sum()
perc_desconto_medio = (total_desconto_geral / total_nominal_geral * 100) if total_nominal_geral > 0 else 0.0

total_recebido_geral = df_alunos['valor_pago'].sum()
total_pendente_geral = df_alunos['valor_pendente'].sum()
total_inadimplentes = (df_alunos['status_financeiro'] == '🔴 Inadimplente').sum()

st.divider()
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Alunos Encontrados", f"{total_alunos_unicos:,}".replace(",", "."))
k2.metric("Receita Prevista (Líq)", format_brl(total_previsto_geral), delta=f"{format_perc(perc_desconto_medio)} desc. médio", delta_color="off")
k3.metric("Descontos Concedidos", format_brl(total_desconto_geral))
k4.metric("Total Recebido", format_brl(total_recebido_geral))
k5.metric("Total Pendente", format_brl(total_pendente_geral), delta=f"{total_inadimplentes} inadimplentes", delta_color="inverse")

st.divider()

# ---------------------------------------------------------
# TABELA RESUMO
# ---------------------------------------------------------
st.subheader("Resumo por Aluno")

df_alunos_exib = df_alunos.copy()
df_alunos_exib['valor_nominal'] = df_alunos_exib['valor_nominal'].map(format_brl)
df_alunos_exib['valor_previsto'] = df_alunos_exib['valor_previsto'].map(format_brl)
df_alunos_exib['perc_desconto'] = df_alunos_exib['perc_desconto'].map(format_perc)
df_alunos_exib['valor_pago'] = df_alunos_exib['valor_pago'].map(format_brl)
df_alunos_exib['valor_pendente'] = df_alunos_exib['valor_pendente'].map(format_brl)

st.dataframe(
    df_alunos_exib.rename(columns={
        'unidade': 'Unidade',
        'numero_matricula': 'Matrícula',
        'sacado': 'Aluno / Sacado',
        'bolsa': 'Bolsa / Convênio',
        'turma': 'Turma',
        'curso': 'Curso',
        'total_parcelas': 'Total Parc.',
        'valor_nominal': 'Nominal Total',
        'valor_previsto': 'Previsto (Líq)',
        'perc_desconto': '% Desconto',
        'valor_pago': 'Total Pago',
        'valor_pendente': 'Total Pendente',
        'parcelas_vencidas': 'Parc. Vencidas',
        'status_financeiro': 'Status'
    }),
    use_container_width=True,
    hide_index=True
)