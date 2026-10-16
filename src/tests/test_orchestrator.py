"""Tests del Orchestrator.

IMPORTANTE: usan NullBrain para no gastar tokens.
"""
from src.orchestrator.core import Orchestrator
from src.orchestrator.brains import NullBrain


def _orq_test():
    return Orchestrator(brain=NullBrain())


def test_inicializacion():
    o = _orq_test()
    assert o.registry.contar() == 7


def test_recibir_objetivo():
    o = _orq_test()
    t = o.recibir_objetivo("probar simulacion")
    assert t["id"].startswith("TASK-")
    assert o.tasks.estadisticas()["total"] >= 1


def test_estado():
    o = _orq_test()
    e = o.estado()
    assert "agentes" in e
    assert e["agentes"] == 7
    assert "tareas" in e
    assert "memoria" in e


def test_panel_devuelve_string():
    o = _orq_test()
    p = o.panel()
    assert isinstance(p, str)
    assert "PANEL CEO" in p