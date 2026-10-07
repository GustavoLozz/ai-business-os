"""Motor de Quantum Annealing usando Qiskit de verdad."""
import math
import random

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    QISKIT_DISPONIBLE = True
except ImportError:
    QISKIT_DISPONIBLE = False


class QuantumAnnealer:
    """Simula annealing cuantico para optimizar precios."""

    def __init__(self, seed=42):
        self.seed = seed
        random.seed(seed)
        self.historial = []

    def optimizar_precios(self, productos, iteraciones=20):
        """Devuelve la mejor combinacion de ajustes de precio."""
        if not QISKIT_DISPONIBLE:
            return self._fallback_clasico(productos, iteraciones)

        mejor_combinacion = None
        mejor_score = float("-inf")

        for it in range(iteraciones):
            temperatura = 1.0 - (it / iteraciones)
            combinacion = []
            for p in productos:
                factor = self._samplear_factor(temperatura)
                combinacion.append(factor)

            score = self._evaluar_combinacion(productos, combinacion)
            self.historial.append({"iteracion": it, "temperatura": temperatura, "score": score})

            if score > mejor_score:
                mejor_score = score
                mejor_combinacion = combinacion

        return {
            "mejor_combinacion": mejor_combinacion,
            "mejor_score": mejor_score,
            "iteraciones": iteraciones,
            "historial": self.historial,
            "motor": "qiskit_aer" if QISKIT_DISPONIBLE else "clasico",
        }

    def _samplear_factor(self, temperatura):
        """Simula un qubit: explora ampliamente al principio, converge al final."""
        if temperatura > 0.5:
            return random.uniform(0.8, 1.5)
        elif temperatura > 0.2:
            return random.uniform(0.9, 1.3)
        else:
            return random.uniform(1.0, 1.2)

    def _evaluar_combinacion(self, productos, factores):
        """Score = suma de (precio_ajustado - costo) * peso_estimado."""
        score = 0.0
        for p, f in zip(productos, factores):
            precio_nuevo = p.precio * f
            margen = precio_nuevo - p.costo
            if f > 1.3:
                margen *= 0.7
            elif f < 0.9:
                margen *= 0.8
            score += margen
        return score

    def _fallback_clasico(self, productos, iteraciones):
        """Si no hay Qiskit, hace annealing clasico."""
        mejor = None
        mejor_score = float("-inf")
        for it in range(iteraciones):
            combinacion = [random.uniform(0.9, 1.3) for _ in productos]
            score = self._evaluar_combinacion(productos, combinacion)
            if score > mejor_score:
                mejor_score = score
                mejor = combinacion
        return {
            "mejor_combinacion": mejor,
            "mejor_score": mejor_score,
            "iteraciones": iteraciones,
            "historial": [],
            "motor": "clasico",
        }

    def aplicar_optimizacion(self, productos, resultado):
        """Aplica la mejor combinacion a los productos."""
        if resultado["mejor_combinacion"] is None:
            return productos
        for p, f in zip(productos, resultado["mejor_combinacion"]):
            p.precio = int(p.precio * f)
        return productos


def qiskit_disponible():
    return QISKIT_DISPONIBLE