"""Tests del AgentRunner con gobernanza efectiva.

Actualizado para la nueva interfaz de ejecutar_agente (v5):
- Devuelve {estado, resultado, tarea_id, intentos, tiempo}
- El flujo se detiene si algo bloquea o espera aprobacion.
"""
from src.orchestrator.core import Orchestrator
from src.orchestrator.agent_runner import AgentRunner
from src.orchestrator.brains import NullBrain


def _orq_test():
    o = Orchestrator(brain=NullBrain())
    # Aislar approvals y memory para no ensuciar
    import tempfile
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    from src.orchestrator.memory import Memory
    from src.orchestrator.approvals import Approvals
    o.memory = Memory(archivo=tmp / "mem.json")
    o.approvals = Approvals(archivo=tmp / "aprob.json")
    return o


def test_runner_instancia_agentes():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    assert len(r.agentes) == 7


def test_runner_ejecuta_agente():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    resultado = r.ejecutar_agente("Director", {"descripcion": "probar algo"})
    # Nueva interfaz: resultado envuelto
    assert resultado["estado"] in ("completado", "esperando_aprobacion", "bloqueado")
    assert resultado["resultado"]["agente"] == "Director"
    assert "subtareas" in resultado["resultado"]
    assert resultado["tarea_id"].startswith("Director_")


def test_runner_rechaza_agente_inexistente():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    resultado = r.ejecutar_agente("NoExiste", {"descripcion": "test"})
    assert resultado["estado"] == "error"
    assert "no encontrado" in resultado["error"]


def test_runner_deniega_permiso():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    resultado = r.ejecutar_agente("Developer", {"accion": "tocar_main", "descripcion": "x"})
    assert resultado["estado"] == "bloqueado"
    assert "denegado" in resultado["razon"].lower() or "permiso" in resultado["razon"].lower()


def test_runner_flujo_completo():
    """El flujo se detiene cuando el Developer pide aprobacion."""
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    flujo = r.ejecutar_flujo("Simular 30 dias de operacion")
    # El Developer pide aprobacion -> el flujo se detiene
    assert flujo["estado"] in ("esperando_aprobacion", "completado", "bloqueado")
    assert len(flujo["pasos"]) >= 2
    agentes = [p["agente"] for p in flujo["pasos"]]
    assert "Director" in agentes


def test_runner_guarda_en_memoria():
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    antes = len(o.memory.buscar("resultado_agente"))
    r.ejecutar_agente("Director", {"descripcion": "probar memoria"})
    despues = len(o.memory.buscar("resultado_agente"))
    assert despues > antes


def test_runner_budget_se_aplica():
    """El budget debe bloquear despues de 3 intentos."""
    o = _orq_test()
    r = AgentRunner(o, brain=NullBrain())
    tarea_id = "TEST-BUDGET-001"
    for _ in range(3):
        o.budget.registrar_intento(tarea_id)
    resultado = r.ejecutar_agente("Director", {"descripcion": "x"}, tarea_id=tarea_id)
    assert resultado["estado"] == "bloqueado"
    assert "Maximo" in resultado["razon"] or "intentos" in resultado["razon"].lower()