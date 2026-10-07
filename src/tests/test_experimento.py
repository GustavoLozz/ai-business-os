"""Tests del motor quantum annealing y del experimento."""
from simulator.empresa import Empresa
from experiments.quantum_annealer import QuantumAnnealer, qiskit_disponible
from experiments.experimento_01 import correr_experimento


def test_qiskit_disponible():
    """Qiskit debe estar disponible (lo instalamos)."""
    assert qiskit_disponible() is True


def test_annealer_creacion():
    a = QuantumAnnealer(seed=42)
    assert a.seed == 42
    assert a.historial == []


def test_annealer_optimiza_precios():
    e = Empresa(seed=42)
    productos = e.generar_productos(cantidad=3)
    precios_originales = [p.precio for p in productos]

    a = QuantumAnnealer(seed=42)
    resultado = a.optimizar_precios(productos, iteraciones=5)

    assert "mejor_combinacion" in resultado
    assert "mejor_score" in resultado
    assert resultado["motor"] == "qiskit_aer"
    assert len(resultado["mejor_combinacion"]) == 3


def test_annealer_aplica_optimizacion():
    e = Empresa(seed=42)
    productos = e.generar_productos(cantidad=3)
    precios_antes = [p.precio for p in productos]

    a = QuantumAnnealer(seed=42)
    resultado = a.optimizar_precios(productos, iteraciones=5)
    a.aplicar_optimizacion(productos, resultado)

    precios_despues = [p.precio for p in productos]
    # Al menos algun precio debe haber cambiado
    assert precios_antes != precios_despues


def test_annealer_historial():
    e = Empresa(seed=42)
    productos = e.generar_productos(cantidad=2)
    a = QuantumAnnealer(seed=42)
    a.optimizar_precios(productos, iteraciones=10)
    assert len(a.historial) == 10
    for h in a.historial:
        assert "iteracion" in h
        assert "temperatura" in h
        assert "score" in h


def test_experimento_corre():
    """El experimento completo debe correr sin errores."""
    payload = correr_experimento(dias=5, clientes=20, productos=3, seed=42)
    assert "resultados" in payload
    assert "recomendacion" in payload
    assert payload["experimento"] == "01"


def test_experimento_tiene_3_estrategias():
    payload = correr_experimento(dias=5, clientes=20, productos=3, seed=42)
    r = payload["resultados"]
    assert "clasico" in r
    assert "quantum_inspired" in r
    assert "cuantico" in r
    assert r["clasico"]["nombre"] == "Clasico"
    assert r["cuantico"]["nombre"] == "Cuantico (Qiskit)"


def test_experimento_cuantico_usa_qiskit():
    payload = correr_experimento(dias=5, clientes=20, productos=3, seed=42)
    assert payload["resultados"]["cuantico"]["motor_quantum"] == "qiskit_aer"


def test_experimento_determinista_con_seed():
    """Con la misma seed, dos corridas deben dar el mismo resultado."""
    p1 = correr_experimento(dias=5, clientes=20, productos=3, seed=99)
    p2 = correr_experimento(dias=5, clientes=20, productos=3, seed=99)
    assert p1["resultados"]["clasico"]["margen"] == p2["resultados"]["clasico"]["margen"]
    assert p1["resultados"]["cuantico"]["margen"] == p2["resultados"]["cuantico"]["margen"]