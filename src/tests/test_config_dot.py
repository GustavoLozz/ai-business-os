"""Tests de config y dot_exporter.

Actualizado para v5 del AgentRunner:
- El flujo puede detenerse en esperando_aprobacion.
- Los diagramas generados pueden tener menos pasos.
"""
from pathlib import Path
from src.orchestrator.config import Config
from src.orchestrator.dot_exporter import DotExporter
from src.orchestrator.core import Orchestrator
from src.orchestrator.brains import NullBrain


def _orq_test():
    return Orchestrator(brain=NullBrain())


def test_config_reportar():
    r = Config.reportar()
    assert "dotenv_disponible" in r
    assert "env_file_existe" in r
    assert "solo_lee_del_env_local" in r
    assert r["solo_lee_del_env_local"] is True


def test_config_valores_por_defecto():
    assert Config.MAX_INTENTOS_POR_TAREA == 3
    assert Config.LOG_LEVEL == "INFO"
    assert Config.SIMULADOR_DIAS_DEFAULT == 30
    assert Config.SIMULADOR_CLIENTES_DEFAULT == 100


def test_config_aislado_del_entorno():
    r = Config.reportar()
    assert r["solo_lee_del_env_local"] is True


def test_dot_exporter_crea_directorio(tmp_path):
    d = DotExporter(directorio=tmp_path)
    assert d.directorio.exists()
    assert d.directorio == tmp_path


def test_dot_exporter_sistema(tmp_path):
    o = _orq_test()
    d = DotExporter(directorio=tmp_path)
    r = d.exportar_sistema(o)
    archivo = Path(r["archivo"])
    assert archivo.exists()
    contenido = archivo.read_text(encoding="utf-8")
    assert "digraph sistema" in contenido
    assert "ORCHESTRATOR" in contenido


def test_dot_exporter_flujo(tmp_path):
    o = _orq_test()
    flujo = o.ejecutar_flujo("Simular empresa 30 dias")
    d = DotExporter(directorio=tmp_path)
    r = d.exportar_flujo(flujo)
    archivo = Path(r["archivo"])
    assert archivo.exists()
    contenido = archivo.read_text(encoding="utf-8")
    assert "digraph flujo" in contenido
    assert "Director" in contenido


def test_dot_exporter_tiene_conexiones(tmp_path):
    """El flujo puede detenerse en aprobacion, asi que verificamos >=2 conexiones."""
    o = _orq_test()
    flujo = o.ejecutar_flujo("Simular empresa")
    d = DotExporter(directorio=tmp_path)
    r = d.exportar_flujo(flujo)
    contenido = Path(r["archivo"]).read_text(encoding="utf-8")
    # Al menos: INICIO->N0 y algun nodo mas
    assert contenido.count("->") >= 2


def test_dot_exporter_escapar():
    d = DotExporter()
    assert d._escapar('hola "mundo"') == 'hola \\"mundo\\"'
    assert d._escapar("linea1\nlinea2") == "linea1\\nlinea2"


def test_dot_exporter_colores():
    d = DotExporter()
    assert d._color_agente("Director") == "#BBDEFB"
    assert d._color_agente("Auditor") == "#FFCDD2"
    assert d._color_estado("completada") == "#C8E6C9"
    assert d._color_estado("fallida") == "#FFCDD2"