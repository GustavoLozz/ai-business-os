"""Tests del presupuesto de autonomia."""
from src.orchestrator.budget import Budget


def test_max_intentos():
    b = Budget(max_intentos=3)
    assert b.puede_reintentar("T1")
    b.registrar_intento("T1")
    b.registrar_intento("T1")
    assert b.puede_reintentar("T1")
    b.registrar_intento("T1")
    assert not b.puede_reintentar("T1")


def test_costo():
    b = Budget(max_costo=1.0)
    assert b.registrar_costo("T1", 0.5)
    assert b.registrar_costo("T1", 0.4)
    assert not b.registrar_costo("T1", 0.2)


def test_estado():
    b = Budget(max_intentos=3, max_costo=2.0)
    b.registrar_intento("T1")
    b.registrar_costo("T1", 1.5)
    e = b.estado("T1")
    assert e["intentos"] == 1
    assert e["max_intentos"] == 3
    assert e["costo"] == 1.5
    assert e["max_costo"] == 2.0