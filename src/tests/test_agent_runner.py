"""Tests del AgentRunner."""
from src.orchestrator.core import Orchestrator
from src.orchestrator.agent_runner import AgentRunner


def test_runner_instancia_agentes():
    o = Orchestrator()
    r = AgentRunner(o)
    assert len(r.agentes) == 7


def test_runner_ejecuta_agente():
    o = Orchestrator()
    r = AgentRunner(o)
    resultado = r.ejecutar_agente("Director", {"descripcion": "probar algo"})
    assert resultado["agente"] == "Director"
    assert "subtareas" in resultado


def test_runner_rechaza_agente_inexistente():
    o = Orchestrator()
    r = AgentRunner(o)
    resultado = r.ejecutar_agente("NoExiste", {"descripcion": "test"})
    assert "error" in resultado


def test_runner_deniega_permiso():
    o = Orchestrator()
    r = AgentRunner(o)
    # Developer NO puede tocar main
    resultado = r.ejecutar_agente("Developer", {"accion": "tocar_main", "descripcion": "x"})
    assert "error" in resultado
    assert "denegado" in resultado["error"].lower() or "permiso" in resultado["error"].lower()


def test_runner_flujo_completo():
    o = Orchestrator()
    r = AgentRunner(o)
    flujo = r.ejecutar_flujo("Simular 30 dias de operacion")
    assert flujo["estado"] == "completado"
    assert len(flujo["pasos"]) >= 7
    agentes_ejecutados = [p["agente"] for p in flujo["pasos"]]
    assert "Director" in agentes_ejecutados
    assert "Arquitecto" in agentes_ejecutados
    assert "Developer" in agentes_ejecutados
    assert "Quantum_RD" in agentes_ejecutados
    assert "Tester" in agentes_ejecutados
    assert "Auditor" in agentes_ejecutados
    assert "Business" in agentes_ejecutados


def test_runner_guarda_en_memoria():
    o = Orchestrator()
    r = AgentRunner(o)
    antes = len(o.memory.buscar("resultado_agente"))
    r.ejecutar_agente("Director", {"descripcion": "probar memoria"})
    despues = len(o.memory.buscar("resultado_agente"))
    assert despues > antes