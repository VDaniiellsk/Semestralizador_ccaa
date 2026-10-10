"""Disponibiliza as orientações de operação dentro do aplicativo.

As orientações acompanham a carga atual, os indicadores e as limitações
das estimativas. README e docs/ARQUITETURA.md detalham a manutenção."""
import streamlit as st

st.title("Manual de Operações e Governança")

st.info("Em Devedores Gerais, consulte alunos com parcelas vencidas por ano e semestre. Em Turmas e Cursos, consulte quantidades, listas de alunos e valores; use os controles de agrupamento e ordenação para reorganizar a análise.")
st.caption("Os filtros financeiros permitem buscar aluno ou matrícula e selecionar unidade, ano, semestre, curso, estágio, turma e situação da parcela. Parcelas canceladas não geram dívida. A base representa a última sincronização; outro ano requer nova carga.")
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
    A sincronização extrai e trata os relatórios atuais do Sponte. Cada linha financeira é preservada no banco, com aluno, turma, datas e valores. O código do contrato não é necessário para esta carga. Parcelas sem turma ou datas do contrato são preservadas; classificações indisponíveis aparecem como não informadas. Valores são arredondados para centavos e o estágio é deduzido pelo nome da turma.
    
    **Como operar:**
    1. Insira o prefixo do seu usuário (ex: se for `Daniel@ccaa`, digite apenas `Daniel`).
    2. Insira a senha.
    3. Defina o **Ano Letivo**. 
    4. Clique em Sincronizar. Aguarde a conclusão e confira a mensagem final; o tempo depende do ERP e da conexão.
    """)
    
    st.warning("Se notar divergências, confira o relatório exportado e o log antes de repetir a sincronização.")
    st.markdown("""
    * **O banco de dados da aplicação não guarda histórico de longo prazo.** 
    * A sincronização substitui a carga do banco relacional somente depois de extrair e validar todas as unidades. Se houver falha, a carga anterior é preservada. A base legada permanece separada.
    * Na extração atual, o ano é filtrado pelo nome da turma; quando ele não está informado no nome, utiliza-se o ano selecionado. Nos painéis, o ano do nome da turma também tem prioridade; sem ele, utiliza-se a data de início, com novembro e dezembro associados ao ano seguinte.
    """)

# =========================================================
# ABA 2: DASHBOARD
# =========================================================
with tab_dash:
    st.header("2. Leitura do Dashboard")
    st.markdown("""
    O dashboard compara os valores previstos com os recebimentos registrados e destaca as parcelas vencidas.
    
    ### Indicadores Principais (KPIs)
    * **Volume Faturado Previsto:** A soma dos valores com desconto das parcelas não canceladas no recorte selecionado.
    * **Caixa Real (Efetivado):** Soma do valor pago das parcelas com situação reconhecida como paga; parcelas pendentes e canceladas não entram nesse indicador.
    * **Passivo Vencido:** Soma do valor com desconto das parcelas pendentes com vencimento menor ou igual à data atual.
    * **Taxa de Calote:** A representação percentual do Passivo Vencido sobre o Volume Faturado.
    
    ### Análises Gráficas
    * **Curva de Fluxo de Caixa:** Compara a linha azul (quando o dinheiro *deveria* entrar) com a linha verde (quando ele *realmente* entrou). As diferenças ajudam a conferir o planejamento e os recebimentos registrados.
    * **Mapa de Risco (Calote por Curso):** Mostra quais modalidades de ensino concentram o maior volume de inadimplência em reais (R$). Útil para focar esforços de cobrança.
    """)

# =========================================================
# ABA 3: MATRIZ DE VALORES
# =========================================================
with tab_matriz:
    st.header("3. Matriz Financeira")
    st.markdown("""
    Esta tela reúne os valores financeiros e permite conferir os resultados por unidade e semestre.
    
    **Como utilizar:**
    * Use esta visão para cruzar **Unidades vs Semestres vs Situação**.
    * Os agrupamentos exibem uma tabela por combinação selecionada, com os totais calculados a partir das parcelas de origem.
    * Use os filtros de datas disponíveis para delimitar a consulta.
    """)

# =========================================================
# ABA 4: GESTÃO POR ALUNO
# =========================================================
with tab_alunos:
    st.header("4. Auditoria Micro (Gestão por Aluno)")
    st.markdown("""
    Esta tela resume as parcelas por aluno e permite abrir os registros para conferência. A identificação considera unidade e matrícula.
    
    **Como interpretar os resultados:**
    1. **Bolsistas:** Quando a bolsa está ausente no ERP, parcelas `Quitadas` com valor pago de R$ 0,00 recebem a classificação operacional `Bolsista`. Confira casos divergentes no relatório de origem.
    2. **Status Financeiro:** 
        * 🔴 **Inadimplente:** O aluno possui pelo menos uma parcela não paga com vencimento menor ou igual a hoje.
        * 🟢 **Em Dia:** Não há parcelas vencidas e pendentes na base de referência consultada; parcelas futuras não geram inadimplência.
    3. **Bolsa e desconto estimado:** A informação do ERP tem prioridade. Quando há uma correspondência única com a referência privada de preços, o sistema mostra o percentual estimado; ele não confirma o nome de um convênio. Resultados ambíguos ou dados incompletos permanecem sem estimativa conclusiva.
    """)
    
    st.info("💡 Dica de Operação: Use a barra de busca (🔍) para digitar o nome ou a matrícula e auditar rapidamente por que um aluno específico está classificado como inadimplente.")