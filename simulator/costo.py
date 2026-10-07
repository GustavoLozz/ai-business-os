"""Modelo de costo. Fijo o variable."""


class Costo:
    def __init__(self, id, categoria, monto, tipo="fijo", recurrente=True):
        self.id = id
        self.categoria = categoria
        self.monto = monto
        self.tipo = tipo  # "fijo" o "variable"
        self.recurrente = recurrente

    def aplicar(self, dias=1):
        """Devuelve el costo total para N dias."""
        if self.tipo == "fijo":
            return self.monto
        return self.monto * dias

    def reportar(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "tipo": self.tipo,
            "monto": self.monto,
            "recurrente": self.recurrente,
        }

    def __repr__(self):
        return f"<Costo {self.categoria} ({self.tipo}, ${self.monto})>"


def total_costos(costos, dias=1):
    """Suma los costos de una lista para N dias."""
    return sum(c.aplicar(dias) for c in costos)


def resumen_costos(costos, dias=1):
    """Devuelve resumen agrupado por categoria."""
    resumen = {}
    for c in costos:
        aplicado = c.aplicar(dias)
        if c.categoria not in resumen:
            resumen[c.categoria] = 0
        resumen[c.categoria] += aplicado
    return resumen


def costos_default():
    """Costos tipicos de una empresa virtual."""
    return [
        Costo("C001", "alquiler", 50000, tipo="fijo"),
        Costo("C002", "sueldos", 150000, tipo="fijo"),
        Costo("C003", "servicios", 20000, tipo="fijo"),
        Costo("C004", "marketing", 30000, tipo="fijo"),
        Costo("C005", "logistica", 500, tipo="variable"),
    ]