"""Agente Tester. Verifica que los agentes funcionan."""
from .base import Agent
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
        self._log("preparando_verificacion", descripcion=descripcion)

        resultado = self._verificacion_interna()

        self.resultados.append(resultado)
        self._log("verificacion_completa", passed=resultado.get("passed", 0),
                  failed=resultado.get("failed", 0))

        return {
            "agente": self.nombre,
            "descripcion": descripcion,
            "resultado": resultado,
            "modo": "verificacion_interna",
        }

    def _verificacion_interna(self):
        """Verifica los 7 agentes SIN subprocess. Rapido y sin recursion."""
        from src.agents import (Director, Architect, Developer, QuantumRD,
                                Tester as _T, Auditor, Business)

        agentes = [Director(), Architect(), Developer(), QuantumRD(),
                   _T(), Auditor(), Business()]

        passed = 0
        failed = 0
        detalles = []

        for a in agentes:
            try:
                rep = a.reportar()
                if rep.get("nombre") and rep.get("rol"):
                    passed += 1
                    detalles.append(f"{a.nombre}: OK")
                else:
                    failed += 1
                    detalles.append(f"{a.nombre}: SIN DATOS")
            except Exception as e:
                failed += 1
                detalles.append(f"{a.nombre}: ERROR {e}")

        return {
            "passed": passed,
            "failed": failed,
            "returncode": 0 if failed == 0 else 1,
            "resumen": f"{passed} agentes OK, {failed} con problemas",
            "detalles": detalles,
        }