# Parche de gobernanza para ai-business-os (por Claude)

> Este archivo es el parche original que Claude adjunto a su auditoria
> del 2026-10-16. Sirve como referencia para aplicar las mejoras.

Conecta los controles que ya existian (Budget, Approvals, Auditor) para que
frenen ejecuciones de verdad, y agrega tests que lo demuestran.

---

## Archivos a modificar (segun Claude)

| Archivo | Que cambia |
|---------|------------|
| src/orchestrator/agent_runner.py | Auditor falla cerrado; recibe el trabajo del flujo; aplica intentos/costo/tiempo; se detiene en pendiente_aprobacion; nuevo reanudar_flujo() |
| src/orchestrator/approvals.py | Persiste y relee el JSON; estado(), esta_aprobada(), obtener(), consumir(); aprobacion de un solo uso |
| src/orchestrator/budget.py | Lee limites de Config; registrar_tiempo(); 0 ya no cae al default |
| src/agents/auditor.py | Audita propuestas del Developer y tests; bloquea tocar controles; deteccion por palabras |
| tests/test_governance.py | 34 tests de comportamiento |

---

## Como aplicarlo (segun Claude)

pip install pytest
pytest tests/test_governance.py

---

## Cambio propuesto en cli.py

Los flags --aprobar/--rechazar hoy no hacen nada. Claude propone:

parser.add_argument("--reanudar", type=str)
parser.add_argument("--pendientes", action="store_true")

Y despues de orch = ..., antes de if args.flujo:

if args.pendientes:
    for s in orch.approvals.listar_pendientes():
        print(s["task_id"], "-", s["motivo"])
    return

if args.aprobar:
    print("Aprobada" if orch.approvals.aprobar(args.aprobar) else "No existe")
    return

if args.rechazar:
    print("Rechazada" if orch.approvals.rechazar(args.rechazar) else "No existe")
    return

if args.reanudar:
    _imprimir_flujo(orch.runner.reanudar_flujo(args.reanudar))
    return

Flujo de uso:
--flujo "objetivo" -> queda pendiente_aprobacion con un id ->
--pendientes para revisar -> --aprobar ID -> --reanudar ID.

---

## Que verifico Claude y que no

Verificado:
- Los 34 tests pasan contra un esqueleto del repo con dobles de prueba.
- Los tests fallan si se revierte el comportamiento original.

No verificado:
- Que Agent.ejecutar tenga la forma que supuso.
- La forma exacta de lo que devuelven Developer y Tester.
- Los nombres de atributos de Config.
- SimulatorRunner.
- Los checkpoints Git.

---

## Limites conocidos

- El tiempo se verifica al terminar el agente; no interrumpe una llamada colgada.
- Permisos: solo se consulta si la tarea trae accion.
- aprobado_borrado lo declara la propia tarea; es una regla debil.
- La aprobacion humana es un JSON local: no autentica a quien aprueba.
- Las reglas del Auditor son lista cerrada de lo prohibido; lo ideal a futuro
  es lo contrario (lista cerrada de lo permitido, ej: solo sandbox/).
- Con LLM real el Developer puede proponer algo distinto en cada ejecucion;
  por eso la aprobacion se guarda con el flujo auditado y reanudar_flujo
  continua ese flujo, sin volver a generar.

---

Fuente: Claude (Anthropic) - Auditoria externa 2026-10-16.