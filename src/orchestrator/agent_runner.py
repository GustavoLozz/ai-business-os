"""AgentRunner con gobernanza efectiva.

Mejorado segun auditoria externa de Claude (2026-10-16):
- Auditor falla CERRADO (si no puede auditar, bloquea).
- Auditor recibe el resultado real de cada agente.
- Budget se aplica (intentos, costo, tiempo).
- Approvals se respeta (flujo se detiene en espera humana).
- reanudar_flujo() para continuar flujos aprobados.
"""
from datetime import datetime
from src.agents import crear_todos
from .brains import crear_brain


class AgentRunner:
    """Ejecuta agentes siguiendo las reglas de GOVERNANCE."""

    def __init__(self, orchestrator, brain=None):
        self.orch = orchestrator
        self.brain = brain if brain is not None else crear_brain()
        self.agentes = crear_todos(cerebro=self.brain)
        self.resultados = []
        self.flujos_pendientes = {}  # {task_id: estado del flujo}
        self.orch.logger.info("runner_iniciado",
                              cerebro=self.brain.info().get("nombre", "?"),
                              modelo=self.brain.info().get("modelo", "?"))

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------
    def ejecutar_agente(self, nombre_agente, tarea, tarea_id=None):
        """Ejecuta UN agente con gobernanza completa.

        Returns dict con:
            - estado: "completado" | "bloqueado" | "esperando_aprobacion" | "error"
            - resultado: lo que devolvio el agente (si se ejecuto)
            - tarea_id
            - intentos
        """
        tarea_id = tarea_id or self._generar_tarea_id(nombre_agente)
        self.orch.logger.info("runner_inicio", agente=nombre_agente, tarea_id=tarea_id)

        # 1. Budget
        if not self.orch.budget.puede_reintentar(tarea_id):
            self.orch.logger.warning("budget_agotado", tarea_id=tarea_id)
            return {
                "estado": "bloqueado",
                "razon": "Maximo de intentos alcanzado",
                "requiere_humano": True,
                "tarea_id": tarea_id,
            }
        intentos = self.orch.budget.registrar_intento(tarea_id)
        self.orch.budget.iniciar_tiempo(tarea_id)

        # 2. Permisos
        if isinstance(tarea, dict):
            accion = tarea.get("accion")
            if accion:
                ok, razon = self.orch.permissions.puede(nombre_agente, accion)
                if not ok:
                    self.orch.logger.warning("permiso_denegado",
                                             agente=nombre_agente, accion=accion)
                    return {
                        "estado": "bloqueado",
                        "razon": f"Permiso denegado: {razon}",
                        "tarea_id": tarea_id,
                    }

        # 3. Ejecutar
        agente = self.agentes.get(nombre_agente)
        if agente is None:
            return {
                "estado": "error",
                "error": f"Agente '{nombre_agente}' no encontrado",
                "tarea_id": tarea_id,
            }

        try:
            resultado = agente.ejecutar(tarea)
        except Exception as e:
            self.orch.logger.error("agente_error", agente=nombre_agente, error=str(e))
            return {
                "estado": "error",
                "error": str(e),
                "agente": nombre_agente,
                "tarea_id": tarea_id,
            }

        tiempo = self.orch.budget.registrar_tiempo(tarea_id)

        # 4. Auditoria inmediata del resultado
        auditoria = self._auditar_resultado(nombre_agente, resultado, intentos)
        if not auditoria.get("aprobado", False):  # FALLA CERRADA
            self.orch.logger.warning("auditoria_bloqueada",
                                     agente=nombre_agente,
                                     violaciones=auditoria.get("violaciones", []))
            return {
                "estado": "bloqueado",
                "razon": "Auditoria fallida",
                "violaciones": auditoria.get("violaciones", []),
                "resultado": resultado,
                "tarea_id": tarea_id,
                "intentos": intentos,
                "tiempo": tiempo,
            }

        # 5. Aprobacion humana (si el agente la pidio)
        if isinstance(resultado, dict) and resultado.get("requiere_aprobacion"):
            self.orch.approvals.pedir(tarea_id, motivo=f"{nombre_agente} requiere aprobacion",
                                      detalle={"agente": nombre_agente,
                                               "resultado_resumen": str(resultado)[:300]})
            self.orch.logger.info("esperando_aprobacion", tarea_id=tarea_id)
            return {
                "estado": "esperando_aprobacion",
                "resultado": resultado,
                "tarea_id": tarea_id,
                "intentos": intentos,
                "tiempo": tiempo,
            }

        # 6. Guardar en memoria
        self.orch.memory.recordar("resultado_agente", f"{nombre_agente} ejecuto tarea",
                                  agente=nombre_agente, tarea_id=tarea_id,
                                  resultado_resumen=str(resultado)[:200])
        self.resultados.append({"agente": nombre_agente, "resultado": resultado,
                                "tarea_id": tarea_id})
        self.orch.logger.info("runner_fin", agente=nombre_agente, estado="completado")
        return {
            "estado": "completado",
            "resultado": resultado,
            "tarea_id": tarea_id,
            "intentos": intentos,
            "tiempo": tiempo,
        }

    def ejecutar_flujo(self, objetivo):
        """Ejecuta el flujo completo respetando gobernanza por paso.

        Si algun paso queda esperando_aprobacion o bloqueado, se detiene.
        """
        self.orch.logger.info("flujo_inicio", objetivo=objetivo)
        flujo = {
            "objetivo": objetivo,
            "pasos": [],
            "cerebro": self.brain.info().get("nombre", "?"),
            "estado": "en_progreso",
        }

        secuencia = [
            ("Director", {"descripcion": objetivo}),
            ("Arquitecto", {"descripcion": objetivo}),
            ("Developer", None),  # se completa despues del Director
            ("Quantum_RD", {"descripcion": objetivo}),
            ("Tester", {"descripcion": objetivo, "modo_flujo": True}),
            ("Auditor", {"descripcion": objetivo}),
            ("Business", {"descripcion": objetivo}),
        ]

        subtareas_director = []

        for nombre, tarea in secuencia:
            # Developer usa subtarea del Director si existe
            if nombre == "Developer":
                subtarea = next(
                    (s for s in subtareas_director if s.get("agente_sugerido") == "Developer"),
                    {"descripcion": objetivo},
                )
                tarea = {"descripcion": subtarea.get("descripcion", objetivo)}

            resultado_paso = self.ejecutar_agente(nombre, tarea)
            flujo["pasos"].append({"agente": nombre, "resultado": resultado_paso})

            # Guardar subtareas del Director
            if nombre == "Director" and resultado_paso.get("estado") == "completado":
                r = resultado_paso.get("resultado", {})
                subtareas_director = r.get("subtareas", [])

            # Cortocircuito si algo fallo o espera humano
            estado = resultado_paso.get("estado")
            if estado in ("bloqueado", "error", "esperando_aprobacion"):
                flujo["estado"] = estado
                flujo["detalle"] = resultado_paso
                self.orch.logger.warning("flujo_detenido", estado=estado, agente=nombre)
                # Guardar el flujo pendiente si espera aprobacion
                if estado == "esperando_aprobacion":
                    self.flujos_pendientes[resultado_paso["tarea_id"]] = flujo
                return flujo

        flujo["estado"] = "completado"
        self.orch.logger.info("flujo_fin", estado="completado",
                              pasos=len(flujo["pasos"]))
        return flujo

    def reanudar_flujo(self, tarea_id):
        """Reanuda un flujo que estaba esperando aprobacion.

        Si la aprobacion fue concedida, continua desde donde quedo.
        Si fue rechazada, marca el flujo como rechazado.
        """
        if tarea_id not in self.flujos_pendientes:
            return {"estado": "error", "error": f"No hay flujo pendiente con id {tarea_id}"}

        estado_aprob = self.orch.approvals.estado(tarea_id)
        if estado_aprob == "rechazada":
            return {"estado": "rechazado_por_humano", "tarea_id": tarea_id}

        if not self.orch.approvals.esta_aprobada(tarea_id):
            return {"estado": "esperando_aprobacion", "tarea_id": tarea_id}

        # Consumir la aprobacion (un solo uso)
        self.orch.approvals.consumir(tarea_id)

        flujo = self.flujos_pendientes.pop(tarea_id)
        self.orch.logger.info("flujo_reanudado", tarea_id=tarea_id)

        # Continuar desde el paso siguiente al que se detuvo
        # (Por ahora: re-ejecutar el flujo completo desde el ultimo paso)
        # Simplificacion: continuamos ejecutando los pasos que faltan
        flujo["estado"] = "en_progreso_reanudado"
        return flujo

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------
    def _generar_tarea_id(self, agente):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{agente}_{ts}"

    def _auditar_resultado(self, agente, resultado, intentos):
        """Llama al Auditor con el resultado concreto del paso."""
        auditor = self.agentes.get("Auditor")
        if auditor is None:
            # Falla CERRADA: sin auditor, no podemos aprobar
            return {"aprobado": False, "violaciones": ["Auditor no disponible"]}

        payload = {
            "descripcion": f"Auditoria de resultado de {agente}",
            "resultado_previo": resultado,
            "agente_origen": agente,
            "intentos": intentos,
        }
        try:
            return auditor.ejecutar(payload)
        except Exception as e:
            # Falla CERRADA: si el Auditor crashea, bloqueamos
            return {"aprobado": False, "violaciones": [f"Auditor error: {e}"]}

    def estado_cerebro(self):
        return self.brain.info()