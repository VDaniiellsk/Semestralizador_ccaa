# Migração relacional

## Situação atual

A aplicação utiliza `data/auditoria_relatorios.db`, com esquema versão 4. As tabelas implementadas são `unidade`, `aluno`, `curso`, `turma` e `parcela`. A view `recebiveis_auditados` fornece os 21 campos financeiros anteriores, `Estagio` e os cinco campos de estimativa de desconto.

O modelo completo de entidade-relacionamento, com `contrato` e `contrato_turma`, permanece planejado. A exportação atual não fornece o código do contrato; por isso, a implementação não cria contratos a partir de nome, matrícula e número de parcela.

## Compatibilidade com os relatórios existentes

Aluno é identificado por unidade e matrícula. Turma é identificada por unidade e nome. Cada linha financeira recebe um ID interno válido para a carga atual. Linhas idênticas e números de parcela repetidos são preservados, pois podem representar registros de contratos diferentes.

Turma, estágio e datas opcionais podem permanecer ausentes. Valores monetários são guardados em centavos inteiros e descontos estimados em pontos-base. A view converte esses valores para o formato esperado pelos painéis.

A classificação analítica de contrato e os critérios de ano e semestre seguem a implementação documentada em [Arquitetura e regras](docs/ARQUITETURA.md). Essas aproximações não comprovam vínculos com um contrato específico.

## Migrações automáticas

`get_connection` identifica a versão e prepara a estrutura antes da leitura ou gravação. A migração de versão 2 reconstrói o esquema em uma transação, preservando os registros. A migração de versão 3 acrescenta os cinco campos de estimativa e recria a view, preservando os IDs e valores existentes.

Não é necessário apagar o banco para atualizar o esquema. Faça uma cópia privada antes de uma alteração estrutural em produção. Bancos de nomes antigos bloqueados pelo código não devem ser usados como substitutos do banco ativo.

## Sincronização e teste

A coleta valida todas as unidades antes de substituir os registros em uma transação. Falhas preservam a fotografia anterior; não há histórico de sincronizações no banco ativo.

Execute a aplicação normalmente e use a tela administrativa para uma coleta real. Para reprocessar arquivos já exportados, siga o exemplo do [README](README.md). Use um caminho de banco separado ao testar sem substituir a base ativa.

A suíte em `tests` verifica migrações, preservação de valores, integridade e publicação sem acesso ao ERP. O teste operacional do navegador e a conferência dos dados reais continuam necessários após mudanças na coleta.
