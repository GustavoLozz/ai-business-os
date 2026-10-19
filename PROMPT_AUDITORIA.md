# MISIÓN: AUDITORÍA TÉCNICA Y CIERRE DE GOBERNANZA — AI-BUSINESS-OS

**Objetivo**
Verificar y corregir exclusivamente los defectos demostrables del motor de gobernanza antes de implementar API REST, MCP o conectores reales.

## REGLAS OBLIGATORIAS
1. Empezá con una inspección de solo lectura.
2. No modifiques archivos en la fase de diagnóstico.
3. No borres datos, informes, memoria, checkpoints ni aprobaciones.
4. No instales dependencias ni hagas llamadas a servicios externos sin autorización.
5. No ejecutes acciones sobre cuentas reales ni expongas credenciales.
6. Conservá el diseño actual. No hagas refactorizaciones generales.
7. Antes de modificar código, presentá los hallazgos, los archivos afectados y el plan mínimo. Esperá autorización humana.
8. No declares una prueba aprobada si no se ejecutó y se verificó su resultado.

## FASE A — DIAGNÓSTICO DE SOLO LECTURA

Inspeccioná:
- src/orchestrator/agent_runner.py
- src/orchestrator/budget.py
- src/orchestrator/approvals.py
- src/orchestrator/permission_system.py
- src/agents/auditor.py
- GOVERNANCE.md
- Los tests relacionados con esos módulos.

Verificá específicamente:
1. Si el presupuesto máximo de costo y tiempo se hace cumplir antes, durante y después de ejecutar una tarea.
2. Si todos los costos de llamadas a modelos se registran correctamente y no se permite superar el presupuesto por falta de contabilización.
3. Si reanudar_flujo() continúa realmente desde el paso pendiente, sin repetir operaciones previas ni saltarse controles.
4. Si las aprobaciones persisten ante reinicios, errores de escritura, archivos JSON inválidos y accesos concurrentes.
5. Si se comprueba la identidad y autorización de quien aprueba.
6. Si el control de permisos funciona de forma predeterminada restrictiva.
7. Si el Auditor puede ser evadido mediante estructuras de datos inesperadas, código ofuscado, rutas alternativas o instrucciones maliciosas.
8. Si el Developer está realmente aislado por controles del sistema operativo y no solo por una bandera o una convención del agente.
9. Si el flujo completo puede alcanzar un estado incorrecto aunque un paso esté bloqueado.
10. Si los tests existentes comprueban comportamiento real o solamente valores declarados.

## FASE B — INFORME
Generá un informe con:
- Hallazgo y severidad.
- Archivo, función y líneas.
- Evidencia reproducible.
- Impacto real.
- Test que falta.
- Corrección mínima propuesta.
- Riesgo de regresión.
- Criterio de aceptación.
Separá los defectos confirmados de las hipótesis que todavía necesitan pruebas.

## FASE C — ESPERA DE AUTORIZACIÓN
Al terminar el informe, detenete. No modifiques el código hasta recibir aprobación explícita.