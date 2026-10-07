"""Tests del gestor de tareas."""
from src.orchestrator.task_manager import TaskManager, EstadoTarea


def test_crear_tarea():
    tm = TaskManager()
    t = tm.crear("probar algo")
    assert t["id"] == "TASK-000001"
    assert t["estado"] == EstadoTarea.PENDIENTE.value


def test_flujo_tarea():
    tm = TaskManager()
    t = tm.crear("probar", agente="Developer")
    assert tm.asignar(t["id"], "Developer")
    assert tm.iniciar(t["id"])
    assert tm.completar(t["id"])
    assert tm.obtener(t["id"])["estado"] == EstadoTarea.COMPLETADA.value


def test_fallar_incrementa_intentos():
    tm = TaskManager()
    t = tm.crear("probar")
    tm.fallar(t["id"], "error")
    assert tm.obtener(t["id"])["intentos"] == 1