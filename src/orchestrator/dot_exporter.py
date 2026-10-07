"""Exportador de diagramas Graphviz (.dot).

Genera archivos .dot legibles por IA y humanos que representan:
- Flujos de agentes (recorrido de una tarea por los 7 agentes)
- Estados de tareas individuales
- Relaciones entre componentes del sistema

Los .dot se pueden renderizar a PNG/SVG con Graphviz.
"""
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class DotExporter:
    def __init__(self, directorio=None):
        self.directorio = Path(directorio) if directorio else (
            ROOT / "reports" / datetime.now().strftime("%Y-%m-%d") / "flows"
        )
        self.directorio.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Flujo de agentes
    # ------------------------------------------------------------------
    def exportar_flujo(self, flujo, nombre=None):
        """Genera un .dot desde el resultado de un flujo de agentes."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = nombre or f"flujo_{timestamp}"
        archivo = self.directorio / f"{nombre}.dot"

        objetivo = flujo.get("objetivo", "")
        estado = flujo.get("estado", "desconocido")
        pasos = flujo.get("pasos", [])

        lineas = [
            "digraph flujo {",
            '  rankdir=TB;',
            '  node [shape=box, style="rounded,filled", fontname="Arial"];',
            '  edge [fontname="Arial", fontsize=10];',
            '',
            f'  label="Flujo: {self._escapar(objetivo)[:60]}\\nEstado: {estado}";',
            '  labelloc=t;',
            '',
        ]

        # Nodo de inicio
        lineas.append(f'  INICIO [label="INICIO\\n{self._escapar(objetivo)[:40]}", fillcolor="#C8E6C9"];')

        # Nodos de cada agente
        for i, paso in enumerate(pasos):
            agente = paso.get("agente", f"Agente{i}")
            resultado = paso.get("resultado", {})
            descripcion = self._describir_resultado(agente, resultado)
            color = self._color_agente(agente)
            node_id = f"N{i}"
            lineas.append(
                f'  {node_id} [label="{agente}\\n{self._escapar(descripcion)}", fillcolor="{color}"];'
            )

        # Nodo final
        if estado == "completado":
            lineas.append('  FIN [label="COMPLETADO", fillcolor="#66BB6A"];')
        elif estado == "bloqueado_por_auditor":
            lineas.append('  FIN [label="BLOQUEADO", fillcolor="#EF5350"];')
        else:
            lineas.append(f'  FIN [label="{estado.upper()}", fillcolor="#FFD54F"];')

        # Conexiones
        if pasos:
            lineas.append('  INICIO -> N0;')
            for i in range(len(pasos) - 1):
                lineas.append(f'  N{i} -> N{i+1};')
            lineas.append(f'  N{len(pasos)-1} -> FIN;')
        else:
            lineas.append('  INICIO -> FIN;')

        lineas.append("}")

        contenido = "\n".join(lineas)
        archivo.write_text(contenido, encoding="utf-8")

        return {
            "archivo": str(archivo),
            "nombre": archivo.name,
            "nodos": len(pasos) + 2,
        }

    # ------------------------------------------------------------------
    # Tarea individual
    # ------------------------------------------------------------------
    def exportar_tarea(self, tarea, nombre=None):
        """Genera un .dot desde una tarea del TaskManager."""
        task_id = tarea.get("id", "TASK")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = nombre or f"tarea_{task_id}_{timestamp}"
        archivo = self.directorio / f"{nombre}.dot"

        descripcion = tarea.get("descripcion", "")
        agente = tarea.get("agente", "sin_asignar")
        estado = tarea.get("estado", "pendiente")
        intentos = tarea.get("intentos", 0)
        historial = tarea.get("historial", [])

        color_estado = self._color_estado(estado)

        lineas = [
            "digraph tarea {",
            '  rankdir=LR;',
            '  node [shape=box, style="rounded,filled", fontname="Arial"];',
            '',
            f'  label="Tarea {task_id}\\n{self._escapar(descripcion)[:60]}";',
            '  labelloc=t;',
            '',
            f'  TAREA [label="{task_id}\\nAgente: {agente}\\nEstado: {estado}\\nIntentos: {intentos}", fillcolor="{color_estado}"];',
            '',
        ]

        # Estados visitados
        for i, ev in enumerate(historial[:10]):
            evt = ev.get("evento", "?")
            ts = ev.get("fecha", "")[:16]
            nuevo = ev.get("nuevo", "")
            label = f"{evt}\\n{ts}"
            if nuevo:
                label += f"\\n-> {nuevo}"
            lineas.append(f'  H{i} [label="{label}", fillcolor="#E3F2FD"];')

        # Conexiones
        for i in range(len(historial[:10]) - 1):
            lineas.append(f'  H{i} -> H{i+1};')
        if historial:
            lineas.append('  TAREA -> H0;')

        lineas.append("}")

        contenido = "\n".join(lineas)
        archivo.write_text(contenido, encoding="utf-8")

        return {
            "archivo": str(archivo),
            "nombre": archivo.name,
        }

    # ------------------------------------------------------------------
    # Sistema completo
    # ------------------------------------------------------------------
    def exportar_sistema(self, orchestrator, nombre=None):
        """Genera un .dot con el estado global del sistema."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre = nombre or f"sistema_{timestamp}"
        archivo = self.directorio / f"{nombre}.dot"

        e = orchestrator.estado()

        lineas = [
            "digraph sistema {",
            '  rankdir=TB;',
            '  node [shape=box, style="rounded,filled", fontname="Arial"];',
            '',
            '  label="AI-BUSINESS-OS - Estado del Sistema";',
            '  labelloc=t;',
            '',
            # Nodo raiz
            f'  ORQ [label="ORCHESTRATOR\\nAgentes: {e["agentes"]}\\nTareas: {e["tareas"]["total"]}\\nMemorias: {e["memoria"]["total"]}", fillcolor="#4FC3F7"];',
            '',
            # Agentes
        ]

        for i, a in enumerate(orchestrator.registry.listar()):
            nombre_a = a["nombre"]
            rol = a["rol"][:30]
            color = "#C8E6C9" if a["estado"] == "activo" else "#FFF9C4"
            lineas.append(f'  A{i} [label="{nombre_a}\\n{rol}", fillcolor="{color}"];')
            lineas.append(f'  ORQ -> A{i};')

        lineas.append("}")

        contenido = "\n".join(lineas)
        archivo.write_text(contenido, encoding="utf-8")

        return {
            "archivo": str(archivo),
            "nombre": archivo.name,
            "agentes": e["agentes"],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _escapar(self, texto):
        return str(texto).replace('"', '\\"').replace("\n", "\\n")

    def _describir_resultado(self, agente, resultado):
        if not isinstance(resultado, dict):
            return "..."
        if "subtareas" in resultado:
            return f"{len(resultado['subtareas'])} subtareas"
        if "arquitectura" in resultado:
            comp = resultado["arquitectura"].get("componentes", [])
            return f"{len(comp)} componentes"
        if "propuesta" in resultado:
            archivos = resultado["propuesta"].get("archivos", [])
            return f"{len(archivos)} archivos"
        if "experimento" in resultado:
            algo = resultado["experimento"].get("algoritmo", "")[:20]
            return algo
        if "resultado" in resultado and "passed" in resultado["resultado"]:
            r = resultado["resultado"]
            return f"{r['passed']} pass / {r['failed']} fail"
        if "aprobado" in resultado:
            return resultado.get("veredicto", "?")
        if "analisis" in resultado:
            return f"viabilidad: {resultado['analisis'].get('viabilidad', '?')}"
        return "OK"

    def _color_agente(self, agente):
        colores = {
            "Director":   "#BBDEFB",
            "Arquitecto": "#D1C4E9",
            "Developer":  "#C8E6C9",
            "Quantum_RD": "#B2EBF2",
            "Tester":     "#FFE0B2",
            "Auditor":    "#FFCDD2",
            "Business":   "#F8BBD0",
        }
        return colores.get(agente, "#EEEEEE")

    def _color_estado(self, estado):
        colores = {
            "pendiente":            "#FFF9C4",
            "asignada":             "#BBDEFB",
            "en_proceso":           "#B3E5FC",
            "completada":           "#C8E6C9",
            "fallida":              "#FFCDD2",
            "requiere_aprobacion":  "#FFE0B2",
            "aprobada":             "#A5D6A7",
            "rechazada":            "#EF9A9A",
        }
        return colores.get(estado, "#EEEEEE")