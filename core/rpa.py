import os
import time
import logging
import traceback
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, FrameLocator
import pandas as pd
from core.etl import process_contas_receber
from core.database import salvar_lote_no_banco, limpar_banco

DOWNLOAD_DIR = Path("./temp_downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)
LOGS_DIR = Path("./logs")
LOGS_DIR.mkdir(exist_ok=True)

URL_CONTAS_RECEBER = "https://www.sponteweb.com.br/SPRel/Financeiro/ContasReceber.aspx"

from core.config import UNIDADES_DOMINIOS

# =====================================================================
# HANDLER DE LOG PARA STREAMLIT
# =====================================================================
class StreamlitUIHandler(logging.Handler):
    """Captura os logs do Python e dispara para a interface do Streamlit em tempo real."""
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.log_text = ""

    def emit(self, record):
        msg = self.format(record)
        self.log_text += msg + "\n"
        if self.callback:
            self.callback(self.log_text)

def configurar_logger_execucao(ui_log_callback=None) -> tuple[logging.Logger, Path]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = LOGS_DIR / f"rpa_execucao_{timestamp}.log"
    
    logger = logging.getLogger("RPA_CCAA")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
        
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    
    # 1. Salva no arquivo físico
    file_handler = logging.FileHandler(log_filename, encoding="utf-8", delay=False)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 2. Espelha na tela do Streamlit se o callback for fornecido
    if ui_log_callback:
        ui_handler = StreamlitUIHandler(ui_log_callback)
        ui_handler.setFormatter(formatter)
        logger.addHandler(ui_handler)
    
    return logger, log_filename

def salvar_download_com_seguranca(download, destino: Path):
    if destino.exists():
        try:
            destino.unlink()
        except Exception:
            destino = destino.parent / f"{destino.stem}_{int(time.time())}{destino.suffix}"
    download.save_as(destino)
    return destino

def localizar_elemento_profundo(page: Page, seletor: str):
    """Procura o elemento na página raiz e em TODOS os iframes da tela."""
    if page.locator(seletor).count() > 0:
        return page.locator(seletor).first
    for frame in page.frames:
        if frame.locator(seletor).count() > 0:
            return frame.locator(seletor).first
    return None

def injetar_js_em_todos_os_frames(page: Page, js_code: str):
    """Tenta rodar um bloco JavaScript na raiz e em todos os frames em busca de sucesso cego."""
    sucesso = False
    try:
        page.evaluate(js_code)
        sucesso = True
    except:
        pass
    
    if not sucesso:
        for frame in page.frames:
            try:
                frame.evaluate(js_code)
                sucesso = True
                break
            except:
                pass
    return sucesso

def marcar_checkbox_por_id(page: Page, seletor_id: str):
    chk = localizar_elemento_profundo(page, seletor_id)
    if chk:
        try:
            chk.evaluate("""el => {
                if (!el.checked) {
                    el.click();
                }
            }""")
        except:
            pass
    time.sleep(0.3)

def preencher_data_masked(page: Page, seletor_id: str, data_formatada: str, logger=None):
    campo = localizar_elemento_profundo(page, seletor_id)
    if not campo:
        return

    try:
        campo.evaluate(f"""el => {{
            el.focus(); el.value = '{data_formatada}';
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        }}""")
    except:
        pass
        
    time.sleep(0.3)
    try:
        if campo.input_value() != data_formatada:
            somente_numeros = "".join(c for c in data_formatada if c.isdigit())
            campo.click(force=True)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.press("Home")
            campo.press_sequentially(somente_numeros, delay=40)
            page.keyboard.press("Tab")
            time.sleep(0.3)
    except:
        pass

def selecionar_categoria_select2(page: Page, texto_categoria: str = "1. Mensalidades"):
    id_select = "#ctl00_ctl00_ContentPlaceHolder1_tab_tabFiltros_ContentPlaceHolder2_tab_tabFiltro_cmbPlanoConta"
    
    injetar_js_em_todos_os_frames(page, f"""() => {{
        const el = document.querySelector('{id_select}');
        if (el) {{
            for (let i = 0; i < el.options.length; i++) {{
                if (el.options[i].text.includes('{texto_categoria}') || el.options[i].text.toLowerCase().includes('mensalidade')) {{
                    el.selectedIndex = i;
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    break;
                }}
            }}
        }}
    }}""")
    time.sleep(0.5)

# ----------------------------------------------------------------------
# FLUXO RPA
# ----------------------------------------------------------------------

def autenticar_se_necessario(page: Page, usuario: str, senha: str, logger, log_ui):
    try:
        page.wait_for_selector("input[type='password']", state="visible", timeout=12000)
        tela_login_encontrada = True
    except:
        tela_login_encontrada = False

    if tela_login_encontrada:
        log_msg = f"Detectada tela de login. Autenticando `{usuario}`..."
        logger.info(log_msg)
        log_ui(log_msg)
        
        campo_usuario = localizar_elemento_profundo(page, "#txtLogin, #Login, input[name='txtLogin'], input[type='email']")
        if not campo_usuario:
            campo_usuario = localizar_elemento_profundo(page, "input[type='text']")

        if campo_usuario:
            try:
                campo_usuario.click(force=True)
                campo_usuario.fill("")
                campo_usuario.press_sequentially(usuario, delay=30)
            except:
                pass
        
        campo_senha = localizar_elemento_profundo(page, "#txtSenha, input[name='txtSenha'], input[type='password']")
            
        if campo_senha:
            try:
                campo_senha.click(force=True)
                campo_senha.fill("")
                campo_senha.press_sequentially(senha, delay=30)
            except:
                pass
            
        btn_entrar = localizar_elemento_profundo(page, "#btnok, #btnEntrar, #btnLogin, input[type='submit']")
            
        if btn_entrar:
            try:
                btn_entrar.click(force=True)
            except:
                page.keyboard.press("Enter")
        else:
            page.keyboard.press("Enter")
            
        page.wait_for_load_state("networkidle", timeout=60000)
        time.sleep(2)
        logger.info(f"Autenticado no Sponte para {usuario}")

def extrair_contas_receber_unidade(page: Page, unidade: str, data_inicial: str, logger, log_ui) -> Path:
    logger.info(f"[{unidade}] Acessando módulo Financeiro...")
    page.goto(URL_CONTAS_RECEBER, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_load_state("networkidle")
    
    time.sleep(3) 
    
    logger.info(f"[{unidade}] Marcando: [X] Pendentes e [X] Quitadas via Injeção JS")
    marcar_checkbox_por_id(page, "#ctl00_ctl00_ContentPlaceHolder1_tab_tabFiltros_ContentPlaceHolder2_tab_tabFiltro_cbPendentes")
    marcar_checkbox_por_id(page, "#ctl00_ctl00_ContentPlaceHolder1_tab_tabFiltros_ContentPlaceHolder2_tab_tabFiltro_cbQuitadas")
    
    logger.info(f"[{unidade}] Injetando corte de tempo: {data_inicial}")
    preencher_data_masked(page, "#ctl00_ctl00_ContentPlaceHolder1_tab_tabFiltros_ContentPlaceHolder2_tab_tabFiltro_wcdVencimentoInicial_txtData", data_inicial, logger)
    
    logger.info(f"[{unidade}] Isolando categoria: 1. Mensalidades")
    selecionar_categoria_select2(page, "1. Mensalidades")
    
    logger.info(f"[{unidade}] Forçando ativação da Exportação")
    marcar_checkbox_por_id(page, "#ctl00_ctl00_ContentPlaceHolder1_chkExportar")
    
    injetar_js_em_todos_os_frames(page, """() => { 
        const el = document.querySelector('#ctl00_ctl00_ContentPlaceHolder1_cmbTipoExportacao');
        if (el) {
            el.removeAttribute('disabled');
            el.value = '4'; 
            el.dispatchEvent(new Event('change', { bubbles: true })); 
        }
    }""")
    time.sleep(1)
    
    logger.info(f"[{unidade}] Disparando Botão de Visualização/Exportação")
    
    with page.expect_download(timeout=120000) as download_info:
        btn_gerar = localizar_elemento_profundo(page, "#ctl00_ctl00_ContentPlaceHolder1_btnGerar_div")
        if btn_gerar:
            try:
                btn_gerar.evaluate("el => el.click()")
            except:
                injetar_js_em_todos_os_frames(page, "() => { document.querySelector('#ctl00_ctl00_ContentPlaceHolder1_btnGerar_div').click(); }")
        else:
            injetar_js_em_todos_os_frames(page, "() => { document.querySelector('#ctl00_ctl00_ContentPlaceHolder1_btnGerar_div').click(); }")
        
    destino = DOWNLOAD_DIR / f"rec_{unidade}.xlsx"
    path_final = salvar_download_com_seguranca(download_info.value, destino)
    logger.info(f"[{unidade}] Download finalizado: {path_final.name}")
    return path_final

def sincronizar_todas_as_unidades_sponte(usuario_prefixo: str, senha_padrao: str, ano_referencia: int, status_callback=None, log_callback=None, modo_visivel: bool = False) -> tuple[bool, str, Path]:
    logger, log_path = configurar_logger_execucao(ui_log_callback=log_callback)
    inicio_execucao = time.time()
    
    data_inicial_sp = f"01/11/{ano_referencia - 1}"

    def log_ui(msg):
        if status_callback: status_callback(msg)

    logger.info("=" * 90)
    logger.info(f"INICIANDO SINCRONIZAÇÃO DE RECEITAS | OPERADOR: {usuario_prefixo} | ANO REF: {ano_referencia}")
    logger.info("=" * 90)

    log_ui("⚠️ Destruindo banco de dados anterior conforme protocolo...")
    if limpar_banco():
        logger.info("[SISTEMA] O banco de dados foi completamente expurgado.")
    else:
        logger.error("[SISTEMA] Falha ao executar DROP na tabela do banco.")

    unidades_sucesso, unidades_falha = [], []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not modo_visivel, args=["--disable-blink-features=AutomationControlled"])
        total_unidades = len(UNIDADES_DOMINIOS)

        for index, (unidade, dominio) in enumerate(UNIDADES_DOMINIOS.items(), start=1):
            inicio_filial = time.time()
            login_user = f"{usuario_prefixo}{dominio}"
            
            logger.info("-" * 90)
            logger.info(f"[{index}/{total_unidades}] [FILIAL {unidade.upper()}]")
            log_ui(f"[{index}/{total_unidades}] Extraindo dados: {unidade}...")
            
            context_unid = browser.new_context(accept_downloads=True, viewport={"width": 1366, "height": 768})
            page_unid = context_unid.new_page()
            
            try:
                page_unid.goto(URL_CONTAS_RECEBER, wait_until="domcontentloaded", timeout=60000)
                autenticar_se_necessario(page_unid, login_user, senha_padrao, logger, log_ui)
                
                path_rec = extrair_contas_receber_unidade(page_unid, unidade, data_inicial_sp, logger, log_ui)
                logger.info(f"[{unidade}] Artefato bruto: {path_rec.stat().st_size / 1024:.2f} KB")

                logger.info(f"[{unidade}] Transferindo para ETL...")
                inicio_etl = time.time()
                df_tratado = process_contas_receber(path_rec, unidade, ano_referencia)
                logger.info(f"[{unidade}] ETL processou em {time.time() - inicio_etl:.2f}s.")

                if not df_tratado.empty:
                    salvo, msg_banco = salvar_lote_no_banco(df_tratado)
                    if salvo:
                        msg_sucesso = f"[{index}/{total_unidades}] ✅ {unidade}: {len(df_tratado)} parcelas computadas."
                        logger.info(f"[{unidade}] {msg_sucesso}")
                        log_ui(msg_sucesso)
                        unidades_sucesso.append(unidade)
                    else:
                        raise Exception(f"Banco rejeitou a operação: {msg_banco}")
                else:
                    msg_vazio = f"[{index}/{total_unidades}] ⚠️ {unidade}: Carga vazia após regras do ETL."
                    logger.warning(f"[{unidade}] {msg_vazio}")
                    log_ui(msg_vazio)
                    unidades_sucesso.append(unidade)
                    
            except Exception as e:
                msg_erro = f"Falha executando {unidade}: {str(e)}"
                logger.error(f"[{unidade}] {msg_erro}")
                logger.error(traceback.format_exc())
                log_ui(f"[{index}/{total_unidades}] ❌ {unidade} Falhou.")
                unidades_falha.append((unidade, str(e)))
            finally:
                context_unid.close()
                logger.info(f"[{unidade}] Ciclo encerrado. Tempo: {time.time() - inicio_filial:.2f}s.")

        browser.close()

    tempo_total = time.time() - inicio_execucao
    logger.info("=" * 90)
    logger.info(f"RESUMO GERAL | TEMPO: {tempo_total:.2f}s")
    logger.info(f"Sucessos ({len(unidades_sucesso)}): {', '.join(unidades_sucesso) if unidades_sucesso else 'Nenhum'}")
    if unidades_falha:
        logger.error(f"Falhas ({len(unidades_falha)}): {[u[0] for u in unidades_falha]}")
    logger.info("=" * 90)
    
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()

    msg_final = f"Processo finalizado ({tempo_total:.1f}s). Sucesso: {len(unidades_sucesso)}/{total_unidades}."
    return len(unidades_falha) == 0, msg_final, log_path