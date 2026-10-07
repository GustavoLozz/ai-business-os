"""Tests del motor de simulacion y escenarios."""
from simulator.empresa import Empresa
from simulator.escenario import (
    Escenario,
    escenario_clasico,
    escenario_quantum_inspired,
    comparar_escenarios,
)


def test_empresa_creacion():
    e = Empresa(nombre="Test Empresa", seed=42)
    assert e.nombre == "Test Empresa"
    assert e.dias_simulados == 0
    assert len(e.ventas) == 0


def test_empresa_genera_clientes():
    e = Empresa(seed=42)
    clientes = e.generar_clientes(cantidad=50)
    assert len(clientes) == 50
    assert all(c.ingreso_mensual > 0 for c in clientes)


def test_empresa_genera_productos():
    e = Empresa(seed=42)
    productos = e.generar_productos(cantidad=5)
    assert len(productos) == 5
    assert all(p.precio > p.costo for p in productos)


def test_empresa_simula_dias():
    e = Empresa(seed=42)
    e.generar_clientes(cantidad=20)
    e.generar_productos(cantidad=3)
    e.simular(dias=5)
    assert e.dias_simulados == 5
    assert len(e.ventas) >= 0
    assert len(e.historial_diario) == 5


def test_empresa_reporte_tiene_campos():
    e = Empresa(seed=42)
    e.generar_clientes(cantidad=20)
    e.generar_productos(cantidad=3)
    e.simular(dias=5)
    r = e.reporte()
    assert "facturacion" in r
    assert "costos" in r
    assert "margenes" in r
    assert "clientes_totales" in r
    assert r["dias_simulados"] == 5


def test_empresa_determinista_con_seed():
    """Con la misma seed, dos empresas deben dar el mismo resultado."""
    e1 = Empresa(seed=123)
    e1.generar_clientes(cantidad=10)
    e1.generar_productos(cantidad=3)
    e1.simular(dias=5)

    e2 = Empresa(seed=123)
    e2.generar_clientes(cantidad=10)
    e2.generar_productos(cantidad=3)
    e2.simular(dias=5)

    assert e1.reporte()["facturacion"] == e2.reporte()["facturacion"]


def test_escenario_clasico():
    e = escenario_clasico()
    assert e.nombre == "Clasico"
    assert e.config == {}


def test_escenario_quantum_inspired():
    e = escenario_quantum_inspired()
    assert e.nombre == "Quantum-Inspired"
    assert e.config.get("optimizar_precios") is True
    assert e.config.get("optimizar_probabilidad") is True


def test_escenario_ejecuta_y_devuelve_reporte():
    e = escenario_clasico()
    r = e.ejecutar(dias=5, clientes=10, productos=3)
    assert "facturacion" in r
    assert r["dias_simulados"] == 5


def test_comparar_escenarios():
    resultados = comparar_escenarios(dias=5, clientes=20, productos=3)
    assert len(resultados) == 3
    nombres = [r["nombre"] for r in resultados]
    assert "Clasico" in nombres
    assert "Quantum-Inspired" in nombres
    assert "Cuantico" in nombres


def test_comparar_escenarios_tiene_mejora():
    resultados = comparar_escenarios(dias=5, clientes=20, productos=3)
    # El primero (clasico) debe tener mejora 0
    assert resultados[0]["mejora_pct"] == 0.0
    # Todos deben tener el campo
    for r in resultados:
        assert "mejora_pct" in r