"""Agente Auditor. Revisa y bloquea si algo no cumple GOVERNANCE.

Mejorado segun auditoria externa de Claude (2026-10-16):
- Audita el RESULTADO, no solo la intencion.
- Detecta patrones peligrosos en el codigo propuesto por el Developer.
- Reglas por lista cerrada de lo prohibido.
- Falla cerrada (si no puede auditar, bloquea).
- Verifica el sandbox del Developer.
- Modo LLM opcional como segunda opinion.
"""
from .base import Agent
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


# Lista cerrada de patrones peligrosos
PATRONES_PELIGROSOS = [
    "os.system",
    "subprocess.call",
    "subprocess.run",
    "subprocess.Popen",
    "eval(",
    "exec(",
    "rm -rf",
    "shutil.rmtree",
    "__import__",
    "open('/etc/",
    "open('C:\\Windows",
]

# Rutas que el Developer NUNCA debe tocar
RUTAS_PROTEGIDAS = [
    "GOVERNANCE.md",
    ".env",
    ".git",
    "src/orchestrator/",
    "src/agents/auditor.py",
    "src/agents/base.py",
]


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
        self._log("auditando", descripcion=descripcion[:100])

        violaciones = []
        violaciones.extend(self._reglas_estructurales(tarea))
        violaciones.extend(self._reglas_resultado(tarea))
        violaciones.extend(self._reglas_codigo(tarea))
        violaciones.extend(self._reglas_intentos(tarea))

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

    # ------------------------------------------------------------------
    # Reglas
    # ------------------------------------------------------------------
    def _reglas_estructurales(self, tarea):
        """Verifica que GOVERNANCE.md exista."""
        violaciones = []
        if not (ROOT / "GOVERNANCE.md").exists():
            violaciones.append("GOVERNANCE.md no encontrado")
        return violaciones

    def _reglas_resultado(self, tarea):
        """Audita el resultado concreto del agente que se esta auditando."""
        violaciones = []
        if not isinstance(tarea, dict):
            return violaciones

        resultado = tarea.get("resultado_previo") or tarea
        agente_origen = tarea.get("agente_origen", "")

        # Developer debe trabajar en sandbox
        if agente_origen == "Developer":
            if not resultado.get("sandbox", False):
                violaciones.append("Developer intento escribir fuera de sandbox")
            if not resultado.get("requiere_aprobacion", False):
                violaciones.append("Developer no marco requiere_aprobacion=True")

        # Prohibiciones explicitas
        accion = str(resultado.get("accion", "")).lower()
        if "operar_cuenta" in accion or "operar_cuentas" in accion:
            violaciones.append("Intento de operar cuentas reales")
        if "enviar_mensaje" in accion or "enviar_mensajes" in accion:
            violaciones.append("Intento de enviar mensajes reales")
        if "borrar" in accion and not resultado.get("aprobado_borrado", False):
            violaciones.append("Intento de borrar sin aprobacion")
        if "modificar main" in accion or "tocar_main" in accion:
            violaciones.append("Intento de modificar main directamente")

        return violaciones

    def _reglas_codigo(self, tarea):
        """Inspecciona el codigo propuesto por el Developer."""
        violaciones = []
        resultado = tarea.get("resultado_previo") or {}
        propuesta = resultado.get("propuesta") or {}
        archivos = propuesta.get("archivos", [])

        for arch in archivos:
            nombre = arch.get("nombre", "?")
            contenido = arch.get("contenido", "")

            if not isinstance(contenido, str):
                continue

            # Patrones peligrosos
            for patron in PATRONES_PELIGROSOS:
                if patron in contenido:
                    violaciones.append(
                        f"Codigo contiene patron peligroso: '{patron}' en {nombre}"
                    )

            # Rutas protegidas
            for ruta in RUTAS_PROTEGIDAS:
                if ruta in contenido or nombre == ruta:
                    violaciones.append(
                        f"Codigo intenta tocar ruta protegida: '{ruta}' en {nombre}"
                    )

        return violaciones

    def _reglas_intentos(self, tarea):
        """Verifica que no se exceda el maximo de intentos."""
        violaciones = []
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