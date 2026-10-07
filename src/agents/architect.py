"""Agente Arquitecto. Propone estructura y arquitectura de solucion."""
from .base import Agent


class Architect(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Arquitecto",
            rol="Disena estructura y arquitectura",
            permisos=["disenar", "proponer_estructura", "revisar_arquitectura"],
            cerebro=cerebro,
        )

    def _ejecutar_especifico(self, tarea):
        descripcion = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("disenando", descripcion=descripcion)

        prompt = (
            f"Propone una arquitectura tecnica para esta tarea. "
            f"Devuelve SOLO un JSON con la forma "
            f'{{"componentes": ["..."], "modulos": ["..."], "riesgos": ["..."]}}. '
            f"Tarea: {descripcion}"
        )
        respuesta_llm = self._usar_cerebro(prompt)

        if respuesta_llm:
            arquitectura = self._parsear_respuesta(respuesta_llm, descripcion)
        else:
            arquitectura = self._disenar_simbolico(descripcion)

        self._log("disenado", componentes=len(arquitectura.get("componentes", [])))
        return {
            "agente": self.nombre,
            "descripcion": descripcion,
            "arquitectura": arquitectura,
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
        return self._disenar_simbolico(descripcion)

    def _disenar_simbolico(self, descripcion):
        """Arquitectura determinista basada en la descripcion."""
        base = descripcion.lower()
        componentes = ["modulo_entrada", "modulo_proceso", "modulo_salida"]
        modulos = ["configuracion", "logica", "persistencia"]
        riesgos = ["complejidad excesiva", "falta de tests"]

        if "simul" in base or "empresa" in base:
            componentes = ["modelo_clientes", "modelo_productos", "modelo_costos",
                           "modelo_ventas", "motor_escenarios"]
            modulos = ["clientes.py", "productos.py", "costos.py", "ventas.py", "escenarios.py"]
            riesgos = ["parametros irreales", "datos de entrada incompletos"]
        elif "optimiz" in base or "maximiz" in base:
            componentes = ["funcion_objetivo", "restricciones", "algoritmo_clasico",
                           "algoritmo_quantum", "comparador"]
            modulos = ["objetivo.py", "clasico.py", "quantum.py", "comparador.py"]
            riesgos = ["convergencia prematura", "costo computacional alto"]
        elif "test" in base or "probar" in base:
            componentes = ["runner_tests", "casos_prueba", "reporte_resultados"]
            modulos = ["runner.py", "casos.py", "reporte.py"]
            riesgos = ["cobertura insuficiente"]

        return {
            "componentes": componentes,
            "modulos": modulos,
            "riesgos": riesgos,
            "descripcion_tecnica": f"Arquitectura modular para: {descripcion[:80]}",
        }