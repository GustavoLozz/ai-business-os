"""Sistema de permisos por agente."""

PERMISOS = {
    "Director": {"puede": ["planificar", "priorizar", "asignar_tareas", "reportar"],
                 "no_puede": ["modificar_codigo", "borrar_archivos", "operar_cuentas"]},
    "Arquitecto": {"puede": ["disenar", "proponer_estructura", "revisar_arquitectura"],
                   "no_puede": ["modificar_produccion", "borrar_archivos"]},
    "Developer": {"puede": ["escribir_codigo", "modificar_codigo", "crear_archivos"],
                  "no_puede": ["tocar_main", "borrar_sin_permiso", "operar_cuentas"]},
    "Quantum_RD": {"puede": ["experimentar", "crear_sandbox", "analizar_resultados"],
                   "no_puede": ["consumir_sin_limite", "modificar_produccion"]},
    "Tester": {"puede": ["crear_tests", "correr_tests", "reportar_bugs"],
               "no_puede": ["modificar_codigo_produccion"]},
    "Auditor": {"puede": ["revisar", "bloquear", "informar", "auditar"],
                "no_puede": ["modificar_nada"]},
    "Business": {"puede": ["simular", "analizar", "informar", "proponer_escenarios"],
                 "no_puede": ["operar_cuentas_reales", "enviar_mensajes_reales"]},
}


class PermissionSystem:
    def __init__(self):
        self.permisos = PERMISOS

    def puede(self, agente, accion):
        if agente not in self.permisos:
            return False, f"Agente desconocido: {agente}"
        if accion in self.permisos[agente]["no_puede"]:
            return False, f"{agente} NO puede {accion}"
        if accion in self.permisos[agente]["puede"]:
            return True, f"{agente} puede {accion}"
        return False, f"Accion no definida: {accion}"

    def listar(self, agente=None):
        if agente:
            return self.permisos.get(agente, {})
        return self.permisos