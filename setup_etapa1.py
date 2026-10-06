#!/usr/bin/env python
"""
AI-BUSINESS-OS - Setup Etapa 1
Crea la estructura completa del Orchestrator + 7 agentes registrados.
Regla: checkpoint antes -> crear -> tests -> auditoria -> commit.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

def run(cmd, silent=False):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if not silent and result.stdout:
        print(result.stdout)
    return result.returncode == 0

def write_file(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  OK -> {path}")

print("=" * 60)
print("  AI-BUSINESS-OS - SETUP ETAPA 1")
print("=" * 60)
print()

print("[0/7] Creando checkpoint previo...")
checkpoint_dir = ROOT / "checkpoints"
checkpoint_dir.mkdir(exist_ok=True)
checkpoint_file = checkpoint_dir / f"checkpoint_etapa1_{datetime.now():%Y%m%d_%H%M%S}.json"
checkpoint_data = {
    "fecha": datetime.now().isoformat(),
    "etapa": "etapa1_pre_setup",
    "archivos_antes": [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.py")],
}
checkpoint_file.write_text(json.dumps(checkpoint_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"  OK -> {checkpoint_file.name}")
run("git add . 2>&1")
run('git commit -m "pre-etapa1: checkpoint antes de crear orchestrator" 2>&1', silent=True)
print()

print("[1/7] Creando estructura de carpetas...")
dirs = [
    "src/orchestrator",
    "src/tests",
    "src/agents",
    "memory",
    "logs",
    "checkpoints",
]
for d in dirs:
    (ROOT / d).mkdir(parents=True, exist_ok=True)
print(f"  OK -> {len(dirs)} carpetas verificadas")
print()

print("[2/7] Escribiendo modulos base...")
write_file("src/__init__.py", '"""AI-BUSINESS-OS - paquete principal."""\n__version__ = "0.1.0"\n')
write_file("src/orchestrator/__init__.py", '"""Orchestrator - cerebro operativo."""\n')
write_file("src/tests/__init__.py", '"""Tests del proyecto."""\n')
write_file("src/agents/__init__.py", '"""Agentes del sistema."""\n')
print()

print("[3/7] Escribiendo modulos del Orchestrator...")