"""Tests del informe ejecutivo."""
from pathlib import Path
from src.orchestrator.core import Orchestrator
from src.orchestrator.executive_report import ExecutiveReport


def test_executive_report_crea_instancia():
    o = Orchestrator()
    r = ExecutiveReport(o)
    assert r is not None
    assert r.hoy is not None


def test_generar_devuelve_dict():
    o = Orchestrator()
    informe = ExecutiveReport(o).generar()
    assert isinstance(informe, dict)
    assert "fecha" in informe
    assert "sistema" in informe
    assert "agentes" in informe
    assert "ultima_simulacion" in informe
    assert "recomendaciones" in informe
    assert "proximos_pasos" in informe


def test_generar_tiene_7_agentes():
    o = Orchestrator()
    informe = ExecutiveReport(o).generar()
    assert len(informe["agentes"]) == 7
    nombres = [a["nombre"] for a in informe["agentes"]]
    assert "Director" in nombres
    assert "Auditor" in nombres
    assert "Business" in nombres


def test_generar_guarda_archivos():
    o = Orchestrator()
    r = ExecutiveReport(o)
    informe = r.generar()
    archivo_md = r.dir / "informe-ejecutivo.md"
    archivo_json = r.dir / "informe-ejecutivo.json"
    assert archivo_md.exists()
    assert archivo_json.exists()


def test_informe_markdown_tiene_secciones():
    o = Orchestrator()
    r = ExecutiveReport(o)
    r.generar()
    contenido = (r.dir / "informe-ejecutivo.md").read_text(encoding="utf-8")
    assert "# AI-BUSINESS-OS - Informe Ejecutivo" in contenido
    assert "## 1. Estado del Sistema" in contenido
    assert "## 2. Estado de los Agentes" in contenido
    assert "## 3. Ultima Simulacion" in contenido
    assert "## 4. Recomendaciones" in contenido
    assert "## 5. Proximos Pasos" in contenido


def test_informe_json_es_valido():
    import json
    o = Orchestrator()
    r = ExecutiveReport(o)
    r.generar()
    contenido = (r.dir / "informe-ejecutivo.json").read_text(encoding="utf-8")
    data = json.loads(contenido)
    assert data["fecha"]
    assert data["sistema"]["agentes_registrados"] == 7