"""Tests del registro de agentes."""
from src.orchestrator.agent_registry import AgentRegistry


def test_registrar_7_agentes():
    r = AgentRegistry()
    assert r.contar() == 7


def test_obtener_agente():
    r = AgentRegistry()
    assert r.obtener("Director") is not None
    assert r.obtener("NoExiste") is None


def test_activar():
    r = AgentRegistry()
    assert r.activar("Director")
    assert r.obtener("Director")["estado"] == "activo"