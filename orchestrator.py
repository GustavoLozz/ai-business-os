#!/usr/bin/env python
"""
AI-BUSINESS-OS - Orchestrator CLI
Punto de entrada principal del sistema.
"""
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.orchestrator.cli import main as cli_main

if __name__ == "__main__":
    cli_main()