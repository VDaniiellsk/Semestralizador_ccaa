import os
import streamlit as st

LOGO_PATH = os.path.join("src", "CCAA_logo_(2020).svg")

# Configuração da página com o logo como favicon se o arquivo existir
st.set_page_config(
    page_title="Gestão Financeira CCAA",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização visual refinada
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

# 1. Integração nativa do logo no topo do menu de navegação
if os.path.exists(LOGO_PATH):
    try:
        st.logo(LOGO_PATH, icon_image=LOGO_PATH)
    except Exception:
        pass
    # Exibição de destaque no topo da barra lateral
    st.sidebar.image(LOGO_PATH, use_container_width=True)
    st.sidebar.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# 2. Definição das páginas e navegação
pages = {

    "Análises e Gestão": [
        st.Page("views/dashboard.py", title="Dashboard Geral", icon=":material/dashboard:"),
        st.Page("views/valores_semestrais.py", title="Matriz de Valores", icon=":material/calendar_today:"),
        st.Page("views/valores_alunos.py", title="Valores por Alunos", icon=":material/school:")
    ],
        "Configuração": [
        st.Page("views/upload.py", title="Upload & Sincronização", icon=":material/upload:")
    ]
}

pg = st.navigation(pages)
pg.run()