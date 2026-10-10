"""Testes de regressão de estimativas de desconto e persistência dos resultados.

Os cenários usam dados fictícios; não precisam acessar o ERP nem a base de produção."""
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import closing
import sqlite3
import pandas as pd
from core.descontos import estimar_descontos, bolsa_exibida, CAMPOS
from core.catalogo import classificar
from core import database as db


def referencia():
    precos={'English 1-3':'1000','English 4-6':'1100','English 7-9':'1200','English 10-11':'1300',
            'English C 1-2':'1400','TEACHERS':'1500','Kids':'600','Baby':'600','Preteen':'700','Español':'1000','VIP':'2000'}
    regiao=dict(unidades=['Teste'],precos=precos,descontos=[0,20,25,26,28,30,35,40,43],
                parcelas_semestrais=list(range(2,10)),parcelas_anuais=list(range(7,15)),parcelas_vip=[2,3,7])
    return dict(ano=2026,fonte='Tabela fictícia de testes',regioes={'Teste':regiao})


def lote(n=6,valor=125,stages=('English A 3',),anual=False):
    rows=[]
    for i in range(1,n+1):
        stage=stages[0] if len(stages)==1 or i<=n//2 else stages[1]
        rows.append(dict(unidade='Teste',NumeroMatricula='1',NumeroParcela=i,Sacado='Aluno fictício',
                         Turma=f'2026 - {stage}.1',Estagio=stage,Curso='ENGLISH COURSE',
                         TipoContrato='Anual' if anual else 'Semestral',DataInicio='2026-01-10',
                         DataTermino='2026-12-10' if anual else '2026-06-10',DataVencimento='2026-02-10',
                         DataPagamento=None,ValorComDesconto=valor,ValorPago=0,Situacao='Pendente',
                         SemestreReferencia='1º Semestre',Bolsa=None))
    return pd.DataFrame(rows)


