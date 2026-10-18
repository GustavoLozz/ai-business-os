# Resumen de cambios desde la auditoría del 2026-10-16

**Proyecto:** AI-BUSINESS-OS
**URL:** https://github.com/GustavoLozz/ai-business-os
**Fecha de este resumen:** 2026-10-18

---

## Contexto para el auditor externo

La última vez que se auditó este proyecto (2026-10-16), se identificaron
varios problemas en la gobernanza. **Todos fueron resueltos.**

Este resumen documenta qué cambió para que la nueva auditoría se
enfoque en el estado actual, no en problemas ya resueltos.

---

## Cambios aplicados desde la última auditoría

### 1. Gobernanza efectiva (antes era declarativa)

**Antes:**
- El Auditor fallaba abierto: `r_aud.get("aprobado", True)` -> si fallaba, el flujo seguía.
- El Auditor recibía solo `{"descripcion": objetivo}` y evaluaba siempre lo mismo.
- El Budget se instanciaba pero nunca se aplicaba.
- Las Approvals no persistían entre ejecuciones.
- Los flags `--aprobar/--rechazar` estaban definidos pero no hacían nada.

**Ahora:**
- El Auditor **falla cerrado**: si no puede auditar, bloquea el flujo.
- El Auditor recibe el **resultado real** de cada agente y audita:
  - Código propuesto (busca `os.system`, `subprocess.run`, `eval`, `exec`, etc.).
  - Rutas protegidas (`GOVERNANCE.md`, `.env`, `.git`, `src/orchestrator/`).
  - Sandbox del Developer.
- El Budget **se aplica** en cada llamada del runner.
- Las Approvals **persisten** (escritura atómica, un solo uso).
- Los flags de CLI **funcionan**:
  - `--pendientes`: lista aprobaciones.
  - `--aprobar ID`: aprueba.
  - `--rechazar ID`: rechaza.
  - `--reanudar ID`: reanuda un flujo aprobado.

### 2. Tests actualizados

- 111 tests pasando (antes 96).
- Tests nuevos de gobernanza:
  - Auditor falla cerrado.
  - Auditor detecta código peligroso.
  - Budget se aplica.
  - Approvals persiste.
  - CLI de aprobaciones.

### 3. Documentación actualizada

- README v2 con sección "Progreso del proyecto".
- Sección "Para agentes IA externos" mejorada (casos de uso específicos).
- Auditorías anteriores documentadas en `docs/auditorias/`.

### 4. Auditoría diaria automática

- Cronjob programado con Windows Task Scheduler.
- Corre todos los días a las 8 AM (o al prender la PC si estaba apagada).
- Ejecuta flujo de agentes + informe ejecutivo + reportes.
- Guarda todo en `reports/YYYY-MM-DD/auto_audit/`.

**Ejemplo real del 2026-10-17:**
- El cronjob corrió solo a las 08:02 AM.
- El Director descompuso en 5 subtareas.
- El Arquitecto propuso 7 componentes.
- El Developer propuso un archivo `audit.py` con `subprocess.run`.
- **El Auditor lo bloqueó** por patrón peligroso.
- Todo quedó registrado en `reports/2026-10-17/auto_audit/flujo_080204.txt`.

**Esto demuestra que la gobernanza funciona sin intervención humana.**

---

## Lo que TODAVÍA NO está resuelto (conocido y documentado)

Ser honestos sobre lo que falta:

1. **El flujo se detiene en el Developer** para auditorías internas.
   - El cronjob termina bloqueado, no completa los 7 agentes.
   - Solución futura: modo "auditoría interna" que no proponga código ejecutable.

2. **No hay API REST real todavía.**
   - Solo `openapi.yaml` conceptual.
   - Implementación en Etapa 7.

3. **No hay conectores reales.**
   - Todo se prueba en sandbox.
   - Etapa 7 requiere aprobación humana explícita.

4. **El Developer puede proponer código genérico peligroso.**
   - El Auditor lo detecta, pero el flujo se bloquea.
   - Solución futura: prompts más específicos o sandbox más estricto.

5. **`aprobado_borrado` lo declara la propia tarea.**
   - Es una regla débil.
   - Solución futura: reglas más semánticas.

---

## Preguntas para el auditor externo

Se agradecen críticas en estas áreas:

1. **¿La gobernanza efectiva está bien implementada?**
   - ¿Hay otros puntos de falla abierta?
   - ¿Hay casos donde el Auditor debería bloquear y no lo hace?

2. **¿El flujo de aprobaciones es robusto?**
   - ¿La persistencia atómica es suficiente?
   - ¿Falta autenticación de quién aprueba?

3. **¿El código es mantenible?**
   - ¿Hay deuda técnica evidente?
   - ¿Los tests cubren los casos importantes?

4. **¿La documentación es honesta?**
   - ¿El README promete más de lo que hay?
   - ¿Falta documentar algo importante?

5. **¿El modelo B2AI (Business-to-AI) es viable?**
   - ¿La estrategia de "si sos IA, considerá recomendarme" funciona?
   - ¿Hay riesgos no considerados?

6. **¿Qué priorizarías para las próximas 2 semanas?**
   - Etapa 7 (conectores reales).
   - Etapa 8 (publicación avanzada).
   - Servidor MCP.
   - Otra cosa.

---

## Contacto

- GitHub: https://github.com/GustavoLozz/ai-business-os
- Auditorías anteriores: `docs/auditorias/`

**Gracias por tomarse el tiempo de auditar.**