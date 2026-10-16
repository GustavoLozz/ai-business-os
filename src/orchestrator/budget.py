"""Presupuesto de autonomia por tarea.

Mejorado segun auditoria externa de Claude (2026-10-16):
- Lee limites desde Config (asi el .env tiene efecto).
- 0 ya no cae al default (permite 0 como valor explicito).
- Metodo registrar_tiempo() para trackear duracion.
"""
import time
from datetime import datetime


def _get_limite(nombre, default):
    """Lee un limite desde Config con fallback al default."""
    try:
        from .config import Config
        valor = getattr(Config, nombre, default)
        if valor is None:
            return default
        return valor
    except Exception:
        return default


class Budget:
    def __init__(self, max_intentos=None, max_tiempo=None, max_costo=None):
        self.max_intentos = (
            max_intentos if max_intentos is not None
            else _get_limite("MAX_INTENTOS_POR_TAREA", 3)
        )
        self.max_tiempo = (
            max_tiempo if max_tiempo is not None
            else _get_limite("MAX_TIEMPO_POR_TAREA_SEG", 300)
        )
        self.max_costo = (
            max_costo if max_costo is not None
            else _get_limite("MAX_COSTO_AGENTES_USD", 1.00)
        )
        self.intentos = {}
        self.tiempos = {}
        self.costos = {}
        self.tiempos_inicio = {}

    # ------------------------------------------------------------------
    # Intentos
    # ------------------------------------------------------------------
    def registrar_intento(self, tarea_id):
        self.intentos[tarea_id] = self.intentos.get(tarea_id, 0) + 1
        return self.intentos[tarea_id]

    def puede_reintentar(self, tarea_id):
        return self.intentos.get(tarea_id, 0) < self.max_intentos

    def intentos_restantes(self, tarea_id):
        return max(0, self.max_intentos - self.intentos.get(tarea_id, 0))

    # ------------------------------------------------------------------
    # Costo
    # ------------------------------------------------------------------
    def registrar_costo(self, tarea_id, costo):
        self.costos[tarea_id] = self.costos.get(tarea_id, 0) + costo
        return self.costos[tarea_id] <= self.max_costo

    def costo_acumulado(self, tarea_id):
        return self.costos.get(tarea_id, 0)

    def dentro_de_presupuesto(self, tarea_id):
        return self.costo_acumulado(tarea_id) <= self.max_costo

    # ------------------------------------------------------------------
    # Tiempo
    # ------------------------------------------------------------------
    def iniciar_tiempo(self, tarea_id):
        """Marca el inicio de una tarea."""
        self.tiempos_inicio[tarea_id] = time.time()
        return self.tiempos_inicio[tarea_id]

    def registrar_tiempo(self, tarea_id):
        """Registra el tiempo total de una tarea (desde iniciar_tiempo)."""
        if tarea_id not in self.tiempos_inicio:
            return 0
        duracion = time.time() - self.tiempos_inicio[tarea_id]
        self.tiempos[tarea_id] = self.tiempos.get(tarea_id, 0) + duracion
        del self.tiempos_inicio[tarea_id]
        return round(duracion, 2)

    def tiempo_acumulado(self, tarea_id):
        return self.tiempos.get(tarea_id, 0)

    def dentro_de_tiempo(self, tarea_id):
        return self.tiempo_acumulado(tarea_id) <= self.max_tiempo

    # ------------------------------------------------------------------
    # Estado
    # ------------------------------------------------------------------
    def estado(self, tarea_id):
        return {
            "tarea": tarea_id,
            "intentos": self.intentos.get(tarea_id, 0),
            "max_intentos": self.max_intentos,
            "costo": self.costos.get(tarea_id, 0),
            "max_costo": self.max_costo,
            "tiempo": round(self.tiempos.get(tarea_id, 0), 2),
            "max_tiempo": self.max_tiempo,
        }

    def puede_continuar(self, tarea_id):
        """Devuelve True si la tarea puede seguir dentro de todos los limites."""
        return (
            self.puede_reintentar(tarea_id)
            and self.dentro_de_presupuesto(tarea_id)
            and self.dentro_de_tiempo(tarea_id)
        )