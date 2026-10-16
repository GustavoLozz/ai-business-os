"""Tests del AgentRunner.

IMPORTANTE: usan NullBrain para no gastar tokens.
"""
from src.orchestrator.core import Orchestrator
from src.orchestrator.agent_runner import AgentRunner
from src.orchestrator.brains import NullBrain


def _orq_test():
    return Orchestrator(brain=NullBrain())


def test_runner_instancia_agentes():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    assert len(r.agentes) == 7


def test_runner_ejecuta_agente():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    resultado = r.ejecutar_agente("Director", {"descripcion": "probar algo"})
    assert resultado["agente"] == "Director"
    assert "subtareas" in resultado


def test_runner_rechaza_agente_inexistente():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    resultado = r.ejecutar_agente("NoExiste", {"descripcion": "test"})
    assert "error" in resultado


def test_runner_deniega_permiso():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    resultado = r.ejecutar_agente("Developer", {"accion": "tocar_main", "descripcion": "x"})
    assert "error" in resultado


def test_runner_flujo_completo():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    flujo = r.ejecutar_flujo("Simular 30 dias de operacion")
    assert flujo["estado"] == "completado"
    assert len(flujo["pasos"]) >= 7
    agentes = [p["agente"] for p in flujo["pasos"]]
    assert "Director" in agentes
    assert "Business" in agentes


def test_runner_guarda_en_memoria():
    o = _orq_test()
    o.memory.resetear()
    r = AgentRunner(o, brain=NullBrain())
    antes = len(o.memory.buscar("resultado_agente"))
    r.ejecutar_agente("Director", {"descripcion": "probar memoria"})
    despues = len(o.memory.buscar("resultado_agente"))
    assert despues > antes