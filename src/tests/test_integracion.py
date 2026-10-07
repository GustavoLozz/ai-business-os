"""Tests de integracion: agentes + simulador + Qiskit."""
from src.orchestrator.core import Orchestrator


def test_orchestrator_tiene_simulator_runner():
    o = Orchestrator()
    assert o.simulator is not None
    assert hasattr(o.simulator, "ejecutar")


def test_simular_empresa_basico():
    o = Orchestrator()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    assert flujo["estado"] == "completado"
    assert "simulacion" in flujo


def test_simulacion_tiene_datos_reales():
    o = Orchestrator()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    sim = flujo["simulacion"]
    assert "facturacion" in sim
    assert "costos" in sim
    assert "margen" in sim
    assert sim["facturacion"] >= 0
    assert sim["costos"] >= 0


def test_simulacion_usa_qiskit():
    o = Orchestrator()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    assert flujo["simulacion"]["motor_quantum"] == "qiskit_aer"


def test_simulacion_ejecuta_7_agentes():
    o = Orchestrator()
    flujo = o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    agentes = [p["agente"] for p in flujo["pasos"]]
    assert "Director" in agentes
    assert "Arquitecto" in agentes
    assert "Developer" in agentes
    assert "Quantum_RD" in agentes
    assert "Tester" in agentes
    assert "Auditor" in agentes
    assert "Business" in agentes


def test_simulacion_guarda_en_memoria():
    o = Orchestrator()
    o.memory.resetear()
    antes = len(o.memory.buscar("simulacion_completa"))
    o.simular_empresa(dias=5, clientes=20, productos=3, seed=42)
    despues = len(o.memory.buscar("simulacion_completa"))
    assert despues > antes


def test_simulacion_determinista():
    o1 = Orchestrator()
    o2 = Orchestrator()
    f1 = o1.simular_empresa(dias=5, clientes=20, productos=3, seed=99)
    f2 = o2.simular_empresa(dias=5, clientes=20, productos=3, seed=99)
    assert f1["simulacion"]["facturacion"] == f2["simulacion"]["facturacion"]