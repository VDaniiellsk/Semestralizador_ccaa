"""Configuração privada das unidades, compartilhada pelo ETL e pelo RPA."""
import streamlit as st


def carregar_unidades():
    try:
        registros = st.secrets["unidades"]
    except (KeyError, FileNotFoundError):
        raise RuntimeError(
            "Configure as unidades no secrets.toml ou nos secrets da hospedagem."
        ) from None
    if not isinstance(registros, (list, tuple)) or not registros:
        raise RuntimeError("A configuração privada de unidades deve conter uma lista.")
    dominios = {}
    for registro in registros:
        nome = registro.get("nome")
        dominio = registro.get("dominio")
        if (not isinstance(nome, str) or not nome.strip()
                or not isinstance(dominio, str) or not dominio.startswith("@")):
            raise RuntimeError("Uma unidade possui configuração privada inválida.")
        if nome in dominios:
            raise RuntimeError("Há uma unidade duplicada na configuração privada.")
        dominios[nome] = dominio
    return dominios


UNIDADES_DOMINIOS = carregar_unidades()
UNIDADES_VALIDAS = list(UNIDADES_DOMINIOS)
