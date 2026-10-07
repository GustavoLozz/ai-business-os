"""Modelo de producto con costo, precio y margen."""


class Producto:
    def __init__(self, id, nombre, costo, precio, categoria="general"):
        self.id = id
        self.nombre = nombre
        self.costo = costo
        self.precio = precio
        self.categoria = categoria
        self.vendidos = 0

    def margen_unitario(self):
        """Margen absoluto por unidad."""
        return self.precio - self.costo

    def margen_porcentaje(self):
        """Margen como porcentaje del precio."""
        if self.precio == 0:
            return 0.0
        return ((self.precio - self.costo) / self.precio) * 100

    def registrar_venta(self, cantidad=1):
        self.vendidos += cantidad

    def ingresos_totales(self):
        return self.precio * self.vendidos

    def costos_totales(self):
        return self.costo * self.vendidos

    def ganancia_total(self):
        return self.ingresos_totales() - self.costos_totales()

    def reportar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "costo": self.costo,
            "precio": self.precio,
            "margen_unitario": self.margen_unitario(),
            "margen_pct": round(self.margen_porcentaje(), 2),
            "vendidos": self.vendidos,
            "ingresos": self.ingresos_totales(),
            "costos": self.costos_totales(),
            "ganancia": self.ganancia_total(),
        }

    def __repr__(self):
        return f"<Producto {self.id} {self.nombre} (${self.precio}, margen {self.margen_porcentaje():.1f}%)>"