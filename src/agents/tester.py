"""Agente Tester. Crea y corre tests automaticamente."""
from .base import Agent
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Tester(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Tester",
            rol="Crea y corre tests",
            permisos=["crear_tests", "correr_tests", "reportar_bugs"],
            cerebro=cerebro,
        )
        self.resultados = []

    def _ejecutar_especifico(self, tarea):
        descripcion = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("preparando_tests", descripcion=descripcion)

        # Correr la suite de tests actual del proyecto
        resultado = self._correr_suite()
        self.resultados.append(resultado)
        self._log("tests_corridos", passed=resultado.get("passed", 0),
                  failed=resultado.get("failed", 0))

        return {
            "agente": self.nombre,
            "descripcion": descripcion,
            "resultado": resultado,
        }

    def _correr_suite(self):
        """Corre pytest sobre src/tests/ y devuelve resumen."""
        cmd = [str(ROOT / ".venv" / "Scripts" / "python.exe"),
               "-m", "pytest", "src/tests/", "-q", "--tb=no"]
        try:
            proc = subprocess.run(
                cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=60
            )
            salida = proc.stdout + proc.stderr
            passed = 0
            failed = 0
            for linea in salida.splitlines():
                if " passed" in linea:
                    partes = linea.replace(",", " ").split()
                    for i, p in enumerate(partes):
                        if p == "passed":
                            try:
                                passed = int(partes[i - 1])
                            except (ValueError, IndexError):
                                pass
                        if p == "failed":
                            try:
                                failed = int(partes[i - 1])
                            except (ValueError, IndexError):
                                pass
            return {
                "passed": passed,
                "failed": failed,
                "returncode": proc.returncode,
                "resumen": salida.strip().splitlines()[-1] if salida.strip() else "",
            }
        except subprocess.TimeoutExpired:
            return {"passed": 0, "failed": 0, "returncode": -1, "resumen": "TIMEOUT"}
        except Exception as e:
            self._log("error_tests", error=str(e))
            return {"passed": 0, "failed": 0, "returncode": -1, "resumen": f"ERROR: {e}"}