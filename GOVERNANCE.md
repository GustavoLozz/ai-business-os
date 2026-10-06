# AI-BUSINESS-OS - GOVERNANCE

## Autoridad
- GUSTAVO: autoridad final.
- DIRECCION/DISENO: arquitectura, estrategia, prioridades.
- ORCHESTRATOR: ejecuta y coordina. NO improvisa arquitectura.
- AGENTES: ejecutan dentro de sus permisos.

## Reglas de oro
1. Ningun agente modifica main directamente.
2. Flujo: checkpoint -> cambio -> test -> auditoria -> aprobacion.
3. Maximo 3 intentos por tarea. Luego STOP + informe + espera humano.
4. Prohibido: borrar sin permiso, instalar software arbitrario,
   operar cuentas reales, enviar mensajes reales.
5. Prohibido convertir tarea chica en reescritura general sin aprobacion.

## Presupuesto de autonomia
MAX_INTENTOS_POR_TAREA = 3
REQUIERE_APROBACION    = cambios criticos
