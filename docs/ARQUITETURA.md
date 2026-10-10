# Arquitetura e regras da versão atual

## Separação de responsabilidades

O navegador entrega arquivos, o ETL entrega registros tratados e o banco publica uma carga completa. As telas não devem executar SQL de gravação para corrigir um indicador. A regra deve ser corrigida na camada responsável, para que todas as telas usem a mesma interpretação.

```text
Sponte → rpa.py → arquivos Excel → etl.py
                                  ├─ catalogo.py
                                  ├─ descontos.py ← preços privados
                                  └─ database.py → SQLite
                                                     ↓
                                          recebiveis_auditados
                                                     ↓
                                             analise.py → views
```

`sync_runtime.py` recarrega banco, ETL e RPA nessa ordem antes de sincronizar. Um bloqueio em memória impede execuções concorrentes no mesmo processo e é liberado mesmo se ocorrer uma exceção.

## Modelo de dados implementado

| Tabela | Identificação | Observação |
| --- | --- | --- |
| unidade | ID interno; nome único | Identifica a origem do relatório. |
| aluno | Unidade + matrícula | A matrícula pode se repetir em outra unidade. |
| curso | ID interno; nome único | Usa a nomenclatura reconhecida pelo catálogo. |
| turma | Unidade + nome | Vinculada a um curso; um vínculo conflitante impede a publicação. |
| parcela | ID interno; unidade + linha de origem únicos | Preserva cada linha da carga, sem deduplicação financeira. |

Uma parcela referencia aluno e curso; a turma pode ser nula. As datas e o tipo analítico de contrato ficam na parcela enquanto não houver código real de contrato. Os IDs internos e números de linha pertencem à fotografia atual e não são identificadores estáveis entre sincronizações.

Valores monetários são inteiros em centavos, com arredondamento `ROUND_HALF_UP`. Datas persistidas são texto ISO. Descontos estimados usam pontos-base: 2500 representa 25%. A view converte centavos para reais, pontos-base para percentuais e fornece os nomes em PascalCase esperados nas análises, além de `unidade`.

A view possui 27 campos: 21 campos financeiros anteriores, `Estagio` e cinco campos de estimativa. Consulte o SQL para o contrato completo de nomes e restrições. Não altere um alias isoladamente: ETL, análises e telas dependem dessa interface.

## Publicação e integridade

`validar_lote` rejeita campos financeiros inválidos e identifica a linha. `salvar_carga_completa` exige todas as unidades esperadas, valida os lotes antes de gravar e recusa uma carga totalmente vazia. A exclusão e a inserção de registros ocorrem dentro de uma transação; uma falha restaura a carga anterior.

O banco é um retrato da coleta, sem histórico de cargas. Uma unidade que passou de registros para zero registros será atualizada para zero, desde que a coleta completa tenha sido concluída com sucesso.

## Critérios temporais existentes

Os critérios abaixo descrevem a implementação atual, inclusive suas diferenças entre camadas:

- **Recorte do ETL:** usa o ano `20xx` encontrado no nome da turma; se não houver, usa o ano selecionado na sincronização.
- **Ano nos painéis:** prioriza o ano do nome da turma. Na ausência dele, usa o ano de início e considera novembro/dezembro como o ano seguinte. Sem essas referências, o ano permanece ausente.
- **Tipo de contrato:** preserva a informação fornecida. Quando ela falta, a classificação herdada compara a quantidade de linhas da matrícula com limites por mês de início: novembro 8, dezembro 7, janeiro 6, fevereiro 5, março 4 e abril 3. Nos meses dessa lista, atingir o limite indica Anual; fora da condição, Semestral. Sem início, Não informado. Essa aproximação pode misturar contratos da mesma matrícula e não substitui um código de contrato.
- **Semestre:** para registros Anuais, vencimento até 30 de junho do ano selecionado indica primeiro semestre; depois, segundo. Nos demais registros, início entre maio e outubro indica segundo semestre; outros meses indicam primeiro. Sem início, Não informado.

Essas regras precisam ser conferidas com o diretor quando forem modificadas. Não substitua a regra implementada por uma descrição genérica de semestre civil.

## Cursos e estágios

O catálogo padroniza seis cursos: BABY CLASS, ENGLISH COURSE, ESPAÑOL, KIDS´ COURSE, PRETEEN COURSE e TEACHERS' COURSE. As variantes de estágios, inclusive A, T, I, VIP e combinações previstas, estão em `STAGE_COURSES`.

