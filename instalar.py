#!/usr/bin/env python
"""
AI-BUSINESS-OS - Instalador Etapa 1
Crea orchestrator.py y setup_etapa1.py desde dentro de Python.
Sin heredocs de PowerShell.
"""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

orchestrator_py = """#!/usr/bin/env python
"""AI-1 - Orchestrator CLI
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.cli import main as cli_main

if __name__ == "__main__":
    cli_main()
"""

ROOT.join("orchestrator.py").write_text(orchestrator_py, encoding="utf-8")
print("OK -> orchestrator.py creado")
print("")
print("AHORA EJECUTA SETUP_ETAPA_1")
print("")
print("No te olvides de ejecutar el setup de la Etapa 1.")
