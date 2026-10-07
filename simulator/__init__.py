"""Simulador empresarial de AI-BUSINESS-OS.

Modela una empresa virtual con clientes, productos, costos,
ventas y margenes. Permite simular 30 dias de operacion y
comparar estrategias.
"""
from .cliente import Cliente
from .producto import Producto
from .costo import Costo
from .venta import Venta
from .margen import calcular_margen, resumen_margenes
from .empresa import Empresa
from .escenario import Escenario, comparar_escenarios

__all__ = [
    "Cliente",
    "Producto",
    "Costo",
    "Venta",
    "calcular_margen",
    "resumen_margenes",
    "Empresa",
    "Escenario",
    "comparar_escenarios",
]