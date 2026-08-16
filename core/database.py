import sqlite3
from pathlib import Path
import pandas as pd
import logging

DB_PATH = Path("./data/auditoria_financeira.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("RPA_CCAA")

def get_connection():
    return sqlite3.connect(DB_PATH)

def ensure_table_schema(conn, table_name: str, df: pd.DataFrame):
    """Garante que todas as colunas do DataFrame existam na tabela SQLite (migração automática)."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_cols = [row[1] for row in cursor.fetchall()]
    
    if existing_cols:
        colunas_adicionadas = 0
        for col in df.columns:
            if col not in existing_cols:
                col_type = 'REAL' if pd.api.types.is_numeric_dtype(df[col]) else 'TEXT'
                cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN "{col}" {col_type}')
                colunas_adicionadas += 1
                logger.info(f"[Banco de Dados] Coluna inédita identificada e adicionada: '{col}' ({col_type}).")
        if colunas_adicionadas > 0:
            conn.commit()
    else:
        logger.info(f"[Banco de Dados] Tabela '{table_name}' não encontrada. O Pandas criará o esquema do zero.")

def salvar_lote_no_banco(df: pd.DataFrame) -> tuple[bool, str]:
    """Salva o lote de parcelas no SQLite."""
    if df.empty:
        logger.warning("[Banco de Dados] Tentativa de salvar DataFrame vazio bloqueada.")
        return False, "DataFrame está vazio."
    
    conn = get_connection()
    try:
        unidade_atual = df['unidade'].iloc[0] if 'unidade' in df.columns else "Desconhecida"
        logger.info(f"[Banco de Dados] Preparando inserção de {len(df)} registros para a filial '{unidade_atual}'.")
        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recebiveis_auditados'")
        tabela_existe = cursor.fetchone() is not None

        if tabela_existe:
            ensure_table_schema(conn, 'recebiveis_auditados', df)
            # Redundância de segurança unitária (mesmo com o banco sendo limpo no início)
            cursor.execute("DELETE FROM recebiveis_auditados WHERE unidade = ?", (unidade_atual,))
            linhas_deletadas = cursor.rowcount
            conn.commit()
            if linhas_deletadas > 0:
                logger.info(f"[Banco de Dados] {linhas_deletadas} registros anteriores da filial '{unidade_atual}' foram sobrescritos.")

        df.to_sql('recebiveis_auditados', conn, if_exists='append', index=False)
        conn.commit()
        logger.info(f"[Banco de Dados] Operação de I/O concluída. {len(df)} linhas persistidas com sucesso.")
        return True, "Sucesso"
    except Exception as e:
        err_msg = f"Falha de I/O no SQLite: {str(e)}"
        logger.error(f"[Banco de Dados] {err_msg}")
        return False, err_msg
    finally:
        conn.close()

def carregar_dados_auditados() -> pd.DataFrame:
    """Carrega todas as parcelas auditadas do SQLite."""
    conn = get_connection()
    try:
        query = "SELECT * FROM recebiveis_auditados"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception:
        return pd.DataFrame()
    finally:
        conn.close()

def limpar_banco() -> bool:
    """Destrói a tabela de recebíveis para reprocessamento completo."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS recebiveis_auditados")
        conn.commit()
        logger.info("[Banco de Dados] Tabela 'recebiveis_auditados' dropada. O banco foi expurgado com sucesso.")
        return True
    except Exception as e:
        logger.error(f"[Banco de Dados] Erro fatal ao tentar destruir a tabela: {str(e)}")
        return False
    finally:
        conn.close()