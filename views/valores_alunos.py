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

st.title("Financeira por Aluno")

df = carregar_dados_auditados()

if df.empty:
    st.warning("Nenhuma base financeira carregada. Vá até a aba 'Upload & Sincronização'.")
    st.stop()

# ---------------------------------------------------------
# HIGIENIZAÇÃO (ALINHADA AO NOVO ESQUEMA DO DB)
# ---------------------------------------------------------
cols_num = ['ValorComDesconto', 'ValorComJuros', 'ValorPago']
for c in cols_num:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

date_cols = ['DataVencimento', 'DataPagamento', 'DataInicio', 'DataTermino']
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

for c in ['unidade', 'NumeroMatricula', 'Sacado', 'Turma', 'Curso', 'Bolsa', 'Situacao', 'SemestreReferencia']:
    if c not in df.columns:
        df[c] = 'S/I'
    else:
        df[c] = df[c].fillna('S/I').astype(str).str.strip()

# Engenharia de Feature: Reconstrução do Ano Letivo
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
c_busca, c_uni, c_ano, c_sem = st.columns([3, 2, 1.5, 1.5])

with c_busca:
    busca_termo = st.text_input("🔍 Buscar por Nome do Sacado ou Matrícula:", placeholder="Ex: Maria Silva ou 12345")

with c_uni:
    lista_uni = ['Todas as Unidades'] + sorted([u for u in df['unidade'].unique() if u != 'S/I'])
    uni_sel = st.selectbox("Unidade:", lista_uni)

with c_ano:
    anos_validos = sorted([int(x) for x in df['AnoLetivo'].dropna().unique() if int(x) > 2000])
    ano_padrao = anos_validos[-1] if anos_validos else 2026
    lista_ano = ['Todos'] + anos_validos
    ano_sel = st.selectbox("Ano Letivo:", lista_ano, index=lista_ano.index(ano_padrao) if ano_padrao in lista_ano else 0)

with c_sem:
    lista_sem = ['Todos os Semestres', '1º Semestre', '2º Semestre']
    sem_sel = st.selectbox("Semestre:", lista_sem)

df_f = df.copy()

if busca_termo:
    termo_limpo = busca_termo.strip().lower()
    mascara_sacado = df_f['Sacado'].str.lower().str.contains(termo_limpo, na=False)
    mascara_mat = df_f['NumeroMatricula'].str.lower().str.contains(termo_limpo, na=False)
    df_f = df_f[mascara_sacado | mascara_mat]

if uni_sel != 'Todas as Unidades':
    df_f = df_f[df_f['unidade'] == uni_sel]

if ano_sel != 'Todos':
    df_f = df_f[df_f['AnoLetivo'] == int(ano_sel)]

if sem_sel != 'Todos os Semestres':
    df_f = df_f[df_f['SemestreReferencia'] == sem_sel]

if df_f.empty:
    st.info("Nenhum registro encontrado para os filtros aplicados.")
    st.stop()

# ---------------------------------------------------------
# CONSOLIDAÇÃO VETORIZADA POR ALUNO
# ---------------------------------------------------------
cols_grp = ['unidade', 'NumeroMatricula', 'Sacado', 'Turma', 'Curso']
hoje = pd.Timestamp(datetime.now().date())

# Atenção: 'Situacao' sem acento conforme correção prévia no ETL
df_f['is_quitada'] = df_f['Situacao'].str.lower().str.contains('quitad|liquid|pag|receb', na=False)
df_f['is_pendente'] = ~df_f['is_quitada']
df_f['is_vencida'] = df_f['is_pendente'] & (df_f['DataVencimento'] <= hoje)

df_f['valor_pago_calc'] = np.where(df_f['is_quitada'], df_f['ValorPago'], 0.0)
df_f['valor_pendente_calc'] = np.where(df_f['is_pendente'], df_f['ValorComDesconto'], 0.0)
df_f['valor_vencido_calc'] = np.where(df_f['is_vencida'], df_f['ValorComDesconto'], 0.0)
df_f['is_vencida_flag'] = np.where(df_f['is_vencida'], 1, 0)

def extrair_bolsas_agrupadas(series):
    validas = [str(x).strip() for x in series.unique() if str(x).strip() not in ['S/I', 'nan', 'None', '', '0', '0.0', '-']]
    return ", ".join(validas) if validas else 'S/I'

agg_dict = {
    'ValorComDesconto': 'sum',
    'valor_pago_calc': 'sum',
    'valor_pendente_calc': 'sum',
    'valor_vencido_calc': 'sum',
    'is_vencida_flag': 'sum',
    'Bolsa': extrair_bolsas_agrupadas
}

df_alunos = df_f.groupby(cols_grp, as_index=False, dropna=False).agg(agg_dict)
# Contagem de parcelas
parcelas_count = df_f.groupby(cols_grp, as_index=False, dropna=False)['NumeroParcela'].count()
df_alunos = pd.merge(df_alunos, parcelas_count, on=cols_grp, how='left')

df_alunos.rename(columns={
    'unidade': 'unidade',
    'NumeroMatricula': 'numero_matricula',
    'Sacado': 'sacado',
    'Turma': 'turma',
    'Curso': 'curso',
    'ValorComDesconto': 'valor_previsto',
    'valor_pago_calc': 'valor_pago',
    'valor_pendente_calc': 'valor_pendente',
    'valor_vencido_calc': 'valor_vencido',
    'is_vencida_flag': 'parcelas_vencidas',
    'Bolsa': 'bolsa',
    'NumeroParcela': 'total_parcelas'
}, inplace=True)

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
total_previsto_geral = df_alunos['valor_previsto'].sum()
total_recebido_geral = df_alunos['valor_pago'].sum()
total_pendente_geral = df_alunos['valor_pendente'].sum()
total_inadimplentes = (df_alunos['status_financeiro'] == '🔴 Inadimplente').sum()

st.divider()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Alunos Encontrados", f"{total_alunos_unicos:,}".replace(",", "."))
k2.metric("Receita Prevista (Líq)", format_brl(total_previsto_geral))
k3.metric("Total Recebido", format_brl(total_recebido_geral))
k4.metric("Total Pendente", format_brl(total_pendente_geral), delta=f"{total_inadimplentes} inadimplentes", delta_color="inverse")

st.divider()

# ---------------------------------------------------------
# TABELA RESUMO
# ---------------------------------------------------------
st.subheader("Resumo por Aluno")

df_alunos_exib = df_alunos.copy()
df_alunos_exib['valor_previsto'] = df_alunos_exib['valor_previsto'].map(format_brl)
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
        'valor_previsto': 'Previsto (Líq)',
        'valor_pago': 'Total Pago',
        'valor_pendente': 'Total Pendente',
        'parcelas_vencidas': 'Parc. Vencidas',
        'status_financeiro': 'Status'
    }),
    use_container_width=True,
    hide_index=True
)