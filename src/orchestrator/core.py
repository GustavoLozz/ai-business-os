"""Nucleo del Orchestrator - coordina todo."""
from .logger import Logger
from .memory import Memory
from .budget import Budget
from .permission_system import PermissionSystem
from .agent_registry import AgentRegistry
from .task_manager import TaskManager
from .approvals import Approvals


class Orchestrator:
    def __init__(self, brain=None, brain_tipo=None):
        """Crea el Orchestrator.

        Args:
            brain: instancia de Brain (opcional). Si es None, auto-detecta.
            brain_tipo: "openrouter" | "null" | None. Fuerza un tipo especifico.
        """
        self.logger = Logger()
        self.memory = Memory()
        self.budget = Budget()
        self.permissions = PermissionSystem()
        self.registry = AgentRegistry()
        self.tasks = TaskManager()
        self.approvals = Approvals()
        self._brain = brain
        self._brain_tipo = brain_tipo
        self._runner = None
        self._simulator_runner = None
        self.logger.info("Orchestrator inicializado", agentes=self.registry.contar())

    @property
    def brain(self):
        """Lazy loading del cerebro."""
        if self._brain is None:
            from .brains import crear_brain
            self._brain = crear_brain(self._brain_tipo)
        return self._brain

    @property
    def runner(self):
        """Lazy loading del AgentRunner."""
        if self._runner is None:
            from .agent_runner import AgentRunner
            self._runner = AgentRunner(self, brain=self.brain)
        return self._runner

    @property
    def simulator(self):
        """Lazy loading del SimulatorRunner."""
        if self._simulator_runner is None:
            from .simulator_runner import SimulatorRunner
            self._simulator_runner = SimulatorRunner(self)
        return self._simulator_runner

    def recibir_objetivo(self, objetivo):
        self.logger.info("Objetivo recibido", objetivo=objetivo)
        self.memory.recordar("objetivo", objetivo)
        return self.tasks.crear(objetivo, agente="Director", prioridad="alta")

    def ejecutar_flujo(self, objetivo):
        """Ejecuta el flujo completo de agentes (sin simulador)."""
        self.logger.info("Flujo solicitado", objetivo=objetivo)
        self.memory.recordar("objetivo_flujo", objetivo)
        return self.runner.ejecutar_flujo(objetivo)

    def simular_empresa(self, dias=30, clientes=100, productos=5, seed=42):
        """Ejecuta el flujo de simulacion completo con agentes + simulador."""
        self.logger.info("Simulacion solicitada", dias=dias, clientes=clientes)
        self.memory.recordar("objetivo_simulacion",
                             f"simular {dias} dias con {clientes} clientes")
        return self.simulator.ejecutar(dias=dias, clientes=clientes,
                                       productos=productos, seed=seed)

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