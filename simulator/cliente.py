"""Modelo de cliente. Empezamos simple, luego enriquecemos."""
import random
from datetime import datetime


class Cliente:
    def __init__(self, id, nombre, ingreso_mensual, segmento="medio"):
        self.id = id
        self.nombre = nombre
        self.ingreso_mensual = ingreso_mensual
        self.segmento = segmento
        self.compras = []
        self.activo = True
        self.churn_probabilidad = 0.02
        self.probabilidad_compra = 0.15

    def comprar(self, producto, cantidad=1, dia=1):
        """Registra una compra si el cliente decide comprar."""
        if not self.activo:
            return None

        if random.random() > self.probabilidad_compra:
            return None

        venta = {
            "cliente_id": self.id,
            "producto_id": producto.id,
            "producto_nombre": producto.nombre,
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
            "total": producto.precio * cantidad,
            "dia": dia,
        }
        self.compras.append(venta)
        return venta

    def pasar_dia(self):
        """Avanza un dia. Puede churnear."""
        if not self.activo:
            return False
        if random.random() < self.churn_probabilidad:
            self.activo = False
            return False
        return True

    def total_comprado(self):
        return sum(c["total"] for c in self.compras)

    def cantidad_compras(self):
        return len(self.compras)

    def reportar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "segmento": self.segmento,
            "ingreso_mensual": self.ingreso_mensual,
            "activo": self.activo,
            "compras": self.cantidad_compras(),
            "total_comprado": self.total_comprado(),
        }

    def __repr__(self):
        estado = "activo" if self.activo else "churn"
        return f"<Cliente {self.id} {self.nombre} ({estado}, {self.cantidad_compras()} compras)>"