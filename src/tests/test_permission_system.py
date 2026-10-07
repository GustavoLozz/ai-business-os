"""Tests del sistema de permisos."""
from src.orchestrator.permission_system import PermissionSystem


def test_developer_puede_escribir():
    ps = PermissionSystem()
    ok, _ = ps.puede("Developer", "escribir_codigo")
    assert ok


def test_developer_no_puede_tocar_main():
    ps = PermissionSystem()
    ok, _ = ps.puede("Developer", "tocar_main")
    assert not ok


def test_auditor_no_puede_modificar():
    ps = PermissionSystem()
    ok, _ = ps.puede("Auditor", "modificar_nada")
    assert not ok


def test_agente_desconocido():
    ps = PermissionSystem()
    ok, _ = ps.puede("Inexistente", "algo")
    assert not ok