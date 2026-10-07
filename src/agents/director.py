"""Agente Director. Descompone objetivos en subtareas concretas."""
from .base import Agent


class Director(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Director",
            rol="Planifica y prioriza objetivos",
            permisos=["planificar", "priorizar", "asignar_tareas", "reportar"],
            cerebro=cerebro,
        )

    def _ejecutar_especifico(self, tarea):
        objetivo = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("descomponiendo", objetivo=objetivo)

        # Intentar con cerebro (LLM) primero
        prompt = (
            f"Descompone este objetivo empresarial en 3 a 5 subtareas concretas. "
            f"Devuelve SOLO una lista en JSON con la forma "
            f'[{{"descripcion": "...", "agente_sugerido": "..."}}]. '
            f"Objetivo: {objetivo}"
        )
        respuesta_llm = self._usar_cerebro(prompt)

        if respuesta_llm:
            subtareas = self._parsear_respuesta(respuesta_llm, objetivo)
        else:
            subtareas = self._descomponer_simbolico(objetivo)

        self._log("descompuesto", cantidad=len(subtareas))
        return {
            "agente": self.nombre,
            "objetivo": objetivo,
            "subtareas": subtareas,
            "metodo": "llm" if respuesta_llm else "simbolico",
        }

    def _parsear_respuesta(self, respuesta, objetivo):
        import json
        try:
            if isinstance(respuesta, str):
                # limpiar bloques de codigo markdown si vienen
                limpio = respuesta.strip()
                if limpio.startswith("```"):
                    limpio = limpio.split("```")[1]
                    if limpio.startswith("json"):
                        limpio = limpio[4:]
                subtareas = json.loads(limpio)
                return subtareas
        except Exception as e:
            self._log("error_parseo_llm", error=str(e))
        return self._descomponer_simbolico(objetivo)

    def _descomponer_simbolico(self, objetivo):
        """Descomposicion determinista. Reglas fijas, sin IA."""
        base = objetivo.lower()
        subtareas = []

        if "simular" in base or "simulacion" in base or "empresa" in base:
            subtareas = [
                {"descripcion": "Definir parametros de la empresa virtual", "agente_sugerido": "Arquitecto"},
                {"descripcion": "Implementar modelo de clientes y productos", "agente_sugerido": "Developer"},
                {"descripcion": "Implementar modelo de costos y ventas", "agente_sugerido": "Developer"},
                {"descripcion": "Correr escenarios y comparar estrategias", "agente_sugerido": "Quantum_RD"},
                {"descripcion": "Analizar resultados y viabilidad", "agente_sugerido": "Business"},
            ]
        elif "test" in base or "probar" in base:
            subtareas = [
                {"descripcion": "Disenar casos de test", "agente_sugerido": "Tester"},
                {"descripcion": "Implementar tests automatizados", "agente_sugerido": "Developer"},
                {"descripcion": "Correr tests y reportar", "agente_sugerido": "Tester"},
            ]
        elif "optimiz" in base or "maximiz" in base:
            subtareas = [
                {"descripcion": "Definir funcion objetivo y restricciones", "agente_sugerido": "Arquitecto"},
                {"descripcion": "Implementar algoritmo clasico", "agente_sugerido": "Developer"},
                {"descripcion": "Implementar algoritmo quantum-inspired", "agente_sugerido": "Quantum_RD"},
                {"descripcion": "Comparar resultados", "agente_sugerido": "Business"},
            ]
        else:
            subtareas = [
                {"descripcion": f"Analizar objetivo: {objetivo}", "agente_sugerido": "Arquitecto"},
                {"descripcion": "Implementar solucion", "agente_sugerido": "Developer"},
                {"descripcion": "Verificar resultado", "agente_sugerido": "Tester"},
                {"descripcion": "Auditar cumplimiento de GOVERNANCE", "agente_sugerido": "Auditor"},
            ]

        return subtareas