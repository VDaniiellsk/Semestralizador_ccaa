-- Esquema financeiro v4: uma fotografia da última carga completa.
-- IDs internos não representam códigos de contrato e podem mudar entre cargas.
-- Matrícula é única apenas dentro da unidade; turma usa unidade e nome.
-- Valores financeiros são centavos inteiros. Estimativa de desconto usa
-- pontos-base (2500 = 25%); NULL indica que não houve estimativa conclusiva.
-- A view mantém o contrato de nomes usado pelo ETL e pelas telas.
PRAGMA foreign_keys=ON;
CREATE TABLE unidade(id INTEGER PRIMARY KEY, nome TEXT NOT NULL UNIQUE);
CREATE TABLE aluno(unidade_id INTEGER NOT NULL, matricula TEXT NOT NULL, nome TEXT NOT NULL,
 PRIMARY KEY(unidade_id,matricula), FOREIGN KEY(unidade_id) REFERENCES unidade(id));
CREATE TABLE curso(id INTEGER PRIMARY KEY,nome TEXT NOT NULL UNIQUE);
CREATE TABLE turma(unidade_id INTEGER NOT NULL,nome TEXT NOT NULL,curso_id INTEGER NOT NULL,
 PRIMARY KEY(unidade_id,nome), FOREIGN KEY(unidade_id) REFERENCES unidade(id),FOREIGN KEY(curso_id) REFERENCES curso(id));
-- Cada linha do relatório é preservada. NumeroParcela não é chave única.
CREATE TABLE parcela(
 id INTEGER PRIMARY KEY,unidade_id INTEGER NOT NULL,linha_origem INTEGER NOT NULL,
 matricula TEXT NOT NULL,turma_nome TEXT,numero INTEGER NOT NULL CHECK(numero>0),
 sacado TEXT NOT NULL,situacao_aluno TEXT,tipo_contrato TEXT NOT NULL,
 data_inicio TEXT,data_termino TEXT,data_vencimento TEXT NOT NULL,data_pagamento TEXT,
 valor_com_desconto_centavos INTEGER NOT NULL CHECK(typeof(valor_com_desconto_centavos)='integer' AND valor_com_desconto_centavos>=0),
 valor_pago_centavos INTEGER NOT NULL CHECK(typeof(valor_pago_centavos)='integer' AND valor_pago_centavos>=0),
 valor_com_juros_centavos INTEGER CHECK(valor_com_juros_centavos IS NULL OR (typeof(valor_com_juros_centavos)='integer' AND valor_com_juros_centavos>=0)),
 situacao TEXT NOT NULL,semestre_referencia TEXT NOT NULL CHECK(semestre_referencia IN ('1º Semestre','2º Semestre','Não informado')),
 bolsa TEXT,forma_cobranca TEXT,nome_atendente TEXT,nome_operadora_cartao TEXT,curso_id INTEGER NOT NULL,estagio TEXT,
 desconto_estimado_bp INTEGER CHECK(desconto_estimado_bp BETWEEN 0 AND 10000),
 pacote_estimado TEXT,parcelamento_estimado INTEGER CHECK(parcelamento_estimado>0),
 resultado_estimativa TEXT,fonte_estimativa TEXT,
 UNIQUE(unidade_id,linha_origem),FOREIGN KEY(unidade_id,matricula) REFERENCES aluno(unidade_id,matricula),
 FOREIGN KEY(unidade_id,turma_nome) REFERENCES turma(unidade_id,nome),
 FOREIGN KEY(curso_id) REFERENCES curso(id));
CREATE INDEX parcela_aluno ON parcela(unidade_id,matricula);
CREATE INDEX parcela_turma ON parcela(unidade_id,turma_nome);
CREATE INDEX parcela_vencimento ON parcela(data_vencimento);
CREATE VIEW recebiveis_auditados AS SELECT
 p.numero AS NumeroParcela,p.sacado AS Sacado,p.matricula AS NumeroMatricula,
 p.valor_com_desconto_centavos/100.0 AS ValorComDesconto,p.data_vencimento AS DataVencimento,
 p.data_pagamento AS DataPagamento,p.valor_com_juros_centavos/100.0 AS ValorComJuros,
 p.valor_pago_centavos/100.0 AS ValorPago,p.bolsa AS Bolsa,p.forma_cobranca AS FormaCobranca,
 p.situacao AS Situacao,p.situacao_aluno AS SituacaoAluno,p.turma_nome AS Turma,c.nome AS Curso,
 p.nome_atendente AS NomeAtendente,p.data_inicio AS DataInicio,p.data_termino AS DataTermino,
 p.nome_operadora_cartao AS NomeOperadoraCartao,p.tipo_contrato AS TipoContrato,
 p.semestre_referencia AS SemestreReferencia,u.nome AS unidade,p.estagio AS Estagio,
 p.desconto_estimado_bp/100.0 AS DescontoEstimado,p.pacote_estimado AS PacoteEstimado,
 p.parcelamento_estimado AS ParcelamentoEstimado,p.resultado_estimativa AS ResultadoEstimativa,
 p.fonte_estimativa AS FonteEstimativa
FROM parcela p JOIN unidade u ON u.id=p.unidade_id
JOIN curso c ON c.id=p.curso_id;
