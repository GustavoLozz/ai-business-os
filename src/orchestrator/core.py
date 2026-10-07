"""Nucleo del Orchestrator - coordina todo."""
from .logger import Logger
from .memory import Memory
from .budget import Budget
from .permission_system import PermissionSystem
from .agent_registry import AgentRegistry
from .task_manager import TaskManager
from .approvals import Approvals


class Orchestrator:
    def __init__(self):
        self.logger = Logger()
        self.memory = Memory()
        self.budget = Budget()
        self.permissions = PermissionSystem()
        self.registry = AgentRegistry()
        self.tasks = TaskManager()
        self.approvals = Approvals()
        self.logger.info("Orchestrator inicializado", agentes=self.registry.contar())

    def recibir_objetivo(self, objetivo):
        self.logger.info("Objetivo recibido", objetivo=objetivo)
        self.memory.recordar("objetivo", objetivo)
        return self.tasks.crear(objetivo, agente="Director", prioridad="alta")

    def estado(self):
        return {
            "agentes": self.registry.contar(),
            "tareas": self.tasks.estadisticas(),
            "memoria": self.memory.estadisticas(),
            "pendientes_aprobacion": len(self.approvals.listar_pendientes()),
        }

    def panel(self):
        e = self.estado()
        return "\n".join([
            "=" * 50,
            "       AI-BUSINESS-OS - PANEL CEO",
            "=" * 50,
            f"  Agentes registrados:      {e['agentes']}",
            f"  Tareas totales:           {e['tareas']['total']}",
            f"  Memorias guardadas:       {e['memoria']['total']}",
            f"  Pendientes de aprobacion: {e['pendientes_aprobacion']}",
            "=" * 50,
        ])