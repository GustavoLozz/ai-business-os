"""Presupuesto de autonomia por tarea."""
MAX_INTENTOS_POR_TAREA = 3
MAX_TIEMPO_POR_TAREA_SEG = 300
MAX_COSTO_AGENTES_USD = 1.00


class Budget:
    def __init__(self, max_intentos=None, max_tiempo=None, max_costo=None):
        self.max_intentos = max_intentos or MAX_INTENTOS_POR_TAREA
        self.max_tiempo = max_tiempo or MAX_TIEMPO_POR_TAREA_SEG
        self.max_costo = max_costo or MAX_COSTO_AGENTES_USD
        self.intentos = {}
        self.tiempos = {}
        self.costos = {}

    def registrar_intento(self, tarea_id):
        self.intentos[tarea_id] = self.intentos.get(tarea_id, 0) + 1
        return self.intentos[tarea_id]

    def puede_reintentar(self, tarea_id):
        return self.intentos.get(tarea_id, 0) < self.max_intentos

    def registrar_costo(self, tarea_id, costo):
        self.costos[tarea_id] = self.costos.get(tarea_id, 0) + costo
        return self.costos[tarea_id] <= self.max_costo

    def estado(self, tarea_id):
        return {"tarea": tarea_id, "intentos": self.intentos.get(tarea_id, 0), "max_intentos": self.max_intentos}