A busca considera grafias e espaçamentos comuns e testa os nomes mais específicos antes dos mais curtos. O número após um ponto pode representar a identificação da turma, não outro estágio. Uma turma não reconhecida continua na base; a ausência de classificação não autoriza excluir o financeiro.

## Indicadores e agrupamentos

Os recebimentos exigem uma situação reconhecida como paga, excluindo expressões que indiquem pendência e cancelamento. O valor vencido usa `ValorComDesconto` das pendências com vencimento menor ou igual a hoje. O valor a receber também inclui pendências futuras.

`resumo_alunos` utiliza a referência anterior ao filtro de situação para determinar se o aluno é inadimplente. As tabelas usam `totais_tabela` com as parcelas de origem: somar as contagens dos resumos pode repetir alunos que aparecem em mais de uma turma.

Agrupar divide os registros em tabelas sem reduzir suas colunas. Os grupos são paginados em conjuntos de até 20. A renderização usa formatos nativos do Streamlit, evitando o limite de células do Pandas Styler.

## Referência privada de preços

`config/precos_<ano>.json` contém:

| Campo | Conteúdo |
| --- | --- |
| ano | Ano da referência, como inteiro. |
| fonte | Identificação da tabela usada. |
| regioes | Dicionário de regiões e suas regras. |
| regioes.*.unidades | Nomes das unidades atendidas pela região. |
| regioes.*.precos | Preços integrais como strings decimais com ponto. |
| regioes.*.descontos | Percentuais permitidos na comparação. |
| regioes.*.parcelas_semestrais | Quantidades permitidas para pacotes semestrais. |
| regioes.*.parcelas_anuais | Quantidades permitidas para pacotes anuais. |
| regioes.*.parcelas_vip | Quantidades VIP, quando aplicável. |

As chaves de preço são Baby, Kids, Preteen, Español, TEACHERS, English 1-3, English 4-6, English 7-9, English 10-11, English C 1-2 e VIP, quando disponível. Validade, equivalências e observações podem documentar a origem e decisões da referência. Não inclua os valores reais em exemplos públicos.

### Como a estimativa funciona

1. Agrupa candidatos por unidade, matrícula, início, término e ano; as datas delimitam uma hipótese, não a identidade do contrato.
2. Exige datas coerentes com o período da referência, sequência completa de 1 a N, sem números repetidos e valores positivos. Grupos com cancelamentos não são estimados.
3. Reconhece até dois estágios e busca pacotes e parcelamentos compatíveis. English A, T e I convergem para o preço do nível equivalente; VIP permanece separado.
4. Compara `ValorComDesconto` com as parcelas esperadas após o desconto. A tolerância é de um centavo por parcela; somente a última parcela pode ter ajuste maior, limitado a N centavos, e a diferença do total também não pode exceder N centavos.
5. Aceita somente uma correspondência. Uma combinação anual com segundo estágio não observado recebe um aviso explícito de inferência.

A duração de 240 dias é uma proteção heurística: pacotes semestrais acima desse limite e anuais abaixo dele são rejeitados. Isso reduz falsos positivos de cargas parciais, mas pode deixar contratos reais sem correspondência. O cálculo também não identifica taxas separadas ou contratos que tenham datas iguais e parcelas repetidas.

Os resultados são `DescontoEstimado`, `PacoteEstimado`, `ParcelamentoEstimado`, `ResultadoEstimativa` e `FonteEstimativa`. A bolsa informada pelo ERP tem prioridade de exibição. Quitadas de valor pago zero e sem bolsa recebem a classificação operacional Bolsista no ETL; essa regra depende da qualidade do relatório e não constitui comprovação externa de uma bolsa.

## Evolução e conferência

O próximo modelo com contratos requer os identificadores reais do ERP. Até lá, preserve as linhas e indique as limitações de qualquer inferência. Alterações no banco devem incluir migração transacional e teste de preservação de valores. Alterações em curso, estágio, status e desconto devem incluir casos de reconhecimento e casos em que o sistema deve se abster de classificar.

Os testes automatizados não comprovam disponibilidade do ERP nem equivalência contábil dos relatórios. A validação operacional compara amostras e totais com as exportações reais sem publicar dados sensíveis.
