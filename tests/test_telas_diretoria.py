"""Testes de regressão de telas, tabelas grandes, agrupamentos e totais.

Os cenários usam dados fictícios; não precisam acessar o ERP nem a base de produção."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from test_analise_diretoria import exemplo


@unittest.skipUnless(importlib.util.find_spec('streamlit'), 'Streamlit não instalado neste ambiente')
class TelasTests(unittest.TestCase):
    """Verifica os cenários de Telas usando dados de teste e dependências isoladas."""
    def app(self,pagina,df=None):
        from streamlit.testing.v1 import AppTest
        source=Path(__file__).resolve().parents[1]/'views'/pagina
        with patch('core.database.carregar_dados_auditados',return_value=exemplo() if df is None else df):
            app=AppTest.from_file(str(source),default_timeout=30).run()
        self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
        return app
    def test_todas_paginas_abrem_sem_erros(self):
        for pagina in ['dashboard.py','valores_alunos.py','valores_semestrais.py','devedores.py','turmas.py']:
            with self.subTest(pagina=pagina):self.app(pagina)
    def test_filtro_de_curso_e_agrupamento(self):
        app=self.app('turmas.py')
        with patch('core.database.carregar_dados_auditados',return_value=exemplo()):
            curso=next(e for e in app.selectbox if e.label=='Curso')
            curso.select('KIDS´ COURSE').run()
            self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
            self.assertEqual(app.metric[0].value,'1')
            agrupamento=next(e for e in app.multiselect if e.label=='Agrupar painel por')
            agrupamento.set_value(['Curso']).run()
            self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
    def test_pagina_vazia_apresenta_aviso(self):
        for pagina in ['valores_alunos.py','devedores.py','turmas.py','valores_semestrais.py']:
            with self.subTest(pagina=pagina):
                app=self.app(pagina,exemplo().iloc[:0]);self.assertGreater(len(app.info),0)


@unittest.skipUnless(importlib.util.find_spec('streamlit'), 'Streamlit não instalado neste ambiente')
class RenderizacaoTests(unittest.TestCase):
    """Verifica os cenários de Renderizacao usando dados de teste e dependências isoladas."""
    app = TelasTests.app
    def test_turmas_mostra_resumo_e_detalhe_somente_apos_selecao(self):
        app=self.app('turmas.py')
        self.assertEqual(len(app.dataframe),1)
        with patch('core.database.carregar_dados_auditados',return_value=exemplo()):
            seletor=next(e for e in app.selectbox if e.label=='Turma para consultar alunos')
            seletor.set_value(('A','2026/1 - English 4.1')).run()
            self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
            self.assertEqual(len(app.dataframe),2)
            self.assertEqual(len(app.dataframe[1].value),2)
            self.assertNotIn('Turma',app.dataframe[1].value.columns)
    def test_tabela_grande_sem_styler_preserva_numeros(self):
        from streamlit.testing.v1 import AppTest
        source="""import pandas as pd
from views.componentes import tabela
n=12500
df=pd.DataFrame({'Previsto':[123.45]*n,'Recebido':[100.0]*n,'DataInicio':pd.to_datetime(['2026-01-01']*n),**{f'Campo{i}':['exemplo']*n for i in range(21)}})
tabela(df,'teste_grande')
"""
        app=AppTest.from_string(source,default_timeout=30).run()
        self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
        self.assertEqual(app.dataframe[0].value.size,300000)
        self.assertEqual(len(app.dataframe[0].value),12500)
        self.assertEqual(app.dataframe[0].value['Previsto'].dtype.kind,'f')


@unittest.skipUnless(importlib.util.find_spec('streamlit'), 'Streamlit não instalado neste ambiente')
class AgrupamentoTabelasTests(unittest.TestCase):
    """Verifica os cenários de AgrupamentoTabelas usando dados de teste e dependências isoladas."""
    app=TelasTests.app
    def test_painel_por_curso_mantem_colunas_e_separa_tabelas(self):
        app=self.app('turmas.py')
        original=app.dataframe[0].value.copy()
        with patch('core.database.carregar_dados_auditados',return_value=exemplo()):
            next(e for e in app.multiselect if e.label=='Agrupar painel por').set_value(['Curso']).run()
        self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
        self.assertEqual(len(app.dataframe),2)
        self.assertEqual(sum(len(e.value) for e in app.dataframe),len(original))
        for frame in app.dataframe:
            self.assertEqual(list(frame.value.columns),list(original.columns))
            self.assertEqual(frame.value['Curso'].nunique(),1)
        self.assertAlmostEqual(sum(e.value.Recebido.sum() for e in app.dataframe),original.Recebido.sum())
    def test_detalhamento_em_outras_paginas_tambem_separa(self):
        for pagina in ['valores_alunos.py','valores_semestrais.py']:
            with self.subTest(pagina=pagina):
                app=self.app(pagina)
                original=app.dataframe[1].value.copy()
                with patch('core.database.carregar_dados_auditados',return_value=exemplo()):
                    seletores=[e for e in app.multiselect if e.label=='Agrupar por']
                    seletores[-1].set_value(['Curso']).run()
                self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
                self.assertEqual(len(app.dataframe),3)
                for frame in app.dataframe[1:]:self.assertEqual(list(frame.value.columns),list(original.columns))


@unittest.skipUnless(importlib.util.find_spec('streamlit'), 'Streamlit não instalado neste ambiente')
class TotaisRenderizadosTests(unittest.TestCase):
    """Verifica os cenários de TotaisRenderizados usando dados de teste e dependências isoladas."""
    app=TelasTests.app
    def test_cada_tabela_de_curso_tem_totais(self):
        app=self.app('turmas.py')
        with patch('core.database.carregar_dados_auditados',return_value=exemplo()):
            next(e for e in app.multiselect if e.label=='Agrupar painel por').set_value(['Curso']).run()
        self.assertEqual(len(app.exception),0,[e.message for e in app.exception])
        self.assertEqual(len([e for e in app.metric if e.label=='Valor inadimplente']),len(app.dataframe))
        self.assertEqual(len([e for e in app.metric if e.label=='Total de alunos']),len(app.dataframe))
        valores=[e.value for e in app.metric if e.label=='Valor inadimplente']
        self.assertIn('R$ 200,00',valores)
        self.assertIn('R$ 0,00',valores)
