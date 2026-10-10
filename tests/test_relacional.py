"""Testes de regressão de integridade do banco, migrações e preservação da carga anterior.

Os cenários usam dados fictícios; não precisam acessar o ERP nem a base de produção."""
import copy
import tempfile
import sqlite3
from unittest.mock import patch
import unittest
from contextlib import closing
from pathlib import Path
import pandas as pd
from core import database as db

def registro(unit='A',numero=1,turma='2026 Turma 1'):
    return dict(unidade=unit,NumeroMatricula='100',NumeroParcela=numero,Sacado='Aluno fictício',
                SituacaoAluno='Ativo',Turma=turma,Curso='Curso fictício',TipoContrato='Semestral',
                DataInicio='2026-01-01',DataTermino='2026-12-31',DataVencimento='2026-02-10',
                DataPagamento=None,ValorComDesconto=123.45,ValorPago=0.0,ValorComJuros=125.5,
                Situacao='Pendente',SemestreReferencia='1º Semestre',Bolsa=None,FormaCobranca='Boleto')

class RelacionalTests(unittest.TestCase):
    """Verifica os cenários de Relacional usando dados de teste e dependências isoladas."""
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.path=Path(temp.name)/'teste.db'
        self.lotes={'A':pd.DataFrame([registro(),registro(numero=2)]),'B':pd.DataFrame([registro('B')])}
        self.assertTrue(self.save()[0])
    def save(self,lotes=None):return db.salvar_carga_completa(self.lotes if lotes is None else lotes,['A','B'],self.path)
    def read(self):return db.carregar_dados_auditados(self.path)
    def test_importa_sem_codigo_contrato_e_preserva_colunas(self):
        df=self.read();self.assertEqual(len(df),3);self.assertAlmostEqual(df.ValorComDesconto.sum(),370.35)
        self.assertTrue(set(registro())<=set(df.columns))
        with closing(db.get_connection(self.path)) as c:
            self.assertEqual(c.execute('SELECT count(*) FROM aluno').fetchone()[0],2)
            self.assertFalse(c.execute('PRAGMA foreign_key_check').fetchall())
    def test_preserva_linhas_identicas_e_numero_repetido(self):
        lotes=copy.deepcopy(self.lotes)
        lotes['A']=pd.DataFrame([registro(),registro(),registro(turma='2026 Turma 2')])
        self.assertTrue(self.save(lotes)[0]);self.assertEqual(len(self.read()),4)
        with closing(db.get_connection(self.path)) as c:
            self.assertEqual(c.execute('SELECT count(DISTINCT id) FROM parcela').fetchone()[0],4)
    def test_reimporta_sem_acumular(self):
        self.assertTrue(self.save()[0]);self.assertEqual(len(self.read()),3)
    def test_carga_parcial_ou_vazia_preserva(self):
        for lotes in ({'A':self.lotes['A']},{u:df.iloc[:0] for u,df in self.lotes.items()}):
            self.assertFalse(self.save(lotes)[0]);self.assertEqual(len(self.read()),3)
    def test_unidade_vazia_remove_registros_antigos(self):
        lotes=copy.deepcopy(self.lotes);lotes['B']=lotes['B'].iloc[:0]
        self.assertTrue(self.save(lotes)[0]);self.assertEqual(len(self.read()),2)
    def test_falha_na_gravacao_restaura_carga(self):
        with closing(db.get_connection(self.path)) as c,c:
            c.execute("CREATE TRIGGER falha BEFORE INSERT ON parcela BEGIN SELECT RAISE(ABORT,'teste'); END")
        self.assertFalse(self.save()[0]);self.assertEqual(len(self.read()),3)
    def test_turma_curso_conflitante_preserva(self):
        lotes=copy.deepcopy(self.lotes);lotes['A'].loc[1,'Curso']='Outro curso'
        self.assertFalse(self.save(lotes)[0]);self.assertEqual(len(self.read()),3)
    def test_valores_datas_unidade_invalidos_preservam(self):
        for field,value in [('ValorPago',-1),('ValorPago',float('inf')),('DataInicio','2026-02-30'),('unidade','C')]:
            with self.subTest(field=field):
                lotes=copy.deepcopy(self.lotes);lotes['A'].loc[0,field]=value
                self.assertFalse(self.save(lotes)[0]);self.assertEqual(len(self.read()),3)
    def test_update_sql_reflete_na_view(self):
        with closing(db.get_connection(self.path)) as c,c:
            c.execute("UPDATE parcela SET valor_pago_centavos=12345,situacao='Quitada' WHERE id=1")
        self.assertAlmostEqual(self.read().ValorPago.sum(),123.45)
    def test_sem_turma_datas_e_estagio_preserva_parcela(self):
        lotes=copy.deepcopy(self.lotes)
        lotes['A'].loc[0,['Turma','DataInicio','DataTermino']]=None
        lotes['A'].loc[0,'Curso']='Curso informado'
        self.assertTrue(self.save(lotes)[0])
        df=self.read();self.assertEqual(len(df),3)
        self.assertTrue(pd.isna(df.iloc[0].Turma));self.assertTrue(pd.isna(df.iloc[0].DataInicio))
        self.assertEqual(df.iloc[0].Curso,'Curso informado')
    def test_arredondamento_e_estagio_persistidos(self):
        lotes=copy.deepcopy(self.lotes)
        lotes['A']['Estagio']='English 10'
        lotes['A'].loc[0,'ValorPago']=1.005
        self.assertTrue(self.save(lotes)[0])
        df=self.read();self.assertEqual(df.iloc[0].ValorPago,1.01)
        self.assertEqual(df.iloc[0].Estagio,'English 10')
    def legacy(self):
        # Esquema anterior reduzido, com as mesmas cinco entidades e view.
        p=self.path.with_name('anterior.db')
        with closing(sqlite3.connect(p)) as c, c:
            c.executescript("""
            CREATE TABLE unidade(id INTEGER PRIMARY KEY,nome TEXT);INSERT INTO unidade VALUES(1,'A');
            CREATE TABLE aluno(id INTEGER PRIMARY KEY);CREATE TABLE curso(id INTEGER PRIMARY KEY);
            CREATE TABLE turma(id INTEGER PRIMARY KEY);
            CREATE TABLE parcela(NumeroParcela, Sacado, NumeroMatricula, ValorComDesconto, DataVencimento,
              DataPagamento, ValorComJuros, ValorPago, Bolsa, FormaCobranca, Situacao, SituacaoAluno,
              Turma, Curso, NomeAtendente, DataInicio, DataTermino, NomeOperadoraCartao, TipoContrato, SemestreReferencia, unidade);
            INSERT INTO parcela VALUES(1,'Aluno fictício','100',123.45,'2026-02-10',NULL,125.50,0,NULL,'Boleto','Pendente','Ativo',
              '2026 English 1.1','Curso fictício',NULL,'2026-01-01',NULL,NULL,'Semestral','1º Semestre','A');
            CREATE VIEW recebiveis_auditados AS SELECT * FROM parcela;PRAGMA user_version=2;
            """)
        return p
    def test_migracao_v2_preserva_dados(self):
        p=self.legacy();df=db.carregar_dados_auditados(p)
        self.assertEqual(len(df),1);self.assertEqual(df.iloc[0].ValorComDesconto,123.45)
        self.assertIn('Estagio',df.columns)
        with closing(db.get_connection(p)) as c:self.assertEqual(c.execute('PRAGMA user_version').fetchone()[0],4)
    def test_falha_na_migracao_preserva_esquema_e_dados(self):
        p=self.legacy()
        with patch.object(db,'_gravar',side_effect=sqlite3.OperationalError('falha simulada')):
            with self.assertRaises(sqlite3.OperationalError):db.get_connection(p)
        with closing(sqlite3.connect(p)) as c, c:
            self.assertEqual(c.execute('PRAGMA user_version').fetchone()[0],2)
            self.assertEqual(c.execute('SELECT count(*) FROM parcela').fetchone()[0],1)
            self.assertEqual(c.execute('SELECT ValorComDesconto FROM recebiveis_auditados').fetchone()[0],123.45)
    def test_base_antiga_bloqueada(self):
        for name in ('auditoria_financeira.db','auditoria_relacional.db'):
            with self.assertRaises(ValueError):db.get_connection(self.path.with_name(name))
