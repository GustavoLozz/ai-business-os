"""Interfaz de linea de comandos del Orchestrator."""
import sys
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _imprimir_flujo(flujo):
    """Imprime el resultado del flujo de forma legible."""
    print("=" * 60)
    print(f"  FLUJO: {flujo.get('objetivo', '')[:50]}")
    print("=" * 60)
    print(f"  Estado: {flujo.get('estado', 'desconocido')}")
    print(f"  Pasos ejecutados: {len(flujo.get('pasos', []))}")
    print("-" * 60)
    for paso in flujo.get("pasos", []):
        agente = paso.get("agente", "?")
        r = paso.get("resultado", {})
        print(f"  [{agente}]")
        if "subtareas" in r:
            print(f"    -> {len(r['subtareas'])} subtareas generadas")
        elif "arquitectura" in r:
            comp = r["arquitectura"].get("componentes", [])
            print(f"    -> {len(comp)} componentes propuestos")
        elif "propuesta" in r:
            archivos = r["propuesta"].get("archivos", [])
            print(f"    -> {len(archivos)} archivos propuestos (sandbox)")
        elif "experimento" in r:
            algo = r["experimento"].get("algoritmo", "")
            print(f"    -> experimento: {algo[:40]}")
        elif "resultado" in r and "passed" in r["resultado"]:
            print(f"    -> tests: {r['resultado']['passed']} passed, {r['resultado']['failed']} failed")
        elif "aprobado" in r:
            print(f"    -> auditoria: {r['veredicto']}")
            if r.get("violaciones"):
                for v in r["violaciones"]:
                    print(f"       ! {v}")
        elif "analisis" in r:
            print(f"    -> viabilidad: {r['analisis'].get('viabilidad', '?')}")
        print()
    if flujo.get("violaciones"):
        print("  VIOLACIONES DETECTADAS:")
        for v in flujo["violaciones"]:
            print(f"    - {v}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="AI-BUSINESS-OS - Orchestrator CLI")
    parser.add_argument("--objetivo", type=str)
    parser.add_argument("--desde-archivo", action="store_true")
    parser.add_argument("--estado", action="store_true")
    parser.add_argument("--panel", action="store_true")
    parser.add_argument("--dashboard", action="store_true")
    parser.add_argument("--reporte", action="store_true")
    parser.add_argument("--listar-agentes", action="store_true")
    parser.add_argument("--flujo", type=str, help="Ejecuta el flujo completo de agentes")
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
        print(json.dumps(orch.estado(), indent=2, ensure_ascii=False))
        return

    if args.panel:
        print(orch.panel())
        return

    if args.dashboard:
        from src.orchestrator.dashboard import Dashboard
        Dashboard(orch).mostrar()
        return

    if args.reporte:
        from src.orchestrator.reports import Reports
        r = Reports(orch)
        d = r.generar_todos()
        print(f"Reportes generados en: {d}")
        for f in sorted(d.iterdir()):
            print(f"  - {f.name}")
        return

    if args.flujo:
        flujo = orch.ejecutar_flujo(args.flujo)
        _imprimir_flujo(flujo)
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