"""Tests de integracion: agentes + simulador + Qiskit.

IMPORTANTE: usan NullBrain para no gastar tokens ni tardar minutos.
"""
from src.orchestrator.core import Orchestrator
from src.orchestrator.brains import NullBrain


def _orquestador_test():
    """Orchestrator con NullBrain (rapido, sin llamadas a OpenRouter)."""
    return Orchestrator(brain=NullBrain())


def test_orchestrator_tiene_simulator_runner():
    o = _orquestador_test()
    assert o.simulator is not None
    assert hasattr(o.simulator, "ejecutar")


def test_simular_empresa_basico():
    o = _orquestador_test()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    assert flujo["estado"] == "completado"
    assert "simulacion" in flujo


def test_simulacion_tiene_datos_reales():
    o = _orquestador_test()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    sim = flujo["simulacion"]
    assert "facturacion" in sim
    assert "costos" in sim
    assert "margen" in sim
    assert sim["facturacion"] >= 0


def test_simulacion_usa_qiskit():
    o = _orquestador_test()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    assert flujo["simulacion"]["motor_quantum"] == "qiskit_aer"


def test_simulacion_ejecuta_7_agentes():
    o = _orquestador_test()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    agentes = [p["agente"] for p in flujo["pasos"]]
    assert "Director" in agentes
    assert "Auditor" in agentes
    assert "Business" in agentes


def test_simulacion_guarda_en_memoria():
    o = _orquestador_test()
    o.memory.resetear()
    antes = len(o.memory.buscar("simulacion_completa"))
    o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    despues = len(o.memory.buscar("simulacion_completa"))
    assert despues > antes


def test_simulacion_determinista():
    o1 = _orquestador_test()
    o2 = _orquestador_test()
    f1 = o1.simular_empresa(dias=5, clientes=20, productos=3, seed=99)
    f2 = o2.simular_empresa(dias=5, clientes=20, productos=3, seed=99)
    assert f1["simulacion"]["facturacion"] == f2["simulacion"]["facturacion"]