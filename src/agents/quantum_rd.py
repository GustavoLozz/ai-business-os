"""Agente Quantum/R&D. Experimenta con algoritmos quantum-inspired en sandbox."""
from .base import Agent
import random


class QuantumRD(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Quantum_RD",
            rol="Experimenta con quantum-inspired",
            permisos=["experimentar", "crear_sandbox", "analizar_resultados"],
            cerebro=cerebro,
        )
        self.experimentos = []

    def _ejecutar_especifico(self, tarea):
        descripcion = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("experimentando", descripcion=descripcion)

        prompt = (
            f"Propone un experimento quantum-inspired para esta tarea. "
            f"Devuelve SOLO un JSON con la forma "
            f'{{"algoritmo": "...", "parametros": {{}}, "hipotesis": "...", "metricas": ["..."]}}. '
            f"Tarea: {descripcion}"
        )
        respuesta_llm = self._usar_cerebro(prompt)

        if respuesta_llm:
            experimento = self._parsear_respuesta(respuesta_llm, descripcion)
        else:
            experimento = self._experimentar_simbolico(descripcion)

        # Simular resultado del experimento (deterministico para tests)
        resultado = self._simular_resultado(experimento)
        experimento["resultado_simulado"] = resultado

        self.experimentos.append(experimento)
        self._log("experimento_completo", algoritmo=experimento.get("algoritmo"))

        return {
            "agente": self.nombre,
            "descripcion": descripcion,
            "experimento": experimento,
            "sandbox": True,
            "metodo": "llm" if respuesta_llm else "simbolico",
        }

    def _parsear_respuesta(self, respuesta, descripcion):
        import json
        try:
            if isinstance(respuesta, str):
                limpio = respuesta.strip()
                if limpio.startswith("```"):
                    limpio = limpio.split("```")[1]
                    if limpio.startswith("json"):
                        limpio = limpio[4:]
                return json.loads(limpio)
        except Exception as e:
            self._log("error_parseo_llm", error=str(e))
        return self._experimentar_simbolico(descripcion)

    def _experimentar_simbolico(self, descripcion):
        base = descripcion.lower()

        if "optimiz" in base or "maximiz" in base:
            return {
                "algoritmo": "QAOA (Quantum Approximate Optimization Algorithm)",
                "parametros": {"capas": 3, "shots": 1024, "optimizador": "COBYLA"},
                "hipotesis": "QAOA encontrara mejor solucion que algoritmo clasico en espacio de busqueda grande",
                "metricas": ["valor_objetivo", "tiempo_ejecucion", "convergencia"],
            }
        elif "simul" in base or "empresa" in base:
            return {
                "algoritmo": "Quantum-Inspired Simulated Annealing",
                "parametros": {"temperatura_inicial": 100.0, "iteraciones": 1000, "enfriamiento": 0.95},
                "hipotesis": "El annealing cuantico-inspired explorara mejor el espacio de escenarios",
                "metricas": ["mejor_escenario", "diversidad", "estabilidad"],
            }
        elif "clasific" in base or "predic" in base:
            return {
                "algoritmo": "Quantum Kernel Method",
                "parametros": {"qubits": 4, "feature_map": "ZZFeatureMap", "reps": 2},
                "hipotesis": "El kernel cuantico separara mejor clientes de alto valor",
                "metricas": ["precision", "recall", "f1"],
            }
        else:
            return {
                "algoritmo": "Variational Quantum Eigensolver (VQE) simplificado",
                "parametros": {"qubits": 3, "capas": 2, "shots": 512},
                "hipotesis": "El enfoque variacional dara una solucion aproximada util",
                "metricas": ["energia_final", "iteraciones", "precision"],
            }

    def _simular_resultado(self, experimento):
        """Simula un resultado determinista basado en el algoritmo."""
        algoritmo = experimento.get("algoritmo", "")

        if "QAOA" in algoritmo:
            return {"valor_objetivo": 0.87, "tiempo_ejecucion_seg": 2.3, "convergencia": 0.94}
        elif "Annealing" in algoritmo:
            return {"mejor_escenario": "B", "diversidad": 0.72, "estabilidad": 0.88}
        elif "Kernel" in algoritmo:
            return {"precision": 0.81, "recall": 0.79, "f1": 0.80}
        else:
            return {"energia_final": -1.42, "iteraciones": 87, "precision": 0.76}