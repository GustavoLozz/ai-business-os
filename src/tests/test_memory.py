"""Tests de la memoria persistente."""
import tempfile
from pathlib import Path
from src.orchestrator.memory import Memory


def test_recordar_y_buscar():
    with tempfile.TemporaryDirectory() as tmp:
        m = Memory(Path(tmp) / "mem.json")
        m.recordar("test", "contenido 1")
        m.recordar("test", "contenido 2")
        m.recordar("otra", "contenido 3")
        assert len(m.buscar("test")) == 2
        assert len(m.buscar()) == 3


def test_estadisticas():
    with tempfile.TemporaryDirectory() as tmp:
        m = Memory(Path(tmp) / "mem.json")
        m.recordar("a", "x")
        m.recordar("b", "y")
        stats = m.estadisticas()
        assert stats["total"] == 2
        assert stats["por_categoria"]["a"] == 1
        assert stats["por_categoria"]["b"] == 1