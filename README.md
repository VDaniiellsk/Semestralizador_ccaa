
# Sistema de Auditoria e Inteligência Financeira - CCAA

## Visão Estratégica
Sistema projetado para consolidar, higienizar e analisar o fluxo de caixa, passivo de inadimplência e projeções financeiras de 6 unidades franqueadas do CCAA. O projeto substitui a extração manual e a manipulação descentralizada de planilhas por um pipeline automatizado (RPA), um motor de transformação rigoroso (ETL) e painéis executivos com controle de acesso (RBAC).

O sistema expõe a realidade financeira das unidades calculando métricas a partir da verdade transacional (o que realmente caiu na conta vs. o que foi faturado), ancorando as exclusões e análises em metadados absolutos, como o Ano Letivo.


---

## Arquitetura do Sistema

A aplicação é dividida em três camadas isoladas para garantir escalabilidade e rastreabilidade de falhas:

1. **Camada de Ingestão (RPA - Provisória):** Utiliza automação de navegador (Playwright) para emular o acesso humano ao ERP Sponte, iterar sobre as 6 filiais e baixar os relatórios de "Contas a Receber" no formato `.xlsx`. *Aviso: Esta camada está em processo de migração para o consumo direto da API SOAP oficial da Sponte.*
2. **Camada de Transformação e Banco de Dados (ETL):** Lê os relatórios brutos, aplica regras inegociáveis de higienização de colunas (remoção de acentos/espaços), tipagem de dados, conversão de datas (ISO) e recálculo temporal (Ano Letivo). A persistência é feita em SQLite com arquitetura destrutiva (DROP TABLE a cada sincronização) para garantir que os dados exibidos reflitam o espelho exato do ERP no momento da extração.
3. **Camada de Visualização (Streamlit):** Interface de usuário executiva contendo autenticação por sessão, matrizes de valores cruzadas, detalhamento cirúrgico por aluno (identificação de inadimplentes e bolsistas) e análise de risco (Calote vs. Caixa Realizado).

---

## Stack Tecnológico

* **Linguagem:** Python 3.10+
* **Frontend / Framework:** Streamlit
* **Processamento de Dados:** Pandas, Numpy
* **Visualização:** Plotly Express / Graph Objects
* **Automação Web (Scraping):** Playwright
* **Banco de Dados:** SQLite3

---

## Estrutura de Diretórios

```text
/
├── relccaa.py                 # Ponto de entrada principal, roteamento e barreira de Login (RBAC).
├── rpa.py                     # Motor de extração automatizada no Sponte (Playwright).
├── test_etl.py                # Script de auditoria para rodar transformações isoladas de banco.
├── .streamlit/
│   └── secrets.toml           # Cofre de credenciais (NÃO DEVE SER COMMITADO NO GIT).
├── core/
│   ├── etl.py                 # Regras de negócio, higienização de strings e recálculo de Ano Letivo.
│   └── database.py            # Operações SQLite (limpar banco, salvar lotes, carregar dados).
├── views/
│   ├── dashboard.py           # KPIs globais, gráficos de risco e fluxo de caixa.
│   ├── valores_semestrais.py  # Matriz pivô para cruzamento de filiais e status.
│   ├── valores_alunos.py      # Visão micro para cobrança, cálculo de dívida real por aluno.
│   ├── manual.py              # Documentação operacional das regras de negócio do sistema.
│   └── upload.py              # Interface de disparo do robô e gatilho do pipeline ETL.
├── temp_downloads/            # Pasta temporária para armazenamento bruto dos relatórios (.xlsx).
└── src/
    └── CCAA_logo_(2020).svg   # Identidade visual.

```

---

## Instalação e Configuração

**1. Clonar o Repositório e Criar Ambiente Virtual**

```bash
git clone 
cd 
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

```

**2. Instalar Dependências**

```bash
pip install streamlit pandas numpy plotly playwright openpyxl

```

**3. Instalar os Navegadores do Playwright**

```bash
playwright install

```

**4. Configurar o Cofre de Senhas (Obrigatório)**
Crie a pasta oculta e o arquivo de segredos para habilitar o login:

```bash
mkdir .streamlit
touch .streamlit/secrets.toml

```

Adicione o conteúdo abaixo no arquivo `secrets.toml`:

```toml
[passwords]
daniel = "senha_admin_aqui"
diretoria = "senha_diretoria_aqui"
operacao = "senha_operacao_aqui"

```

---

## Execução

Inicie o servidor local do Streamlit executando o arquivo raiz:

```bash
streamlit run relccaa.py

```

O sistema exigirá login imediatamente. Apenas usuários mapeados na lista de administradores no código `relccaa.py` terão acesso à tela de *Upload & Sincronização* para alterar o banco de dados.

---

## Matriz de Risco e Governança Operacional

* **Arquitetura sem Histórico:** O sistema não é um Data Warehouse incremental. Cada nova sincronização via RPA destrói e recria o banco de dados `auditoria_financeira.db`. Dados filtrados e ignorados pelo expurgo do ETL não poderão ser recuperados pelo dashboard.
* **Bloqueio de IP (WAF Sponte):** A solução de RPA em vigor pode acionar firewalls e resultar em bloqueio de rede. O uso contínuo exige manutenção rigorosa no controle de latência artificial e rotação de sessão para simular tráfego humano, até que a integração oficial via API SOAP seja estabelecida.
* **Verdade Semântica vs. Financeira:** O cálculo de Caixa Realizado obedece estritamente ao termo `"Quitada"`. Erros operacionais nas secretarias das unidades, como o não preenchimento da Situação correta, resultarão imediatamente na exclusão daquele montante das receitas efetivadas do painel. O erro não é corrigido no código; ele deve ser corrigido na origem e ressincronizado.

```

Você manterá este README restrito à documentação interna do projeto ou o utilizará como argumento técnico para demonstrar o nível de maturidade do seu sistema durante a negociação orçamentária com a diretoria?

```