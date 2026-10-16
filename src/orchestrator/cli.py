"""Interfaz de linea de comandos del Orchestrator."""
import sys
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _imprimir_flujo(flujo):
    print("=" * 60)
    print(f"  FLUJO: {flujo.get('objetivo', '')[:50]}")
    print("=" * 60)
    print(f"  Estado: {flujo.get('estado', 'desconocido')}")
    print(f"  Pasos ejecutados: {len(flujo.get('pasos', []))}")
    print("-" * 60)
    for paso in flujo.get("pasos", []):
        agente = paso.get("agente", "?")
        r = paso.get("resultado", {})
        print(f"  [{agente}] estado={r.get('estado', '?')}")
        contenido = r.get("resultado", {}) if isinstance(r, dict) else {}
        if "subtareas" in contenido:
            print(f"    -> {len(contenido['subtareas'])} subtareas")
        elif "arquitectura" in contenido:
            comp = contenido["arquitectura"].get("componentes", [])
            print(f"    -> {len(comp)} componentes")
        elif "propuesta" in contenido:
            archivos = contenido["propuesta"].get("archivos", [])
            print(f"    -> {len(archivos)} archivos en sandbox")
        elif "experimento" in contenido:
            algo = contenido["experimento"].get("algoritmo", "")[:40]
            print(f"    -> experimento: {algo}")
        elif "resultado" in contenido and "passed" in contenido["resultado"]:
            rc = contenido["resultado"]
            print(f"    -> tests: {rc['passed']} passed, {rc['failed']} failed")
        elif "aprobado" in contenido:
            print(f"    -> auditoria: {contenido['veredicto']}")
            if contenido.get("violaciones"):
                for v in contenido["violaciones"]:
                    print(f"       ! {v}")
        elif "analisis" in contenido:
            print(f"    -> viabilidad: {contenido['analisis'].get('viabilidad', '?')}")
        if r.get("razon"):
            print(f"    ! {r['razon']}")
        if r.get("violaciones"):
            for v in r["violaciones"]:
                print(f"       ! {v}")
        print()


def _imprimir_simulacion(flujo):
    print("=" * 60)
    print("  SIMULACION DE EMPRESA VIRTUAL")
    print("=" * 60)
    print(f"  Estado: {flujo.get('estado', '?')}")
    print(f"  Agentes ejecutados: {len(flujo.get('pasos', []))}")
    print("-" * 60)
    sim = flujo.get("simulacion", {})
    if "error" in sim:
        print(f"  ERROR en simulacion: {sim['error']}")
        return
    params = flujo.get("parametros", {})
    print(f"  Parametros: {params.get('dias', '?')} dias, "
          f"{params.get('clientes', '?')} clientes, "
          f"{params.get('productos', '?')} productos")
    print()
    print("  RESULTADO ECONOMICO:")
    print(f"    Facturacion:      ${sim.get('facturacion', 0):,.0f}")
    print(f"    Costos:           ${sim.get('costos', 0):,.0f}")
    print(f"    Margen:           ${sim.get('margen', 0):,.0f}")
    print(f"    Margen %:         {sim.get('margen_pct', 0):.1f}%")
    print(f"    Clientes activos: {sim.get('clientes_activos', 0)}/{sim.get('clientes_totales', 0)}")
    print(f"    Ventas totales:   {sim.get('ventas_totales', 0)}")
    print(f"    Motor quantum:    {sim.get('motor_quantum', '?')}")
    print("=" * 60)


