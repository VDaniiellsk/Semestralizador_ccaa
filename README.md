# Semestralizador CCAA

Aplicação web local para consultar e consolidar os dados financeiros exportados do ERP Sponte. O projeto surgiu da necessidade de recuperar uma visão por semestre e por unidade que deixou de estar disponível no novo sistema da empresa.

A aplicação reúne coleta automatizada, tratamento dos relatórios, armazenamento em SQLite e painéis em Streamlit. Seu objetivo é apoiar a conferência de recebimentos, valores a receber e inadimplência, além da análise por aluno, turma, estágio e curso.

## Executar o projeto

Use o terminal na raiz do repositório. Os comandos abaixo são para PowerShell no Windows; a versão utilizada no desenvolvimento é Python 3.13.

```powershell
git clone https://github.com/VDaniiellsk/Semestralizador_ccaa.git
cd Semestralizador_ccaa
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install streamlit pandas plotly playwright openpyxl
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m streamlit run relccaa.py
```

Se o projeto já estiver na máquina, comece pela criação do ambiente ou use o ambiente existente. Execute a aplicação a partir da raiz: os caminhos do log, das exportações e do logo dependem desse diretório.

### Configuração privada

Crie `.streamlit/secrets.toml` com os usuários da aplicação e as unidades acessíveis no ERP. O exemplo é fictício: substitua nomes, senhas e domínios antes de usar.

```toml
[passwords]
usuario_exemplo = "substitua-por-uma-senha-local"

[[unidades]]
nome = "Unidade Exemplo"
dominio = "@dominio-exemplo"
```

Repita `[[unidades]]` para todas as unidades. As configurações reais devem ser iguais às usadas nos relatórios e na referência de preços. O login do ERP é composto pelo prefixo informado na tela e pelo domínio configurado.

A lista `admins_autorizados` em `relccaa.py` define quem vê a página de sincronização. Os demais usuários autenticados têm acesso às análises. Os nomes dessa lista precisam coincidir com o usuário convertido para minúsculas pela aplicação; cadastrar uma senha não concede, por si só, acesso administrativo. A autenticação atual compara senhas locais no arquivo privado; não utiliza hash de senha, SSO ou um serviço externo de identidade.

A estimativa de descontos utiliza `config/precos_<ano>.json`. Essa tabela é privada e não acompanha o repositório público. Sem uma referência disponível para o ano, a análise financeira continua funcionando e o resultado da estimativa informa a ausência da tabela. A estrutura do arquivo está descrita em [Arquitetura e regras](docs/ARQUITETURA.md).

## Como os dados chegam aos painéis

1. O administrador seleciona o ano e inicia a sincronização com suas credenciais do ERP.
2. O Playwright acessa cada unidade em um contexto separado e baixa o relatório de mensalidades em Excel.
3. O tratamento normaliza datas, valores e textos; reconhece cursos e estágios; aplica o recorte do ano e calcula as estimativas possíveis.
4. Todas as unidades são validadas antes da gravação. Uma transação substitui a fotografia financeira no SQLite.
5. Os painéis consultam a view `recebiveis_auditados` e calculam os indicadores e filtros.

Se a coleta ou a gravação falhar, a carga anterior permanece disponível. Uma unidade sem registros pode participar de uma carga válida; uma carga inteiramente vazia é recusada. O banco não conserva as sincronizações anteriores.

O banco ativo é `data/auditoria_relatorios.db`. Ele é preparado automaticamente e não precisa ser apagado antes de sincronizar. O esquema atual está na versão 4; as migrações preservam os registros existentes. Consulte [Migração relacional](MIGRACAO_RELACIONAL.md) para entender o que foi implementado e o que permanece previsto.

## Telas disponíveis

| Tela | Finalidade |
| --- | --- |
| Dashboard Geral | Visão de receitas previstas, recebimentos, valores vencidos e gráficos. |
| Matriz de Valores | Consolidação financeira e detalhamento por unidade e semestre. |
| Valores por Alunos | Consulta da situação e das parcelas de cada aluno. |
| Devedores Gerais | Consulta dos alunos inadimplentes e dos valores vencidos. |
| Turmas e Cursos | Totais por turma, curso e estágio e detalhamento dos alunos. |
| Manual de Operação | Orientações de uso dentro da aplicação. |
| Upload & Sincronização | Coleta administrativa, acompanhamento e consulta de logs. |

Os filtros compartilhados permitem recortar unidade, ano, semestre, curso, estágio, turma, aluno e situação da parcela. A disponibilidade de cada filtro depende da tela. Agrupar separa o resultado em uma tabela para cada combinação escolhida, mantendo suas informações. Quando há muitos grupos, a exibição é paginada.

Cada tabela apresenta alunos distintos, valor a receber, valor recebido, valor inadimplente e quantidade de devedores. Esses totais usam as parcelas de origem, inclusive quando a tabela exibida é um resumo. Um aluno que aparece em várias turmas não deve ser contado várias vezes no total consolidado.

## Regras financeiras principais

