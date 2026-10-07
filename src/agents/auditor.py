"""Agente Auditor. Revisa, valida y bloquea si algo no cumple GOVERNANCE."""
from .base import Agent
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Auditor(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Auditor",
            rol="Revisa, audita y bloquea si es necesario",
            permisos=["revisar", "bloquear", "informar", "auditar"],
            cerebro=cerebro,
        )
        self.auditorias = []

    def _ejecutar_especifico(self, tarea):
        descripcion = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("auditando", descripcion=descripcion)

        # Reglas de GOVERNANCE a verificar
        violaciones = self._verificar_governance(tarea)

        aprobado = len(violaciones) == 0
        resultado = {
            "agente": self.nombre,
            "descripcion": descripcion,
            "aprobado": aprobado,
            "violaciones": violaciones,
            "veredicto": "APROBADO" if aprobado else "BLOQUEADO",
        }

        self.auditorias.append(resultado)
        self._log("auditoria_completa", aprobado=aprobado, violaciones=len(violaciones))

        return resultado

    def _verificar_governance(self, tarea):
        """Verifica reglas de GOVERNANCE.md."""
        violaciones = []

        # GOVERNANCE.md debe existir
        governance = ROOT / "GOVERNANCE.md"
        if not governance.exists():
            violaciones.append("GOVERNANCE.md no encontrado")

        # Regla: no tocar main
        if isinstance(tarea, dict):
            accion = str(tarea.get("accion", "")).lower()
            if "main" in accion and "modificar" in accion:
                violaciones.append("Intento de modificar main directamente")

            # Regla: no borrar sin permiso
            if "borrar" in accion and not tarea.get("aprobado_borrado", False):
                violaciones.append("Intento de borrar sin aprobacion")

            # Regla: no operar cuentas reales
            if "operar_cuenta" in accion or "operar_cuentas" in accion:
                violaciones.append("Intento de operar cuentas reales")

            # Regla: no enviar mensajes reales
            if "enviar_mensaje" in accion or "enviar_mensajes" in accion:
                violaciones.append("Intento de enviar mensajes reales")

        # Regla: max 3 intentos
        if isinstance(tarea, dict):
            intentos = tarea.get("intentos", 0)
            if intentos >= 3:
                violaciones.append(f"Se alcanzo el maximo de intentos ({intentos})")

        return violaciones

    def bloquear(self, resultado_auditoria):
        """Fuerza el bloqueo de una tarea."""
        return {
            "bloqueado": True,
            "razon": resultado_auditoria.get("violaciones", []),
        }