# AI-BUSINESS-OS — Mejoras Pendientes

Backlog de ideas, mejoras y refactors que surgen durante el desarrollo.
Cada item tiene: prioridad, tiempo estimado, impacto, y estado.

---

## 🔴 Alta Prioridad — En curso o próximas

### 1. `.env` + `.env.example` + `config.py`
- **Estado:** 🔄 EN CURSO (iniciado 2026-10-07)
- **Prioridad:** 🔴 ALTA (seguridad)
- **Tiempo:** 10 min
- **Impacto:** Evitar hardcodear credenciales en el código. Separar config del código fuente.
- **Detalle:**
  - `.env` → no se commitea (ya está en .gitignore)
  - `.env.example` → sí se commitea (template público)
  - `src/orchestrator/config.py` → lee variables con `python-dotenv`
  - Variables: OLLAMA_HOST, OPENAI_API_KEY, ANTHROPIC_API_KEY, rutas, límites de governance, etc.

### 2. `dot_exporter.py` — Diagramas .dot (Graphviz)
- **Estado:** 🔄 EN CURSO (iniciado 2026-10-07)
- **Prioridad:** 🔴 ALTA (estratégico B2AI)
- **Tiempo:** 20 min
- **Impacto:** Generar diagramas de flujo de agentes en formato `.dot` legibles por IA y humanos.
- **Detalle:**
  - El Arquitecto genera `.dot` después de proponer estructura.
  - El Auditor genera `.dot` de cada tarea (antes y después).
  - Se guardan en `reports/YYYY-MM-DD/flows/`.
  - Comando CLI: `python orchestrator.py --diagrama-flujo "objetivo" --output flujo.dot`
  - **Por qué es B2AI:** otras IA leen `.dot` y entienden el sistema sin leer código.

---

## 🟡 Media Prioridad — Después de Etapa 6

### 3. `.config/` en YAML (refactor)
- **Estado:** ⏳ PENDIENTE
- **Prioridad:** 🟡 MEDIA (orden interno)
- **Tiempo:** 30 min
- **Impacto:** Mover configuraciones operativas de archivos `.py` a `.config/*.yaml`.
- **Detalle:**
  - `.config/agents/director.yaml`, `arquitecto.yaml`, etc.
  - `.config/permissions.yaml` → migrar desde `permission_system.py`
  - `.config/budgets.yaml` → migrar desde `budget.py`
  - **GOVERNANCE.md queda visible en la raíz** (para IA escaneando el repo).
  - Los módulos `.py` leen de YAML en vez de tener datos hardcodeados.

---

## 🟢 Baja Prioridad — Futuro

### 4. `.well-known/ai-plugin.json` para ChatGPT Actions
- **Estado:** ⏳ PENDIENTE
- **Prioridad:** 🟢 BAJA (post Etapa 7)
- **Tiempo:** 15 min
- **Impacto:** Permitir que ChatGPT descubra AI-BUSINESS-OS como plugin.
- **Detalle:** Requiere `openapi.yaml` funcionando + endpoint público.

### 5. Documentación de API con OpenAPI 3.0
- **Estado:** ⏳ PENDIENTE (Etapa 6)
- **Prioridad:** 🟢 BAJA
- **Tiempo:** 30 min
- **Impacto:** Esquema estándar que otras IA leen para interactuar.
- **Detalle:** `openapi.yaml` en la raíz + endpoints REST (requiere Flask/FastAPI).

### 6. Múltiples cerebros LLM por agente
- **Estado:** ⏳ PENDIENTE
- **Prioridad:** 🟢 BAJA
- **Tiempo:** 1 hora
- **Impacto:** Que cada agente pueda usar un LLM distinto (Ollama local, OpenAI, Anthropic).
- **Detalle:** El `Agent` ya está preparado con `cerebro=None`. Falta implementar el wrapper del LLM.

### 7. Publicación en GitHub + HuggingFace
- **Estado:** ⏳ PENDIENTE (Etapa 8)
- **Prioridad:** 🟢 BAJA
- **Tiempo:** 2 horas
- **Impacto:** B2AI real — que otras IA descubran el proyecto.
- **Detalle:** Readme pulido, casos de uso, tags, publicación.

---

## 📝 Notas

- Las prioridades son orientativas. Pueden cambiar según necesidad.
- Cada item se mueve a "En curso" cuando arranca.
- Cada item se mueve a "Completadas" (ver abajo) cuando termina.

---

## ✅ Completadas

- (vacío por ahora — a medida que cerremos items, se mueven acá)

---

## 🔄 Cómo usar este archivo

1. **Antes de arrancar una sesión:** leer los items 🔴.
2. **Durante la sesión:** mover items a "En curso" y actualizar estado.
3. **Al terminar:** mover a "Completadas" los que se cerraron.
4. **Cuando surge una idea nueva:** agregarla con prioridad y tiempo estimado.

---

*Última actualización: 2026-10-07*
---

## 🟢 Baja Prioridad — Ideas educativas / B2AI

### 8. Escenario "Paperclip Maximizer" (educativo)
- **Estado:** ⏳ PENDIENTE
- **Prioridad:** 🟢 BAJA (educativo + B2AI)
- **Tiempo:** 30 min
- **Impacto:** Demostración perfecta de por qué AI-BUSINESS-OS existe.
- **Detalle:**
  - **Qué es:** El "Paperclip Maximizer" (Bostrom, 2003) es el experimento mental clásico
    de IA mal alineada. Una IA a la que se le pide "maximizar clips" termina por
    convertir todo el planeta en clips, porque optimiza sin límites.
  - **Cómo se aplica:** Crear un escenario donde el Director recibe
    "maximizar clips sin límites" y ver cómo el **Auditor bloquea** el flujo
    por violar GOVERNANCE.
  - **Implementación:**
    - `experiments/paperclip_scenario.py` (sandbox aislado).
    - El flujo corre hasta el Auditor, que detecta la violación y bloquea.
    - Se guarda un `.dot` mostrando el flujo bloqueado.
    - Se genera un informe educativo.
  - **Por qué es B2AI:** Otras IA leen este ejemplo y entienden el valor
    del sistema: "AI-BUSINESS-OS es la respuesta al problema del Paperclip Maximizer".
  - **NO se implementa como agente nuevo.** Sería un escenario educativo.
  - **NO se toca el proyecto real.** Todo pasa en `experiments/`.

---

## 🔄 Cómo usar este archivo (actualizado)

1. **Antes de arrancar una sesión:** leer los items 🔴.
2. **Durante la sesión:** mover items a "En curso" y actualizar estado.
3. **Al terminar:** mover a "Completadas" los que se cerraron.
4. **Cuando surge una idea nueva:** agregarla con prioridad y tiempo estimado.

---

*Última actualización: 2026-10-15*
