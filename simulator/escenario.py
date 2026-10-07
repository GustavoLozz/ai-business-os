"""Escenarios comparables: clasico vs quantum-inspired vs cuantico."""
import random
from .empresa import Empresa
from .margen import formato_moneda, formato_pct


class Escenario:
    def __init__(self, nombre, descripcion, seed=None, config=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.seed = seed
        self.config = config or {}
        self.resultado = None

    def ejecutar(self, dias=30, clientes=100, productos=5):
        """Corre la simulacion con la configuracion del escenario."""
        empresa = Empresa(nombre=self.nombre, seed=self.seed)
        empresa.generar_clientes(cantidad=clientes)
        empresa.generar_productos(cantidad=productos)

        # Ajustes especificos por escenario
        if self.config.get("optimizar_precios"):
            for p in empresa.productos:
                p.precio = int(p.precio * 1.15)

        if self.config.get("optimizar_probabilidad"):
            for c in empresa.clientes:
                c.probabilidad_compra = min(1.0, c.probabilidad_compra * 1.2)

        if self.config.get("reducir_churn"):
            for c in empresa.clientes:
                c.churn_probabilidad = max(0.001, c.churn_probabilidad * 0.5)

        empresa.simular(dias)
        self.resultado = empresa.reporte()
        return self.resultado


def escenario_clasico():
    """Estrategia base: sin optimizacion."""
    return Escenario(
        nombre="Clasico",
        descripcion="Simulacion base sin optimizacion",
        seed=42,
        config={},
    )


def escenario_quantum_inspired():
    """Estrategia quantum-inspired: optimiza multiples variables a la vez."""
    return Escenario(
        nombre="Quantum-Inspired",
        descripcion="Optimizacion multi-variable inspirada en quantum annealing",
        seed=42,
        config={
            "optimizar_precios": True,
            "optimizar_probabilidad": True,
            "reducir_churn": True,
        },
    )


def escenario_cuantico():
    """Estrategia cuantica: usa Qiskit para optimizar (simulado por ahora)."""
    return Escenario(
        nombre="Cuantico",
        descripcion="Optimizacion con Qiskit (placeholder hasta Etapa 5)",
        seed=42,
        config={
            "optimizar_precios": True,
            "optimizar_probabilidad": True,
            "reducir_churn": True,
            "usar_qiskit": True,
        },
    )


def comparar_escenarios(dias=30, clientes=100, productos=5):
    """Corre los 3 escenarios y devuelve la comparativa."""
    escenarios = [escenario_clasico(), escenario_quantum_inspired(), escenario_cuantico()]
    resultados = []
    for e in escenarios:
        r = e.ejecutar(dias=dias, clientes=clientes, productos=productos)
        resultados.append({
            "nombre": e.nombre,
            "descripcion": e.descripcion,
            "facturacion": r["facturacion"],
            "costos": r["costos"],
            "margen": r["margenes"]["margen"],
            "margen_pct": r["margenes"]["margen_pct"],
            "clientes_activos": r["clientes_activos"],
            "ventas_totales": r["ventas_totales"],
        })

    # Calcular mejoras respecto al clasico
    base = resultados[0]
    for r in resultados:
        if base["margen"] != 0:
            r["mejora_pct"] = round(
                ((r["margen"] - base["margen"]) / abs(base["margen"])) * 100, 2
            )
        else:
            r["mejora_pct"] = 0.0

    return resultados


def imprimir_comparativa(resultados):
    """Imprime la comparativa de forma legible."""
    lineas = [
        "=" * 70,
        "  COMPARATIVA DE ESCENARIOS",
        "=" * 70,
        f"  {'Escenario':<20} {'Facturacion':>15} {'Margen':>15} {'Mejora':>10}",
        "-" * 70,
    ]
    for r in resultados:
        lineas.append(
            f"  {r['nombre']:<20} {formato_moneda(r['facturacion']):>15} "
            f"{formato_moneda(r['margen']):>15} {formato_pct(r['mejora_pct']):>10}"
        )
    lineas.append("=" * 70)
    return "\n".join(lineas)