class DescontosTests(unittest.TestCase):
    """Verifica os cenários de Descontos usando dados de teste e dependências isoladas."""
    def estimar(self,d):return estimar_descontos(d,2026,referencia())
    def test_semestral(self):
        d=self.estimar(lote())
        self.assertTrue(d.DescontoEstimado.eq(25).all())
        self.assertTrue(d.ParcelamentoEstimado.eq(6).all())
        self.assertTrue(d.PacoteEstimado.str.startswith('Semestral').all())
    def test_anual_dois_estagios(self):
        d=self.estimar(lote(12,131.25,('English A 3','English 4'),True))
        self.assertTrue(d.DescontoEstimado.eq(25).all())
        self.assertTrue(d.PacoteEstimado.eq('Anual — English 3 + English 4').all())
    def test_t_e_i_preco_equivalente(self):
        for stage in ['English T 3','English I4','English T I3']:
            valor=125 if stage!='English I4' else 137.5
            self.assertTrue(self.estimar(lote(valor=valor,stages=(stage,))).DescontoEstimado.eq(25).all())
    def test_anual_um_estagio_identifica_segundo_como_inferido(self):
        d=self.estimar(lote(12,131.25,('English A 3',),True))
        self.assertTrue(d.DescontoEstimado.eq(25).all())
        self.assertTrue(d.ResultadoEstimativa.str.contains('inferido').all())
    def test_mesmo_preco_de_pacotes_diferentes_gera_ambiguidade(self):
        d=self.estimar(lote(12,125,('English 2',),True))
        self.assertTrue(d.DescontoEstimado.isna().all())
        self.assertTrue(d.ResultadoEstimativa.eq('Correspondência ambígua').all())
    def test_duplicatas_nao_sao_unidas_como_contrato(self):
        base=lote();d=self.estimar(pd.concat([base,base],ignore_index=True))
        self.assertEqual(len(d),12)
        self.assertTrue(d.DescontoEstimado.isna().all())
        self.assertTrue(d.ResultadoEstimativa.str.contains('repetidas').all())
    def test_dois_contratos_mesmo_aluno_datas_diferentes(self):
        primeiro=lote();segundo=lote(valor=137.5,stages=('English 4',))
        segundo['DataInicio']='2026-07-10';segundo['DataTermino']='2026-12-10'
        d=self.estimar(pd.concat([primeiro,segundo],ignore_index=True))
        self.assertTrue(d.DescontoEstimado.eq(25).all())
    def test_unidades_isoladas_e_preco_especifico(self):
        ref=referencia();regiao=referencia()['regioes']['Teste'];regiao['unidades']=['Outra']
        regiao['precos']['English 1-3']='900';ref['regioes']['Outra']=regiao
        base=lote();outra=lote(valor=112.5);outra['unidade']='Outra'
        d=estimar_descontos(pd.concat([base,outra],ignore_index=True),2026,ref)
        self.assertTrue(d.DescontoEstimado.eq(25).all())
    def test_bolsa_do_erp_e_valores_preservados(self):
        base=lote();base['Bolsa']='Convênio informado'
        d=self.estimar(base)
        pd.testing.assert_frame_equal(d[list(base.columns)],base)
        self.assertTrue(bolsa_exibida(d).eq('Convênio informado').all())
    def test_valor_pago_nao_determina_desconto(self):
        base=lote();base['ValorPago']=9999
        self.assertTrue(self.estimar(base).DescontoEstimado.eq(25).all())
    def test_carga_parcial_nao_vira_contrato_semestral(self):
        base=lote(12,125,('English 2',),True).iloc[:6]
        self.assertTrue(self.estimar(base).DescontoEstimado.isna().all())
    def test_sequencia_incompleta_ou_data_ausente(self):
        for base in [lote().iloc[1:],lote().assign(DataInicio=None),lote().assign(DataTermino=None)]:
            self.assertTrue(self.estimar(base).DescontoEstimado.isna().all())
    def test_arredondamento_com_ajuste_final(self):
        base=lote(n=7,valor=107.14);base.loc[6,'ValorComDesconto']=107.16
        self.assertTrue(self.estimar(base).DescontoEstimado.eq(25).all())
    def test_cobranca_distinta_nao_e_arredondamento(self):
        base=lote();base.loc[2,'ValorComDesconto']=200
        self.assertTrue(self.estimar(base).DescontoEstimado.isna().all())
    def test_canceladas_e_bolsista_zero_nao_estimados(self):
        for base in [lote().assign(Situacao='Cancelada'),lote(valor=0)]:
            self.assertTrue(self.estimar(base).DescontoEstimado.isna().all())
    def test_sem_referencia_ou_ano_diferente(self):
        with patch('core.descontos.carregar_precos',return_value=None):
            for base in [lote(),lote().assign(Turma='2027 - English A3')]:
                d=estimar_descontos(base)
                self.assertTrue(d.ResultadoEstimativa.str.contains('indisponível').all())
    def test_vip_sem_desconto(self):
        base=lote(n=2,valor=1000,stages=('English A VIP 1',))
        self.assertTrue(self.estimar(base).DescontoEstimado.eq(0).all())
    def test_persistencia_e_carregamento_dos_campos(self):
        with TemporaryDirectory() as temp:
            path=Path(temp)/'teste.db';base=self.estimar(lote())
            ok,msg=db.salvar_carga_completa({'Teste':base},['Teste'],path)
            self.assertTrue(ok,msg)
            saved=db.carregar_dados_auditados(path)
            self.assertTrue(saved.DescontoEstimado.eq(25).all())
            self.assertTrue(saved.ParcelamentoEstimado.eq(6).all())
            self.assertEqual(len(saved),len(base))
    def test_migracao_v3_preserva_linhas_e_valores(self):
        sql=db.SCHEMA_PATH.read_text(encoding='utf-8')
        # Reconstitui o esquema anterior, sem novos campos.
        inicio=sql.index(' desconto_estimado_bp');fim=sql.index(' UNIQUE(',inicio)
        sql=sql[:inicio]+sql[fim:]
        inicio=sql.index(',\n p.desconto_estimado_bp');fim=sql.index('\nFROM parcela',inicio)
        sql=sql[:inicio]+sql[fim:]
        with TemporaryDirectory() as temp:
            path=Path(temp)/'anterior.db'
            with closing(sqlite3.connect(path)) as c:
                c.executescript(sql)
                c.execute("INSERT INTO unidade VALUES (1,'Teste')")
                c.execute("INSERT INTO curso VALUES (1,'ENGLISH COURSE')")
                c.execute("INSERT INTO aluno VALUES (1,'1','Aluno fictício')")
                c.execute("INSERT INTO turma VALUES (1,'2026 - English A3',1)")
                c.execute("INSERT INTO parcela(id,unidade_id,linha_origem,matricula,turma_nome,numero,sacado,tipo_contrato,data_inicio,data_termino,data_vencimento,valor_com_desconto_centavos,valor_pago_centavos,situacao,semestre_referencia,curso_id,estagio) VALUES(1,1,1,'1','2026 - English A3',1,'Aluno fictício','Semestral','2026-01-10','2026-06-10','2026-02-10',12500,0,'Pendente','1º Semestre',1,'English A 3')")
                c.execute('PRAGMA user_version=3');c.commit()
            with closing(db.get_connection(path)) as c:
                self.assertEqual(c.execute('PRAGMA user_version').fetchone()[0],4)
                self.assertEqual(c.execute('SELECT id,valor_com_desconto_centavos FROM parcela').fetchone(),(1,12500))
                self.assertEqual(c.execute('PRAGMA foreign_key_check').fetchall(),[])
    def test_etl_chama_estimativa_e_nao_sobrescreve_bolsa(self):
        from core.etl import tratar_contas_receber
        base=lote();base['Bolsa']='Convênio ERP'
        with patch('core.descontos.carregar_precos',return_value=referencia()):
            d=tratar_contas_receber(base,'Teste',2026)
        self.assertTrue(d.DescontoEstimado.eq(25).all())
        self.assertTrue(d.Bolsa.eq('Convênio ERP').all())
