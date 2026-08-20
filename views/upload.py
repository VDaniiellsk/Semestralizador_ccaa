import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from core.database import limpar_banco
from core.rpa import sincronizar_todas_as_unidades_sponte, UNIDADES_DOMINIOS, LOGS_DIR

st.title("Central de Ingestão e Sincronização Sponte")

# ---------------------------------------------------------
# BOTÃO DE 1 CLIQUE COM REGISTRO DE LOG
# ---------------------------------------------------------
st.markdown("### Sincronização Automática Multi-Unidade")
with st.container(border=True):
    st.markdown("**Domínios configurados para extração:**")
    cols_acc = st.columns(3)
    for idx, (uni, dominio) in enumerate(UNIDADES_DOMINIOS.items()):
        cols_acc[idx % 3].caption(f" **{uni}**: `[usuário]{dominio}`")

    st.divider()

    ano_atual = datetime.now().year
    ano_rpa = st.number_input("Defina o Ano Letivo Alvo da Sincronização:", min_value=2024, max_value=2050, value=ano_atual, step=1)

    c_user, c_pwd, c_chk = st.columns([2, 2, 1])
    with c_user:
        sponte_user = st.text_input("Usuário Sponte (apenas antes do @):", placeholder="Ex: Daniel")
    with c_pwd:
        sponte_pass = st.text_input("Senha Geral do Sponte:", type="password")
    with c_chk:
        modo_debug = st.checkbox("Modo Visível (Debug)", value=False)

    if st.button("Sincronizar Todas as 6 Unidades", type="primary", use_container_width=True):
        if not sponte_user or not sponte_pass:
            st.error("Informe o Usuário e a Senha de acesso para executar a extração.")
        else:
            status_area = st.empty()
            
            # Terminal injetado aqui para exibição do log visual em tempo real
            st.markdown("#### Terminal de Execução")
            terminal_area = st.empty() 

            with st.spinner(f"Robô operando a extração do ano letivo {ano_rpa}..."):
                sucesso, msg, path_log = sincronizar_todas_as_unidades_sponte(
                    usuario_prefixo=sponte_user.strip(),
                    senha_padrao=sponte_pass,
                    ano_referencia=ano_rpa,
                    status_callback=lambda txt: status_area.info(txt),
                    log_callback=lambda log_text: terminal_area.code(log_text, language="log"), 
                    modo_visivel=modo_debug
                )
                
                st.session_state['ultimo_log_path'] = str(path_log)
                
                if sucesso:
                    st.success(msg)
                else:
                    st.error(f"Sincronização concluída com inconsistências. Verifique o terminal acima.")

# ---------------------------------------------------------
# PAINEL DE AUDITORIA E LOGS
# ---------------------------------------------------------
st.divider()
st.subheader("Auditoria de Execução (Logs)")

# Corrigido o padrão de busca (rpa_execucao_*.log em vez de sync_*.log)
todos_logs = sorted(LOGS_DIR.glob("rpa_execucao_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
log_ativo_path = None

if 'ultimo_log_path' in st.session_state and Path(st.session_state['ultimo_log_path']).exists():
    log_ativo_path = Path(st.session_state['ultimo_log_path'])
elif todos_logs:
    log_ativo_path = todos_logs[0]

if log_ativo_path and log_ativo_path.exists():
    with open(log_ativo_path, "r", encoding="utf-8") as f:
        conteudo_log = f.read()

    c_info, c_btn = st.columns([3, 1])
    c_info.caption(f"Exibindo log: `{log_ativo_path.name}`")
    c_btn.download_button(
        label="Baixar Arquivo de Log (.log)",
        data=conteudo_log,
        file_name=log_ativo_path.name,
        mime="text/plain",
        use_container_width=True
    )

    with st.expander("Visualizar Histórico Completo do Último Log", expanded=False):
        st.code(conteudo_log, language="log")
else:
    st.info("Nenhum histórico de execução de sincronização registrado ainda.")

# ---------------------------------------------------------
# PAINEL DE SEGURANÇA E RESET
# ---------------------------------------------------------
#with st.sidebar:
#    st.subheader("⚙️ Manutenção do Banco")
#    if st.button("🔴 Forçar Destruição do Banco", type="primary"):
#        if limpar_banco():
#            st.success("Banco SQLite reiniciado com sucesso!")
#            st.rerun()