import os
from pathlib import Path
from core.etl import process_contas_receber
from core.database import salvar_lote_no_banco, limpar_banco

def extrair_unidade_do_nome(nome_arquivo):
    """Tenta adivinhar a unidade baseada no nome do arquivo baixado."""
    unidades_validas = [
        "Paralela", "Matatu de Brotas", "Iguatemi", 
        "Simões Filho", "Periperi", "Cajazeiras"
    ]
    for u in unidades_validas:
        if u.lower() in nome_arquivo.lower():
            return u
    return "Desconhecida"

def rodar_apenas_etl(ano_referencia):
    download_dir = Path("./temp_downloads")
    arquivos = list(download_dir.glob("*.xlsx"))
    
    if not arquivos:
        print("ERRO: Nenhum arquivo .xlsx encontrado na pasta 'temp_downloads'. Rode o RPA pelo menos uma vez para baixar a base bruta.")
        return

    print("🔴 Destruindo banco de dados atual para teste limpo...")
    limpar_banco()
    print("=" * 60)

    for arquivo in arquivos:
        unidade = extrair_unidade_do_nome(arquivo.name)
        print(f"⚙️ Processando: {arquivo.name}")
        print(f"📍 Unidade Identificada: {unidade}")
        
        try:
            # Roda APENAS as regras de negócio
            df_tratado = process_contas_receber(arquivo, unidade, ano_referencia)
            
            if not df_tratado.empty:
                salvo, msg = salvar_lote_no_banco(df_tratado)
                if salvo:
                    print(f"✅ Sucesso: {len(df_tratado)} parcelas inseridas no banco.")
                else:
                    print(f"❌ Erro ao salvar no banco: {msg}")
            else:
                print("⚠️ Aviso: O DataFrame retornou vazio do ETL.")
        
        except Exception as e:
            print(f"🔥 ERRO CRÍTICO NO ETL: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("-" * 60)

if __name__ == "__main__":
    # Defina o ano letivo que deseja testar
    ANO_ALVO = 2026
    print(f"Iniciando Teste Isolado do ETL | Ano: {ANO_ALVO}\n")
    rodar_apenas_etl(ANO_ALVO)