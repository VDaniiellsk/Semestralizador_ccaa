import os
import streamlit as st

# =====================================================================
# BARREIRA DE ACESSO (SESSION STATE)
# =====================================================================
def check_password():
    """Valida a senha e gerencia o estado da sessão."""
    def password_entered():
        usuario = st.session_state["username_input"].strip()
        senha_digitada = st.session_state["password_input"]
        
        # Verifica no secrets.toml se o usuário existe e a senha confere
        if "passwords" in st.secrets and usuario in st.secrets["passwords"] and senha_digitada == st.secrets["passwords"][usuario]:
            st.session_state["password_correct"] = True
            st.session_state["usuario_logado"] = usuario
            del st.session_state["password_input"]  # Limpa a senha da memória
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Primeira renderização: Tela de Login
        st.title("Acesso Restrito: Auditoria CCAA")
        st.text_input("Usuário", key="username_input")
        st.text_input("Senha", type="password", key="password_input")
        st.button("Entrar", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        # Falha de Autenticação
        st.title("Acesso Restrito: Auditoria CCAA")
        st.text_input("Usuário", key="username_input")
        st.text_input("Senha", type="password", key="password_input")
        st.button("Entrar", on_click=password_entered)
        st.error("Credenciais inválidas ou usuário inexistente.")
        return False
    
    else:
        # Autenticação bem-sucedida
        return True

# A execução morre aqui se a senha não for validada
if not check_password():
    st.stop()


# =====================================================================
# CONFIGURAÇÃO GLOBAL
# =====================================================================
LOGO_PATH = os.path.join("src", "CCAA_logo_(2020).svg")

st.set_page_config(
    page_title="Gestão Financeira CCAA",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        stMetric { 
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
        }
        [data-testid="stSidebarHeader"] img {
            max-height: 50px;
            object-fit: contain;
        }
    </style>
""", unsafe_allow_html=True)

if os.path.exists(LOGO_PATH):
    try:
        # Este é o ÚNICO comando que deve existir. Ele coloca a logo no topo.
        st.logo(LOGO_PATH, icon_image=LOGO_PATH)
    except Exception:
        pass
    
# RECUPERA O USUÁRIO E SEGUE O FLUXO
usuario_atual = st.session_state.get("usuario_logado", "").lower()


# =====================================================================
# [RBAC] ROLE-BASED ACCESS CONTROL DINÂMICO
# =====================================================================
# Recupera o usuário real da sessão em vez de usar hardcode
usuario_atual = st.session_state.get("usuario_logado", "").lower()

# Define a hierarquia. Ex: Apenas 'daniel' e 'diretoria' são Admins.
admins_autorizados = ["daniel", "Jobson","Leonardo"]
papel_usuario = "Admin" if usuario_atual in admins_autorizados else "Viewer"

st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.success(f"Logado como: {usuario_atual.title()} ({papel_usuario})")
if st.sidebar.button("Sair"):
    st.session_state.clear()
    st.rerun()

# =====================================================================
# DEFINIÇÃO DE ROTAS E RENDERIZAÇÃO
# =====================================================================
pages = {
    "Análises e Gestão": [
        st.Page("views/dashboard.py", title="Dashboard Geral", icon=":material/dashboard:"),
        st.Page("views/valores_semestrais.py", title="Matriz de Valores", icon=":material/calendar_today:"),
        st.Page("views/valores_alunos.py", title="Valores por Alunos", icon=":material/school:"),
        st.Page("views/manual.py", title="Manual de Operação", icon=":material/book:")
    ]
}

# A injeção das páginas de controle de banco de dados só ocorre para Admins reais
if papel_usuario == "Admin":
    pages["Administração (Acesso Restrito)"] = [
        st.Page("views/upload.py", title="Upload & Sincronização", icon=":material/upload:")
    ]

pg = st.navigation(pages)
pg.run()