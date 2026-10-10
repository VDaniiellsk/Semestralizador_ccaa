"""Testes de regressão de bloqueio da sincronização e repetição limitada da navegação.

Os cenários usam dados fictícios; não precisam acessar o ERP nem a base de produção."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch
from core import sync_runtime


class RuntimeTests(unittest.TestCase):
    """Verifica os cenários de Runtime usando dados de teste e dependências isoladas."""
    def test_recarrega_dependencias_antes_de_sincronizar(self):
        run=MagicMock(return_value=(True,'ok',Path('fake.log')))
        modules={name:SimpleNamespace(sincronizar_todas_as_unidades_sponte=run) for name in ('core.database','core.etl','core.rpa')}
        with patch.object(sync_runtime.importlib,'invalidate_caches') as invalidate, patch.object(sync_runtime.importlib,'import_module',side_effect=modules.get) as load, patch.object(sync_runtime.importlib,'reload',side_effect=lambda module:module) as reload:
            self.assertTrue(sync_runtime.sincronizar_atualizado(ano_referencia=2026)[0])
        invalidate.assert_called_once()
        self.assertEqual([c.args[0] for c in load.call_args_list],list(modules))
        self.assertEqual(reload.call_count,3)
        run.assert_called_once_with(ano_referencia=2026)

    def test_impede_sincronizacoes_simultaneas(self):
        with sync_runtime._SYNC_LOCK:
            with self.assertRaisesRegex(RuntimeError,'em andamento'):
                sync_runtime.sincronizar_atualizado()

    def test_libera_bloqueio_apos_erro_de_carregamento(self):
        with patch.object(sync_runtime.importlib,'import_module',side_effect=RuntimeError('erro simulado')):
            with self.assertRaises(RuntimeError):sync_runtime.sincronizar_atualizado()
        self.assertFalse(sync_runtime._SYNC_LOCK.locked())


class NavigationTests(unittest.TestCase):
    """Verifica os cenários de Navigation usando dados de teste e dependências isoladas."""
    def load_navigation(self):
        source=Path(__file__).resolve().parents[1]/'core/rpa.py'
        tree=ast.parse(source.read_text(encoding='utf-8-sig'))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='abrir_relatorio')
        namespace=dict(URL_CONTAS_RECEBER='https://example.invalid',PlaywrightTimeoutError=TimeoutError,time=SimpleNamespace(sleep=MagicMock()))
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),namespace)
        return namespace

    def test_timeout_repete_somente_navegacao(self):
        ns=self.load_navigation();page=MagicMock();page.goto.side_effect=[TimeoutError(),None]
        ns['abrir_relatorio'](page,MagicMock())
        self.assertEqual(page.goto.call_count,2);ns['time'].sleep.assert_called_once_with(3)

    def test_segundo_timeout_e_propagado(self):
        ns=self.load_navigation();page=MagicMock();page.goto.side_effect=TimeoutError()
        with self.assertRaises(TimeoutError):ns['abrir_relatorio'](page,MagicMock())
        self.assertEqual(page.goto.call_count,2)

    def test_erro_diferente_nao_repete(self):
        ns=self.load_navigation();page=MagicMock();page.goto.side_effect=ValueError('erro')
        with self.assertRaises(ValueError):ns['abrir_relatorio'](page,MagicMock())
        self.assertEqual(page.goto.call_count,1)
