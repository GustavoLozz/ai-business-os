"""Tests del generador de reportes."""
import json
from src.orchestrator.core import Orchestrator
from src.orchestrator.reports import Reports


def test_reports_genera_todos():
    o = Orchestrator()
    r = Reports(o)
    dir_reporte = r.generar_todos()
    assert dir_reporte.exists()
    assert (dir_reporte / "daily-report.md").exists()
    assert (dir_reporte / "business-report.json").exists()
    assert (dir_reporte / "agent-report.json").exists()
    assert (dir_reporte / "security-report.json").exists()
    assert (dir_reporte / "errors.json").exists()


def test_agent_report_tiene_7_agentes():
    o = Orchestrator()
    r = Reports(o)
    r.agent_report()
    data = json.loads((r.dir / "agent-report.json").read_text(encoding="utf-8"))
    assert data["total"] == 7


def test_security_report_tiene_reglas():
    o = Orchestrator()
    r = Reports(o)
    r.security_report()
    data = json.loads((r.dir / "security-report.json").read_text(encoding="utf-8"))
    assert len(data["reglas_activas"]) >= 5
    assert data["estado"] == "OK"