"""Generador de reportes automaticos."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"


class Reports:
    def __init__(self, orchestrator):
        self.orch = orchestrator
        self.hoy = datetime.now().strftime("%Y-%m-%d")
        self.dir = REPORTS_DIR / self.hoy
        self.dir.mkdir(parents=True, exist_ok=True)

    def generar_todos(self):
        self.daily_report()
        self.business_report()
        self.agent_report()
        self.security_report()
        self.errors_report()
        return self.dir

    def daily_report(self):
        e = self.orch.estado()
        lineas = [
            f"# AI-BUSINESS-OS - Reporte Diario",
            "",
            f"Fecha: {self.hoy}",
            f"Generado: {datetime.now().isoformat()}",
            "",
            "## Estado del sistema",
            f"- Agentes registrados: {e['agentes']}",
            f"- Tareas totales: {e['tareas']['total']}",
            f"- Memorias guardadas: {e['memoria']['total']}",
            f"- Pendientes de aprobacion: {e['pendientes_aprobacion']}",
            "",
            "## Detalle de tareas",
            f"```json",
            json.dumps(e['tareas'], indent=2, ensure_ascii=False),
            f"```",
            "",
            "## Regla vigente",
            "Nada destructivo. Todo con checkpoint.",
        ]
        (self.dir / "daily-report.md").write_text("\n".join(lineas), encoding="utf-8")
        return self.dir / "daily-report.md"

    def business_report(self):
        data = {
            "fecha": self.hoy,
            "estado": "etapa2_en_construccion",
            "empresa_simulada": {
                "facturacion": 0,
                "costos": 0,
                "margen_pct": 0,
                "clientes": 0,
                "oportunidades": 0,
            },
            "nota": "La empresa simulada se construye en Etapa 4",
        }
        (self.dir / "business-report.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return self.dir / "business-report.json"

    def agent_report(self):
        agentes = self.orch.registry.listar()
        data = {
            "fecha": self.hoy,
            "total": len(agentes),
            "agentes": agentes,
        }
        (self.dir / "agent-report.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return self.dir / "agent-report.json"

    def security_report(self):
        data = {
            "fecha": self.hoy,
            "reglas_activas": [
                "Ningun agente modifica main directamente",
                "Maximo 3 intentos por tarea",
                "Cambios criticos requieren aprobacion",
                "Prohibido borrar sin permiso",
                "Prohibido operar cuentas reales",
            ],
            "alertas": [],
            "estado": "OK",
        }
        (self.dir / "security-report.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return self.dir / "security-report.json"

    def errors_report(self):
        log_file = ROOT / "logs" / "orchestrator.log"
        errores = []
        if log_file.exists():
            for linea in log_file.read_text(encoding="utf-8").splitlines():
                try:
                    entry = json.loads(linea)
                    if entry.get("nivel") in ("ERROR", "WARNING"):
                        errores.append(entry)
                except json.JSONDecodeError:
                    continue
        data = {
            "fecha": self.hoy,
            "total_errores": len([e for e in errores if e.get("nivel") == "ERROR"]),
            "total_warnings": len([e for e in errores if e.get("nivel") == "WARNING"]),
            "entradas": errores[-50:],
        }
        (self.dir / "errors.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return self.dir / "errors.json"