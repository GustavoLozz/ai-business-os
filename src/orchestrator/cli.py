"""Interfaz de linea de comandos del Orchestrator."""
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description="AI-BUSINESS-OS - Orchestrator CLI")
    parser.add_argument("--objetivo", type=str)
    parser.add_argument("--desde-archivo", action="store_true")
    parser.add_argument("--estado", action="store_true")
    parser.add_argument("--panel", action="store_true")
    parser.add_argument("--listar-agentes", action="store_true")
    parser.add_argument("--aprobar", type=str)
    parser.add_argument("--rechazar", type=str)

    args = parser.parse_args()

    sys.path.insert(0, str(ROOT))
    from src.orchestrator.core import Orchestrator
    orch = Orchestrator()

    if args.listar_agentes:
        print("Agentes registrados:")
        for a in orch.registry.listar():
            print(f"  [{a['estado']}] {a['nombre']:15} - {a['rol']}")
        return

    if args.estado:
        import json
        print(json.dumps(orch.estado(), indent=2, ensure_ascii=False))
        return

    if args.panel:
        print(orch.panel())
        return

    if args.objetivo:
        tarea = orch.recibir_objetivo(args.objetivo)
        print(f"Objetivo recibido. Tarea creada: {tarea['id']}")
        print(orch.panel())
        return

    if args.desde_archivo:
        archivo = ROOT / "objetivo.txt"
        if not archivo.exists():
            print("ERROR: no existe objetivo.txt")
            return
        objetivo = archivo.read_text(encoding="utf-8").strip()
        tarea = orch.recibir_objetivo(objetivo)
        print(f"Objetivo leido de archivo. Tarea creada: {tarea['id']}")
        print(orch.panel())
        return

    parser.print_help()


if __name__ == "__main__":
    main()