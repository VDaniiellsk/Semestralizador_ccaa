import streamlit as st

st.title("Manual de Operações e Governança")
st.markdown("Documentação oficial das regras de negócio, limites de extração e guias de leitura do sistema.")

st.divider()

# ---------------------------------------------------------
# NAVEGAÇÃO POR ABAS
# ---------------------------------------------------------
tab_sync, tab_dash, tab_matriz, tab_alunos = st.tabs([
    "• Sincronização e Banco", 
    "• Dashboard Estratégico", 
    "• Matriz de Valores", 
    "• Gestão por Aluno"
])

# =========================================================
# ABA 1: SINCRONIZAÇÃO
# =========================================================
with tab_sync:
    st.header("1. Central de Ingestão (RPA)")
    st.markdown("""
    A sincronização é o motor do sistema. Ela acessa o Sponte, baixa os relatórios brutos e transforma os dados em inteligência.
    
    **Como operar:**
    1. Insira o prefixo do seu usuário (ex: se for `Daniel@ccaa`, digite apenas `Daniel`).
    2. Insira a senha.
    3. Defina o **Ano Letivo**. 
    4. Clique em Sincronizar. O processo leva em média 5 a 6 minutos para as 6 filiais.
    """)
    
    st.warning("Podem haver divergencias devido a erros operacionais e do Sponte. Se notar inconsistências, rode a sincronização novamente.")
    st.markdown("""
    * **O banco de dados da aplicação não guarda histórico de longo prazo.** 
    * Toda vez que você inicia uma nova sincronização, o sistema **destrói** o banco de dados anterior para garantir que não haja duplicidade de dados corrompidos.
    * O sistema faz um expurgo absoluto: qualquer parcela que não pertença ao Ano Letivo selecionado (baseado na Data de Início do contrato) é **deletada**.
    """)

# =========================================================
# ABA 2: DASHBOARD
# =========================================================
with tab_dash:
    st.header("2. Leitura do Dashboard")
    st.markdown("""
    O Dashboard foi projetado para expor a fissura entre a expectativa (o que a escola deveria ganhar) e a realidade (o que realmente caiu na conta).
    
    ### Indicadores Principais (KPIs)
    * **Volume Faturado Previsto:** O valor total (já com descontos aplicados) de todos os contratos ativos no período filtrado.
    * **Caixa Real (Efetivado):** O dinheiro real. Só conta aqui se a parcela estiver estritamente com o status `Quitada` no Sponte.
    * **Passivo Vencido:** Dívidas abertas. Soma das parcelas cujo status é diferente de `Quitada` e cuja `DataVencimento` já passou.
    * **Taxa de Calote:** A representação percentual do Passivo Vencido sobre o Volume Faturado.
    
    ### Análises Gráficas
    * **Curva de Fluxo de Caixa:** Compara a linha azul (quando o dinheiro *deveria* entrar) com a linha verde (quando ele *realmente* entrou). Se a azul estiver muito acima da verde, a escola está financiando o aluno.
    * **Mapa de Risco (Calote por Curso):** Expõe quais modalidades de ensino concentram o maior volume de inadimplência em reais (R$). Útil para focar esforços de cobrança.
    """)

# =========================================================
# ABA 3: MATRIZ DE VALORES
# =========================================================
with tab_matriz:
    st.header("3. Matriz Financeira")
    st.markdown("""
    Esta tela é focada na auditoria macro e no cruzamento de dados.
    
    **Como utilizar:**
    * Use esta visão para cruzar **Unidades vs Semestres vs Situação**.
    * É a ferramenta ideal para a controladoria identificar o montante exato de "Acordos", "Cancelamentos" e "Inadimplência" separado por cada filial em um formato de tabela dinâmica (Pivot Table).
    * Você pode usar o filtro de range de datas para isolar o faturamento de uma semana específica.
    """)

# =========================================================
# ABA 4: GESTÃO POR ALUNO
# =========================================================
with tab_alunos:
    st.header("4. Auditoria Micro (Gestão por Aluno)")
    st.markdown("""
    Visão cirúrgica para atendimento e cobrança. Esta tela condensa todas as dezenas de parcelas de um aluno em uma única linha de análise.
    
    **Regras de Negócio Inegociáveis:**
    1. **Bolsistas:** Alunos com situação `Quitada` e Valor Pago igual a R$ 0,00 são classificados automaticamente pelo motor ETL como `Bolsista`.
    2. **Status Financeiro:** 
        * 🔴 **Inadimplente:** O aluno possui pelo menos UMA parcela vencida e não paga no passado.
        * 🟢 **Em Dia:** O aluno pagou tudo até a data de hoje (mesmo que tenha dezenas de parcelas a vencer no futuro).
    3. **Desconto Médio:** O sistema não exibe o desconto bruto, pois as turmas possuem valores divergentes. A tela foca no valor final líquido previsto pelo contrato.
    """)
    
    st.info("💡 Dica de Operação: Use a barra de busca (🔍) para digitar o nome ou a matrícula e auditar rapidamente por que um aluno específico está classificado como inadimplente.")