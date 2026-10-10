"""Atualiza os módulos de coleta antes de executar uma sincronização.

O bloqueio evita duas execuções simultâneas dentro deste processo; ele não
coordena aplicações abertas em outros processos ou computadores."""
import importlib
import threading

_SYNC_LOCK = threading.Lock()


def sincronizar_atualizado(**kwargs):
    """Recarrega banco, tratamento e coleta, executa a sincronização e libera o bloqueio mesmo após erro."""
    if not _SYNC_LOCK.acquire(blocking=False):
        raise RuntimeError('Já existe uma sincronização em andamento. Aguarde sua conclusão.')
    try:
        importlib.invalidate_caches()
        for name in ('core.database', 'core.etl', 'core.rpa'):
            module = importlib.reload(importlib.import_module(name))
        return module.sincronizar_todas_as_unidades_sponte(**kwargs)
    finally:
        _SYNC_LOCK.release()
