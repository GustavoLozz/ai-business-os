"""Agente Business. Simula y analiza viabilidad de negocio."""
from .base import Agent


class Business(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Business",
            rol="Simula y analiza negocios",
            permisos=["simular", "analizar", "informar", "proponer_escenarios"],
            cerebro=cerebro,
        )
        self.analisis = []

    def _ejecutar_especifico(self, tarea):
        descripcion = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("analizando", descripcion=descripcion)

        prompt = (
            f"Analiza la viabilidad comercial de esta tarea. "
            f"Devuelve SOLO un JSON con la forma "
            f'{{"viabilidad": "alta|media|baja", "facturacion_estimada": 0, '
            f'"costos_estimados": 0, "margen_pct": 0, "riesgos": ["..."], "recomendacion": "..."}}. '
            f"Tarea: {descripcion}"
        )
        respuesta_llm = self._usar_cerebro(prompt)

        if respuesta_llm:
            analisis = self._parsear_respuesta(respuesta_llm, descripcion)
        else:
            analisis = self._analizar_simbolico(descripcion)

        self.analisis.append(analisis)
        self._log("analisis_completo", viabilidad=analisis.get("viabilidad"))

        return {
            "agente": self.nombre,
            "descripcion": descripcion,
            "analisis": analisis,
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
        return self._analizar_simbolico(descripcion)

    def _analizar_simbolico(self, descripcion):
        """Analisis determinista basado en la descripcion."""
        base = descripcion.lower()

        if "simul" in base or "empresa" in base:
            return {
                "viabilidad": "alta",
                "facturacion_estimada": 8420000,
                "costos_estimados": 4180000,
                "margen_pct": 50.2,
                "clientes_estimados": 184,
                "oportunidades": 327,
                "riesgos": ["parametros irreales", "falta de datos reales"],
                "recomendacion": "Avanzar con simulacion. Comparar con datos reales cuando esten disponibles.",
            }
        elif "optimiz" in base or "maximiz" in base:
            return {
                "viabilidad": "alta",
                "mejora_esperada_pct": 14.7,
                "riesgos": ["convergencia prematura", "costo computacional"],
                "recomendacion": "Probar estrategia quantum-inspired y comparar con clasico.",
            }
        elif "test" in base or "probar" in base:
            return {
                "viabilidad": "alta",
                "riesgos": ["cobertura insuficiente"],
                "recomendacion": "Ampliar cobertura de tests antes de produccion.",
            }
        else:
            return {
                "viabilidad": "media",
                "riesgos": ["informacion insuficiente"],
                "recomendacion": "Profundizar analisis antes de invertir recursos.",
            }