- **Identificação do aluno:** unidade e matrícula, porque a mesma matrícula pode existir em unidades diferentes.
- **Recebido:** valor pago das parcelas cuja situação indica pagamento. Uma parcela cancelada não entra nos indicadores financeiros.
- **A receber:** valor com desconto das parcelas pendentes, incluindo vencimentos futuros.
- **Valor inadimplente:** valor com desconto das parcelas pendentes com vencimento menor ou igual à data atual. Não inclui automaticamente juros futuros.
- **Aluno inadimplente:** aluno com pelo menos uma parcela vencida e não paga. Filtrar apenas parcelas pagas não muda a situação calculada na base de referência.
- **Semestre e ano:** seguem os critérios existentes no tratamento e nos painéis, descritos na documentação técnica. O vencimento participa da classificação dos registros anuais; a data de início participa da classificação dos semestrais.
- **Dados ausentes:** turma, estágio e datas opcionais podem permanecer ausentes. Isso não autoriza excluir a parcela nem inventar um identificador de contrato.

Cada linha exportada é preservada, mesmo que se pareça com outra. O número da parcela representa a sequência dentro do contrato e não é uma chave única do banco. Ainda não há código de contrato disponível na exportação utilizada.

### Estimativa de desconto e bolsa/convênio

A estimativa compara os valores cobrados com os preços e parcelamentos da referência privada do ano e da região. English A, T e I utilizam o preço do nível equivalente. Contratos semestrais também podem ter desconto.

Somente uma correspondência única produz percentual e pacote estimados. Datas incompletas, sequência de parcelas incompleta, números repetidos ou combinações ambíguas deixam o resultado sem confirmação. O cálculo não altera os valores financeiros nem a bolsa informada no ERP. Um percentual estimado não identifica o nome de um convênio.

Quando um pacote anual é reconhecido com apenas um estágio observado, o resultado avisa que o segundo estágio foi inferido. Há também uma verificação conservadora de duração de 240 dias para evitar interpretar uma carga anual parcial como semestral. Essa verificação é uma hipótese técnica e precisa ser considerada na conferência com os contratos reais.

## Reprocessar sem acessar o ERP

Os arquivos de `temp_downloads` podem ser tratados novamente. O exemplo abaixo deve ser salvo como um script local na raiz e executado com o mesmo Python usado pela aplicação. Ele não abre o navegador, mas **substitui a base ativa** se todos os relatórios forem válidos.

```python
from pathlib import Path
from core.config import UNIDADES_DOMINIOS
from core.etl import process_contas_receber
from core.database import salvar_carga_completa

ano = 2026
lotes = {
    unidade: process_contas_receber(
        Path("temp_downloads") / f"rec_{unidade}.xlsx", unidade, ano
    )
    for unidade in UNIDADES_DOMINIOS
}
sucesso, mensagem = salvar_carga_completa(lotes, list(UNIDADES_DOMINIOS))
print(mensagem)
if not sucesso:
    raise SystemExit(1)
```

Confira se os arquivos pertencem à coleta e ao ano desejados. Se o download tiver recebido um nome alternativo por estar ocupado, ajuste o caminho. Para experimentar sem alterar a base ativa, passe `path=Path("data/teste_reprocessamento.db")` à função de gravação; os painéis continuarão lendo a base ativa.

O reconhecimento de estágios e a estimativa de descontos também são atualizados em memória ao preparar os dados das análises. Portanto, algumas correções podem ser visualizadas ao reiniciar a aplicação, antes de uma nova coleta; a próxima sincronização persistirá o resultado atualizado.

## Organização do código

| Local | Responsabilidade |
| --- | --- |
| `relccaa.py` | Entrada, autenticação local e navegação. |
| `core/config.py` | Configuração privada das unidades. |
| `core/rpa.py` | Coleta no navegador e logs. |
| `core/sync_runtime.py` | Atualização dos módulos e bloqueio de execução simultânea no processo. |
| `core/etl.py` | Leitura e tratamento das exportações. |
| `core/catalogo.py` | Reconhecimento de cursos e estágios. |
| `core/descontos.py` | Estimativas a partir da referência de preços. |
| `core/database.py` | Validação, migração e publicação transacional. |
| `core/schema_relacional.sql` | Tabelas, restrições, índices e view. |
| `core/analise.py` | Indicadores, filtros e resumos. |
| `views/` | Telas e componentes compartilhados. |
| `tests/` | Testes de regressão com dados fictícios. |

## Testar e manter

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests
```

Os testes cobrem tratamento, classificação, cálculos, estimativas, integridade relacional, migrações, falhas de carga e renderização das telas. Eles não executam uma coleta real no ERP. Depois de alterar seletores ou o fluxo do Sponte, faça também uma conferência controlada da sincronização e dos totais exportados.

Mantenha regras de classificação em `catalogo.py`, regras de estimativa em `descontos.py`, cálculos em `analise.py` e gravações em `database.py`. Mudanças de estrutura exigem atualizar o SQL, a migração, a view e os testes. Comentários e docstrings explicam as decisões que devem ser preservadas.

## Arquivos privados e limites atuais

O `.gitignore` protege configurações, bancos, relatórios, logs, tabelas de preços, ambientes locais e caches. Não publique dados de alunos, senhas ou valores internos da empresa. Arquivos já rastreados pelo Git não deixam de ser rastreados apenas por receber uma regra de exclusão.

A automação depende da interface do ERP e pode precisar de ajustes quando ela muda. A integração por API é uma evolução prevista, dependente de disponibilidade e autorização; não está implementada nesta versão. O bloqueio da sincronização vale para um processo, não para várias instâncias independentes.

O modelo completo com `contrato` e `contrato_turma` permanece planejado. O esquema atual permite importar os relatórios existentes sem criar vínculos de contrato que os dados ainda não comprovam.
