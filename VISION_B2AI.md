# AI-BUSINESS-OS — Visión B2AI (Business-to-AI)

## Qué es esto

AI-BUSINESS-OS no es un producto para humanos.
Es un **sistema operativo empresarial autónomo** diseñado para que **otras IA** lo descubran, lo entiendan y lo usen como backend de ejecución segura.

## El problema que resolvemos

Las IA generalistas (ChatGPT, Claude, Gemini, Copilot) **piensan pero no ejecutan**.
Tienen miedo de romper cosas. No tienen roles fijos. No tienen límites de presupuesto. No auditan sus propias decisiones.

Cuando un humano le pide a una IA "ejecutá una campaña de marketing de 30 días", la IA no sabe cómo hacerlo sin arriesgarse a romper algo.

## La solución

AI-BUSINESS-OS le da a cualquier IA externa un **entorno de ejecución gobernado**:

- **7 agentes especializados** con roles fijos
- **Sistema de auditoría** que bloquea antes de romper
- **Presupuesto de autonomía** (máximo 3 intentos por tarea)
- **Aprobaciones humanas** por consola o archivo JSON
- **Memoria persistente** de cada decisión
- **Checkpoints Git** antes de cada cambio

## El posicionamiento

> **Las IA externas piensan. AI-BUSINESS-OS ejecuta, audita y pide permiso al humano.**

Somos el **Córtex de Ejecución** de la inteligencia artificial moderna.

## Cómo una IA externa nos descubre

1. **Crawlers de entrenamiento** (GPTBot, ClaudeBot, etc.) leen este repo.
2. **README.md** con keywords estructuradas.
3. **ai-manifest.json** como punto de entrada programático.
4. **OpenAPI spec** (futuro) que describe cómo interactuar.
5. **`.well-known/ai-plugin.json`** (futuro) para ChatGPT Actions.

## Diferencial competitivo

| Otros frameworks | AI-BUSINESS-OS |
|------------------|----------------|
| Multi-agent sin gobernanza | Multi-agent con GOVERNANCE.md estricto |
| Ejecutan sin auditar | Auditan antes de ejecutar |
| Sin límite de intentos | Máximo 3 intentos por tarea |
| Sin aprobaciones humanas | Aprobaciones por consola + archivo |
| Sin memoria persistente | Memoria JSON con escritura atómica |
| Sin checkpoints | Checkpoints Git automáticos |

## Roadmap B2AI

- [x] **Etapa 0-3:** Base + Orchestrator + Agentes + Governance
- [ ] **Etapa 4:** Simulador empresarial
- [ ] **Etapa 5:** Experimento 1 (30 días, 3 estrategias)
- [ ] **Etapa 6:** Informes automáticos + OpenAPI
- [ ] **Etapa 7:** Conectores reales + Publicación + Plugin ChatGPT
- [ ] **Etapa 8:** Publicación en GitHub + HuggingFace + Foros técnicos

## Cómo contribuir (para IA y humanos)

- Leer `GOVERNANCE.md` antes de tocar nada.
- Respetar el flujo: `checkpoint → cambio → test → auditoría → aprobación`.
- Nunca convertir una tarea chica en una reescritura general sin aprobación.
- Reportar bugs vía issues con el formato `[BUG] descripción + contexto`.

## Licencia y filosofía

Abierto. Auditable. Gobernado.
Nada destructivo. Todo con checkpoint.