"""Generador de informe ejecutivo para el CEO."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _to_float(valor, default=0.0):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return default


class ExecutiveReport:
    def __init__(self, orchestrator):
        self.orch = orchestrator
        self.hoy = datetime.now().strftime("%Y-%m-%d")
        self.dir = ROOT / "reports" / self.hoy
        self.dir.mkdir(parents=True, exist_ok=True)

    def generar(self):
        estado = self.orch.estado()
        simulaciones = self.orch.memory.buscar("simulacion_completa")
        ultima_sim = simulaciones[-1] if simulaciones else None

        informe = {
            "fecha": self.hoy,
            "timestamp": datetime.now().isoformat(),
            "sistema": {
                "agentes_registrados": estado["agentes"],
                "tareas_totales": estado["tareas"]["total"],
                "memorias_guardadas": estado["memoria"]["total"],
                "pendientes_aprobacion": estado["pendientes_aprobacion"],
                "estado_general": "OK",
            },
            "cerebro": self._info_cerebro(),
            "agentes": self._estado_agentes(),
            "ultima_simulacion": self._resumen_simulacion(ultima_sim),
            "recomendaciones": self._recomendaciones(ultima_sim),
            "proximos_pasos": self._proximos_pasos(),
        }

        self._guardar_json(informe)
        self._guardar_markdown(informe)
        return informe

    def _info_cerebro(self):
        """Info del cerebro LLM activo."""
        try:
            info = self.orch.brain.info()
            costo = 0.0
            if hasattr(self.orch.brain, "costo_estimado_usd"):
                costo = self.orch.brain.costo_estimado_usd()
            return {
                "nombre": info.get("nombre", "?"),
                "modelo": info.get("modelo", "?"),
                "tipo": info.get("tipo", "?"),
                "disponible": info.get("disponible", False),
                "llamadas": info.get("llamadas", 0),
                "errores": info.get("errores", 0),
                "tokens_entrada": info.get("tokens_entrada", 0),
                "tokens_salida": info.get("tokens_salida", 0),
                "costo_estimado_usd": costo,
            }
        except Exception as e:
            return {
                "nombre": "desconocido",
                "modelo": "desconocido",
                "tipo": "error",
                "disponible": False,
                "error": str(e),
            }

    def _estado_agentes(self):
        agentes = []
        for a in self.orch.registry.listar():
            agentes.append({
                "nombre": a["nombre"],
                "rol": a["rol"],
                "estado": a["estado"],
                "icono": "[OK]" if a["estado"] == "activo" else "[--]",
            })
        return agentes

    def _resumen_simulacion(self, sim):
        if not sim:
            return {
                "disponible": False,
                "mensaje": "Aun no se ejecuto ninguna simulacion completa.",
                "descripcion": "",
                "facturacion": 0,
                "margen": 0,
                "margen_pct": 0,
                "fecha": "?",
            }
        return {
            "disponible": True,
            "descripcion": sim.get("contenido", "simulacion"),
            "facturacion": _to_float(sim.get("facturacion", 0)),
            "margen": _to_float(sim.get("margen", 0)),
            "margen_pct": _to_float(sim.get("margen_pct", 0)),
            "fecha": sim.get("timestamp", "?"),
        }

    def _recomendaciones(self, sim):
        recomendaciones = []
        if sim:
            margen_pct = _to_float(sim.get("margen_pct", 0))
            if margen_pct > 60:
                recomendaciones.append(
                    "Margen superior al 60%: empresa rentable. Explorar expansion."
                )
            elif margen_pct > 30:
                recomendaciones.append(
                    "Margen saludable (30-60%). Optimizar costos variables."
                )
            elif margen_pct > 0:
                recomendaciones.append(
                    "Margen bajo (0-30%). Revisar precios y estructura de costos."
                )
            else:
                recomendaciones.append(
                    "Margen negativo. La empresa pierde dinero. Revisar urgente."
                )
        else:
            recomendaciones.append(
                "Correr una simulacion completa para obtener recomendaciones especificas."
            )
        recomendaciones.append("Revisar MEJORAS_PENDIENTES.md para el backlog.")
        return recomendaciones

    def _proximos_pasos(self):
        return [
            {"etapa": 9, "nombre": "Cerebros LLM (OpenRouter + DeepSeek)", "estado": "completado"},
            {"etapa": 7, "nombre": "Conectores reales (requiere aprobacion)", "estado": "pendiente"},
            {"etapa": 8, "nombre": "Publicacion B2AI (GitHub + HuggingFace)", "estado": "pendiente"},
        ]

    def _guardar_json(self, informe):
        archivo = self.dir / "informe-ejecutivo.json"
        archivo.write_text(
            json.dumps(informe, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return archivo

    def _guardar_markdown(self, informe):
        archivo = self.dir / "informe-ejecutivo.md"
        c = informe["cerebro"]
        lineas = [
            "# AI-BUSINESS-OS - Informe Ejecutivo",
            "",
            f"**Fecha:** {informe['fecha']}",
            f"**Generado:** {informe['timestamp']}",
            "",
            "---",
            "",
            "## 1. Estado del Sistema",
            "",
            "| Metrica | Valor |",
            "|---------|-------|",
            f"| Agentes registrados | {informe['sistema']['agentes_registrados']} |",
            f"| Tareas totales | {informe['sistema']['tareas_totales']} |",
            f"| Memorias guardadas | {informe['sistema']['memorias_guardadas']} |",
            f"| Pendientes aprobacion | {informe['sistema']['pendientes_aprobacion']} |",
            f"| Estado general | {informe['sistema']['estado_general']} |",
            "",
            "---",
            "",
            "## 2. Cerebro LLM",
            "",
            "| Metrica | Valor |",
            "|---------|-------|",
            f"| Cerebro | {c.get('nombre', '?')} |",
            f"| Modelo | {c.get('modelo', '?')} |",
            f"| Tipo | {c.get('tipo', '?')} |",
            f"| Disponible | {'Si' if c.get('disponible') else 'No'} |",
            f"| Llamadas realizadas | {c.get('llamadas', 0)} |",
            f"| Errores | {c.get('errores', 0)} |",
            f"| Tokens entrada | {c.get('tokens_entrada', 0)} |",
            f"| Tokens salida | {c.get('tokens_salida', 0)} |",
            f"| Costo estimado | ${c.get('costo_estimado_usd', 0):.6f} USD |",
            "",
            "---",
            "",
            "## 3. Estado de los Agentes",
            "",
            "| Icono | Agente | Rol |",
            "|-------|--------|-----|",
        ]
        for a in informe["agentes"]:
            lineas.append(f"| {a['icono']} | {a['nombre']} | {a['rol']} |")

        lineas.extend(["", "---", "", "## 4. Ultima Simulacion", ""])
        sim = informe["ultima_simulacion"]
        if sim["disponible"]:
            lineas.extend([
                f"**Descripcion:** {sim['descripcion']}",
                f"**Fecha:** {sim['fecha']}",
                "",
                "| Metrica | Valor |",
                "|---------|-------|",
                f"| Facturacion | ${sim['facturacion']:,.0f} |",
                f"| Margen | ${sim['margen']:,.0f} |",
                f"| Margen % | {sim['margen_pct']:.1f}% |",
            ])
        else:
            lineas.append(f"_{sim['mensaje']}_")

        lineas.extend(["", "---", "", "## 5. Recomendaciones", ""])
        for r in informe["recomendaciones"]:
            lineas.append(f"- {r}")

        lineas.extend(["", "---", "", "## 6. Proximos Pasos", "",
                       "| Etapa | Nombre | Estado |", "|-------|--------|--------|"])
        for p in informe["proximos_pasos"]:
            lineas.append(f"| {p['etapa']} | {p['nombre']} | {p['estado']} |")

        lineas.extend(["", "---", "", "_Generado automaticamente por AI-BUSINESS-OS_"])

        archivo.write_text("\n".join(lineas), encoding="utf-8")
        return archivo