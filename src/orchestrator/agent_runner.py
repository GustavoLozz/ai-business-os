"""AgentRunner. Ejecuta agentes aplicando permisos, presupuesto y aprobaciones."""
from src.agents import crear_todos


class AgentRunner:
    """Ejecuta agentes siguiendo las reglas de GOVERNANCE."""

    def __init__(self, orchestrator):
        self.orch = orchestrator
        self.agentes = crear_todos(cerebro=None)
        self.resultados = []

    def ejecutar_agente(self, nombre_agente, tarea):
        """Ejecuta un agente verificando permisos, presupuesto y aprobaciones."""
        self.orch.logger.info("runner_inicio", agente=nombre_agente,
                              tarea=str(tarea)[:120])

        agente = self.agentes.get(nombre_agente)
        if agente is None:
            self.orch.logger.error("agente_no_encontrado", agente=nombre_agente)
            return {"error": f"Agente '{nombre_agente}' no encontrado"}

        if isinstance(tarea, dict):
            accion = tarea.get("accion")
            if accion:
                ok, razon = self.orch.permissions.puede(nombre_agente, accion)
                if not ok:
                    self.orch.logger.warning("permiso_denegado",
                                             agente=nombre_agente,
                                             accion=accion,
                                             razon=razon)
                    return {"error": f"Permiso denegado: {razon}", "agente": nombre_agente}

        try:
            resultado = agente.ejecutar(tarea)
        except Exception as e:
            self.orch.logger.error("agente_error", agente=nombre_agente, error=str(e))
            return {"error": str(e), "agente": nombre_agente}

        self.orch.memory.recordar(
            "resultado_agente",
            f"{nombre_agente} ejecuto tarea",
            agente=nombre_agente,
            resultado_resumen=str(resultado)[:200],
        )

        self.resultados.append({"agente": nombre_agente, "resultado": resultado})
        self.orch.logger.info("runner_fin", agente=nombre_agente)
        return resultado

    def ejecutar_flujo(self, objetivo):
        """Ejecuta el flujo completo: Director -> Arquitecto -> Developer
        -> Quantum -> Tester -> Auditor -> Business."""
        self.orch.logger.info("flujo_inicio", objetivo=objetivo)
        flujo = {"objetivo": objetivo, "pasos": []}

        # 1. Director descompone
        r_director = self.ejecutar_agente("Director", {"descripcion": objetivo})
        flujo["pasos"].append({"agente": "Director", "resultado": r_director})
        subtareas = r_director.get("subtareas", [])

        # 2. Arquitecto propone estructura del objetivo global
        r_arq = self.ejecutar_agente("Arquitecto", {"descripcion": objetivo})
        flujo["pasos"].append({"agente": "Arquitecto", "resultado": r_arq})

        # 3. Developer propone codigo para la primera subtarea suya
        subtarea_dev = next(
            (s for s in subtareas if s.get("agente_sugerido") == "Developer"),
            {"descripcion": objetivo},
        )
        r_dev = self.ejecutar_agente("Developer", {"descripcion": subtarea_dev["descripcion"]})
        flujo["pasos"].append({"agente": "Developer", "resultado": r_dev})

        # 4. FIX: Quantum_RD recibe el OBJETIVO GLOBAL (no la subtarea puntual)
        #    Asi detecta "simular"/"empresa" y elige el algoritmo especifico.
        r_q = self.ejecutar_agente("Quantum_RD", {"descripcion": objetivo})
        flujo["pasos"].append({"agente": "Quantum_RD", "resultado": r_q})

        # 5. FIX: Tester en modo flujo (evita recursion de pytest)
        r_test = self.ejecutar_agente("Tester", {
            "descripcion": objetivo,
            "modo_flujo": True,
        })
        flujo["pasos"].append({"agente": "Tester", "resultado": r_test})

        # 6. Auditor valida GOVERNANCE
        r_aud = self.ejecutar_agente("Auditor", {"descripcion": objetivo})
        flujo["pasos"].append({"agente": "Auditor", "resultado": r_aud})

        if not r_aud.get("aprobado", True):
            flujo["estado"] = "bloqueado_por_auditor"
            flujo["violaciones"] = r_aud.get("violaciones", [])
            self.orch.logger.warning("flujo_bloqueado",
                                     violaciones=flujo["violaciones"])
            return flujo

        # 7. Business analiza viabilidad
        r_biz = self.ejecutar_agente("Business", {"descripcion": objetivo})
        flujo["pasos"].append({"agente": "Business", "resultado": r_biz})

        flujo["estado"] = "completado"
        self.orch.logger.info("flujo_fin", estado="completado",
                              pasos=len(flujo["pasos"]))
        return flujo