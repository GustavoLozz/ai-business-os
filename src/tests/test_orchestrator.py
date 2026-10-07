"""Tests del Orchestrator completo."""
from src.orchestrator.core import Orchestrator


def test_inicializacion():
    o = Orchestrator()
    assert o.registry.contar() == 7


def test_recibir_objetivo():
    o = Orchestrator()
    t = o.recibir_objetivo("probar simulacion")
    assert t["id"].startswith("TASK-")
    assert o.tasks.estadisticas()["total"] >= 1


def test_estado():
    o = Orchestrator()
    e = o.estado()
    assert "agentes" in e
    assert e["agentes"] == 7
    assert "tareas" in e
    assert "memoria" in e


def test_panel_devuelve_string():
    o = Orchestrator()
    p = o.panel()
    assert isinstance(p, str)
    assert "PANEL CEO" in p