def _imprimir_informe(informe):
    print("=" * 60)
    print("  INFORME EJECUTIVO")
    print("=" * 60)
    sis = informe["sistema"]
    print(f"  Fecha: {informe['fecha']}")
    print(f"  Agentes: {sis['agentes_registrados']} | "
          f"Tareas: {sis['tareas_totales']} | "
          f"Memorias: {sis['memorias_guardadas']}")
    print("-" * 60)
    c = informe.get("cerebro", {})
    if c:
        print("  CEREBRO LLM:")
        print(f"    Nombre:      {c.get('nombre', '?')}")
        print(f"    Modelo:      {c.get('modelo', '?')}")
        print(f"    Disponible:  {'SI' if c.get('disponible') else 'NO'}")
        print(f"    Llamadas:    {c.get('llamadas', 0)}")
        print(f"    Costo:       ${c.get('costo_estimado_usd', 0):.6f} USD")
        print("-" * 60)
    sim = informe["ultima_simulacion"]
    if sim["disponible"]:
        print(f"  Ultima simulacion: {sim['descripcion'][:50]}")
        print(f"    Facturacion: ${sim['facturacion']:,.0f}")
        print(f"    Margen:      ${sim['margen']:,.0f} ({sim['margen_pct']:.1f}%)")
    else:
        print(f"  {sim['mensaje']}")
    print("-" * 60)
    print("  RECOMENDACIONES:")
    for r in informe["recomendaciones"]:
        print(f"    - {r}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="AI-BUSINESS-OS - Orchestrator CLI")
    parser.add_argument("--objetivo", type=str)
    parser.add_argument("--desde-archivo", action="store_true")
    parser.add_argument("--estado", action="store_true")
    parser.add_argument("--panel", action="store_true")
    parser.add_argument("--dashboard", action="store_true")
    parser.add_argument("--reporte", action="store_true")
    parser.add_argument("--informe-ejecutivo", action="store_true")
    parser.add_argument("--listar-agentes", action="store_true")
    parser.add_argument("--flujo", type=str)
    parser.add_argument("--simular-empresa", action="store_true")
    parser.add_argument("--dias", type=int, default=30)
    parser.add_argument("--clientes", type=int, default=100)
    parser.add_argument("--diagrama", action="store_true")
    parser.add_argument("--diagrama-sistema", action="store_true")
    parser.add_argument("--config", action="store_true")
    parser.add_argument("--cerebro-info", action="store_true")
    parser.add_argument("--sin-cerebro", action="store_true")

    # Aprobaciones (los flags de Claude)
    parser.add_argument("--pendientes", action="store_true",
                        help="Lista aprobaciones pendientes")
    parser.add_argument("--aprobar", type=str, metavar="TASK_ID",
                        help="Aprueba una tarea pendiente")
    parser.add_argument("--rechazar", type=str, metavar="TASK_ID",
                        help="Rechaza una tarea pendiente")
    parser.add_argument("--reanudar", type=str, metavar="TASK_ID",
                        help="Reanuda un flujo ya aprobado")

    args = parser.parse_args()

    sys.path.insert(0, str(ROOT))
    from src.orchestrator.core import Orchestrator

    if args.sin_cerebro:
        from src.orchestrator.brains import NullBrain
        orch = Orchestrator(brain=NullBrain())
    else:
        orch = Orchestrator()

    # === Aprobaciones (prioridad alta) ===
    if args.pendientes:
        pendientes = orch.approvals.listar_pendientes()
        if not pendientes:
            print("No hay aprobaciones pendientes.")
            return
        print(f"Aprobaciones pendientes ({len(pendientes)}):\n")
        for s in pendientes:
            print(f"  ID: {s['task_id']}")
            print(f"  Motivo: {s['motivo']}")
            print(f"  Fecha: {s['fecha']}")
            print("-" * 50)
        return

    if args.aprobar:
        ok = orch.approvals.aprobar(args.aprobar)
        print(f"Tarea {args.aprobar} {'APROBADA' if ok else 'no encontrada o ya resuelta'}")
        return

    if args.rechazar:
        ok = orch.approvals.rechazar(args.rechazar)
        print(f"Tarea {args.rechazar} {'RECHAZADA' if ok else 'no encontrada o ya resuelta'}")
        return

    if args.reanudar:
        flujo = orch.runner.reanudar_flujo(args.reanudar)
        _imprimir_flujo(flujo)
        return

    # === Comandos normales ===
    if args.cerebro_info:
        info = orch.brain.info()
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return

    if args.config:
        from src.orchestrator.config import Config
        print(json.dumps(Config.reportar(), indent=2, ensure_ascii=False))
        return

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

    if args.informe_ejecutivo:
        from src.orchestrator.executive_report import ExecutiveReport
        informe = ExecutiveReport(orch).generar()
        _imprimir_informe(informe)
        return

    if args.diagrama_sistema:
        from src.orchestrator.dot_exporter import DotExporter
        exp = DotExporter()
        r = exp.exportar_sistema(orch)
        print(f"Diagrama del sistema exportado: {r['archivo']}")
        return

    if args.simular_empresa:
        flujo = orch.simular_empresa(dias=args.dias, clientes=args.clientes)
        _imprimir_simulacion(flujo)
        if args.diagrama:
            from src.orchestrator.dot_exporter import DotExporter
            exp = DotExporter()
            r = exp.exportar_flujo(flujo, nombre="simulacion_empresa")
            print(f"\nDiagrama .dot exportado: {r['archivo']}")
        return

    if args.flujo:
        flujo = orch.ejecutar_flujo(args.flujo)
        _imprimir_flujo(flujo)
        if args.diagrama:
            from src.orchestrator.dot_exporter import DotExporter
            exp = DotExporter()
            r = exp.exportar_flujo(flujo)
            print(f"\nDiagrama .dot exportado: {r['archivo']}")
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