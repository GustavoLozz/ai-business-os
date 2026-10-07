"""Clase base para todos los agentes de AI-BUSINESS-OS.

Preparada para funcionar de dos formas:
- Modo simbolico: logica determinista programada (default, sin costo).
- Modo LLM: el agente puede recibir un "cerebro" externo (Ollama u otro).
"""
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Agent:
    """Agente base. Todos los agentes heredan de esta clase."""

    def __init__(self, nombre, rol, permisos=None, cerebro=None):
        self.nombre = nombre
        self.rol = rol
        self.permisos = permisos or []
        self.cerebro = cerebro
        self.estado = "registrado"
        self.historial = []

    def activar(self):
        self.estado = "activo"
        return self.estado

    def desactivar(self):
        self.estado = "inactivo"
        return self.estado

    def puede(self, accion):
        return accion in self.permisos

    def ejecutar(self, tarea):
        """Metodo principal. Cada agente lo sobrescribe."""
        self.activar()
        self._log("ejecutar", tarea=str(tarea))
        resultado = self._ejecutar_especifico(tarea)
        self.desactivar()
        return resultado

    def _ejecutar_especifico(self, tarea):
        """Metodo a sobrescribir por cada agente."""
        raise NotImplementedError(f"{self.nombre} no implemento _ejecutar_especifico")

    def _usar_cerebro(self, prompt):
        """Si hay cerebro (LLM), lo usa. Sino, devuelve None."""
        if self.cerebro is None:
            return None
        try:
            return self.cerebro.consultar(prompt)
        except Exception as e:
            self._log("error_cerebro", error=str(e))
            return None

    def _log(self, evento, **extra):
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "agente": self.nombre,
            "evento": evento,
        }
        entrada.update(extra)
        self.historial.append(entrada)
        return entrada

    def reportar(self):
        return {
            "nombre": self.nombre,
            "rol": self.rol,
            "estado": self.estado,
            "permisos": self.permisos,
            "cerebro": "LLM" if self.cerebro else "simbolico",
            "eventos": len(self.historial),
        }

    def __repr__(self):
        return f"<Agent {self.nombre} ({self.estado})>"