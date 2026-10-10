"""Testes de regressão de tratamento dos relatórios e publicação de cargas completas.

Os cenários usam dados fictícios; não precisam acessar o ERP nem a base de produção."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock,patch
import time,traceback
import pandas as pd
from core.etl import tratar_contas_receber,process_contas_receber,clean_currency,deduzir_estagio,STAGE_COURSES
from core.database import REQUIRED

def row():
    return dict(NumeroMatricula='100',NumeroParcela=1,Sacado='Aluno fictício',
                Turma='2026 - English Course',Curso=None,
                DataInicio='2026-01-10',DataVencimento='2026-02-10',
                ValorComDesconto=123.45,ValorPago=0,Situacao='Pendente')

class EtlTests(unittest.TestCase):
    """Verifica os cenários de Etl usando dados de teste e dependências isoladas."""
    def process(self,rows):return tratar_contas_receber(pd.DataFrame(rows),'A',2026)
    def test_campos_crus_sao_tratados_sem_novos_codigos(self):
        df=self.process([row()]);self.assertTrue(set(REQUIRED)<=set(df.columns))
        self.assertEqual(df.iloc[0]['Curso'],'ENGLISH COURSE')
        self.assertEqual(df.iloc[0]['TipoContrato'],'Semestral')
        self.assertEqual(df.iloc[0]['ValorComDesconto'],123.45)
        self.assertEqual(clean_currency('R$ 1.234,56'),1234.56)
    def test_colunas_totalmente_vazias_no_excel(self):
        r=dict(row(),Curso=float('nan'),Bolsa=float('nan'),ValorPago=0.0,Situacao='Quitada')
        df=self.process([r])
        self.assertEqual(df.iloc[0]['Curso'],'ENGLISH COURSE')
        self.assertEqual(df.iloc[0]['Bolsa'],'Bolsista')
    def test_preserva_classificacoes_fornecidas(self):
        df=self.process([dict(row(),Curso='Curso informado',TipoContrato='Anual')])
        self.assertEqual(df.iloc[0]['Curso'],'Curso informado');self.assertEqual(df.iloc[0]['TipoContrato'],'Anual')
    def test_classificacao_herdada_e_semestre_financeiro(self):
        rows=[dict(row(),NumeroParcela=i,DataVencimento='2026-08-10') for i in range(1,7)]
        df=self.process(rows);self.assertTrue(df.TipoContrato.eq('Anual').all())
        self.assertTrue(df.SemestreReferencia.eq('2º Semestre').all())
    def test_estagios_da_lista_completa(self):
        self.assertEqual(len(STAGE_COURSES),83)
        for stage,course in STAGE_COURSES.items():
            with self.subTest(stage=stage):
                self.assertEqual(deduzir_estagio(f'2/2026 - {stage}.1'),stage)
                df=self.process([dict(row(),Turma=f'2026 - {stage}.1')])
                self.assertEqual(df.iloc[0].Estagio,stage)
                self.assertEqual(df.iloc[0].Curso,course)
        for stage in ['English 12','Español 10','Español T1','Español A1','English 111',None]:
            self.assertIsNone(deduzir_estagio(stage))
    def test_estagio_no_tratamento(self):
        df=self.process([dict(row(),Turma='2/2026 - English Course - English 10.1')])
        self.assertEqual(df.iloc[0].Estagio,'English 10')
    def test_sem_turma_inicio_e_termino_nao_descarta(self):
        df=self.process([dict(row(),Turma=None,DataInicio=None,DataTermino=None)])
        self.assertEqual(len(df),1)
        self.assertTrue(pd.isna(df.iloc[0].Turma));self.assertTrue(pd.isna(df.iloc[0].DataInicio))
        self.assertTrue(pd.isna(df.iloc[0].Estagio))
        self.assertEqual(df.iloc[0].SemestreReferencia,'Não informado')
        self.assertEqual(df.iloc[0].TipoContrato,'Não informado')
    def test_moeda_com_casas_excedentes_arredonda(self):
        self.assertEqual(clean_currency('1.005'),1.01)
        self.assertEqual(clean_currency('1,004'),1.0)
        self.assertEqual(clean_currency(1.2349999999999999),1.23)
    def test_falta_de_campo_financeiro_rejeitada(self):
        r=row();del r['ValorPago']
        with self.assertRaisesRegex(ValueError,'ValorPago'):self.process([r])
    def test_data_iso_e_filtro_ano(self):
        df=self.process([dict(row(),DataVencimento='2026-08-05'),dict(row(),Turma='2025 - English Course')])
        self.assertEqual(len(df),1);self.assertEqual(df.iloc[0].DataVencimento.month,8)
    def test_moeda_invalida_nao_vira_zero(self):
        for value in ('abc',None,-1):
            with self.assertRaises(ValueError):self.process([dict(row(),ValorPago=value)])
    def test_esquema_vazio_aceito(self):
        df=tratar_contas_receber(pd.DataFrame(columns=REQUIRED),'A',2026)
        self.assertTrue(df.empty)
    def test_detecta_cabecalho_sem_linhas_de_titulo(self):
        with patch('core.etl.pd.read_excel',side_effect=[pd.DataFrame(columns=['ruim']),pd.DataFrame([row()])]):
            self.assertEqual(len(process_contas_receber('fake','A',2026)),1)

class SincronizacaoTests(unittest.TestCase):
    """Verifica os cenários de Sincronizacao usando dados de teste e dependências isoladas."""
    def run_sync(self, fail=False):
        # Carrega somente a função orquestradora, sem importar Playwright,
        # configurações privadas ou abrir navegador.
        source = Path(__file__).resolve().parents[1] / 'core' / 'rpa.py'
        tree = ast.parse(source.read_text(encoding='utf-8-sig'))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'sincronizar_todas_as_unidades_sponte')
        logger = MagicMock()
        publish = MagicMock(return_value=(True, 'Carga concluída'))
        df = pd.DataFrame([row()])
        process = MagicMock(side_effect=[df, ValueError('Falha de extração simulada') if fail else df])
        namespace = dict(Path=Path, time=time, traceback=traceback,
                         configurar_logger_execucao=MagicMock(return_value=(logger, Path('fake.log'))),
                         sync_playwright=MagicMock(), UNIDADES_DOMINIOS={'A': '@a', 'B': '@b'},
                         URL_CONTAS_RECEBER='https://example.invalid', abrir_relatorio=MagicMock(), autenticar_se_necessario=MagicMock(),
                         extrair_contas_receber_unidade=MagicMock(return_value=SimpleNamespace(stat=lambda: SimpleNamespace(st_size=100))),
                         process_contas_receber=process, validar_lote=MagicMock(), salvar_carga_completa=publish)
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
        result = namespace[node.name]('teste', 'senha fictícia', 2026)
        return result, publish

    def test_falha_de_unidade_nao_publica(self):
        result, publish = self.run_sync(fail=True)
        self.assertFalse(result[0]); publish.assert_not_called()
        self.assertIn('preservada', result[1])

    def test_publica_uma_vez_com_todas_unidades(self):
        result, publish = self.run_sync()
        self.assertTrue(result[0]); publish.assert_called_once()
        self.assertEqual(set(publish.call_args.args[0]), {'A', 'B'})

if __name__ == '__main__':
    unittest.main()


class CursoNormalizadoTests(unittest.TestCase):
    """Verifica os cenários de CursoNormalizado usando dados de teste e dependências isoladas."""
    def test_variantes_de_curso_convergem_sem_trocar_curso_desconhecido(self):
        from core.etl import normalizar_curso
        for value in ['ENGLISH COURSE','ENGLISH COURSE',' english course ']:
            self.assertEqual(normalizar_curso(value),'ENGLISH COURSE')
        self.assertEqual(normalizar_curso('KIDS´ COURSE'),'KIDS´ COURSE')
        self.assertEqual(normalizar_curso('ESPAÑOL'),'ESPAÑOL')
        self.assertEqual(normalizar_curso('Curso Especial'),'Curso Especial')
        self.assertIsNone(normalizar_curso(None))


class EstagiosAvancadosTests(unittest.TestCase):
    """Verifica os cenários de EstagiosAvancados usando dados de teste e dependências isoladas."""
    def test_aliases_preservam_variantes(self):
        aliases={'English A1.1':'English A 1','English T2.1':'English T 2',
                 'English I 10.1':'English I10','English T I 1.1':'English T I1',
                 'english a vip c 1 - 2.1':'English A VIP C 1-2',
                 'ESPANOL VIP 9.1':'Español VIP 9','Teacher': 'TEACHERS'}
        for value,stage in aliases.items(): self.assertEqual(deduzir_estagio(value),stage)
    def test_nao_aceita_niveis_ou_combinacoes_ausentes(self):
        for value in ['English A5','English T11','English VIP 3','English I3','English A 1-3','Kids A1','Baby T1']:
            self.assertIsNone(deduzir_estagio(value))
    def test_estagio_desconhecido_preserva_parcela(self):
        df=tratar_contas_receber(pd.DataFrame([dict(row(),Turma='2026 - English 12.1')]),'A',2026)
        self.assertEqual(len(df),1)
        self.assertTrue(pd.isna(df.iloc[0].Estagio))
        self.assertEqual(df.iloc[0].ValorComDesconto,123.45)


class NomesExportadosTests(unittest.TestCase):
    """Verifica os cenários de NomesExportados usando dados de teste e dependências isoladas."""
    def test_aliases_do_csv(self):
        from core.catalogo import normalizar_curso
        for value,stage,course in [('BABY CLASS 6.50','BABY 6','BABY CLASS'),
                                  ('Espanhol 2.30','Español 2','ESPAÑOL'),
                                  ('ENGLIISAH 6.2','English 6','ENGLISH COURSE')]:
            self.assertEqual(deduzir_estagio(value),stage)
            self.assertEqual(normalizar_curso(value),course)
    def test_catalogo_nao_inventa_niveis_nao_informados(self):
        for value in ['English T10.30','ENGLISH12.6','ENGLISH A 5.2','ENGLISH T 5.2']:
            self.assertIsNone(deduzir_estagio(value))


class EstagiosProducaoTests(unittest.TestCase):
    """Verifica os cenários de EstagiosProducao usando dados de teste e dependências isoladas."""
    def test_turmas_enviadas_preservam_nivel_e_variante(self):
        casos={'1/2026 - English T9.30 IGUATEMI':'English T 9',
               '1/2026 ENGLISH1.6':'English 1',
               '2/2026  ENGLISH 2.2':'English 2',
               '2/2026 ENGLISH2.50 PARALELA':'English 2',
               '2/2026 ENGLISH A 4.2':'English A 4',
               '2/2026 ENGLISH T 4.2':'English T 4'}
        for turma,stage in casos.items():
            self.assertEqual(deduzir_estagio(turma),stage)
            df=tratar_contas_receber(pd.DataFrame([dict(row(),Turma=turma)]),'A',2026)
            self.assertEqual(df.iloc[0].Estagio,stage)
            self.assertEqual(df.iloc[0].Curso,'ENGLISH COURSE')
    def test_turma_ausente_nao_inventa_estagio(self):
        self.assertIsNone(deduzir_estagio('Não informado'))
