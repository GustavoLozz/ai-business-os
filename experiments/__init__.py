"""Experimentos de AI-BUSINESS-OS."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTADOS_DIR = ROOT / "experiments" / "resultados"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ["RESULTADOS_DIR", "ROOT"]