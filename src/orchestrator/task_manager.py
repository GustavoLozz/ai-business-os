"""Gestor de tareas con estados y reintentos."""
from datetime import datetime
from enum import Enum


class EstadoTarea(str, Enum):
    PENDIENTE = "pendiente"
    ASIGNADA = "asignada"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    FALLIDA = "fallida"


class TaskManager:
    def __init__(self):
        self.tareas = {}
        self.contador = 0

    def crear(self, descripcion, agente=None, prioridad="media"):
        self.contador += 1
        task_id = f"TASK-{self.contador:06d}"
        self.tareas[task_id] = {
            "id": task_id, "descripcion": descripcion, "agente": agente,
            "prioridad": prioridad, "estado": EstadoTarea.PENDIENTE.value,
            "creada": datetime.now().isoformat(), "intentos": 0, "historial": [],
        }
        return self.tareas[task_id]

    def asignar(self, task_id, agente):
        if task_id not in self.tareas: return False
        self.tareas[task_id]["agente"] = agente
        self.tareas[task_id]["estado"] = EstadoTarea.ASIGNADA.value
        return True

    def iniciar(self, task_id):
        if task_id in self.tareas:
            self.tareas[task_id]["estado"] = EstadoTarea.EN_PROCESO.value
            return True
        return False

    def completar(self, task_id):
        if task_id in self.tareas:
            self.tareas[task_id]["estado"] = EstadoTarea.COMPLETADA.value
            return True
        return False

    def fallar(self, task_id, motivo):
        t = self.tareas.get(task_id)
        if not t: return False
        t["intentos"] += 1
        t["historial"].append({"fecha": datetime.now().isoformat(), "motivo": motivo})
        t["estado"] = EstadoTarea.FALLIDA.value
        return True

    def obtener(self, task_id):
        return self.tareas.get(task_id)

    def listar(self, estado=None):
        if estado is None: return list(self.tareas.values())
        return [t for t in self.tareas.values() if t["estado"] == estado]

    def estadisticas(self):
        stats = {}
        for t in self.tareas.values():
            stats[t["estado"]] = stats.get(t["estado"], 0) + 1
        return {"total": len(self.tareas), "por_estado": stats}