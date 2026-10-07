"""Runner que conecta el Orchestrator con el simulador empresarial.

Coordina:
- Director (descompone objetivo)
- Arquitecto (propone estructura)
- Developer (propone codigo en sandbox)
- Quantum_RD (optimiza con Qiskit)
- Tester (valida)
- Auditor (verifica GOVERNANCE)
- Business (analiza con datos reales)
"""
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class SimulatorRunner:
    """Ejecuta el flujo completo integrando agentes + simulador."""

    def __init__(self, orchestrator):
        self.orch = orchestrator
        self.resultado = None

    def ejecutar(self, dias=30, clientes=100, productos=5, seed=42):
        """Ejecuta el flujo completo."""
        self.orch.logger.info("simulador_inicio", dias=dias, clientes=clientes)

        flujo = {
            "objetivo": f"Simular empresa virtual {dias} dias con {clientes} clientes",
            "parametros": {"dias": dias, "clientes": clientes, "productos": productos, "seed": seed},
            "pasos": [],
            "estado": "en_proceso",
        }

        # 1. Director: descompone el objetivo
        r_director = self.orch.runner.ejecutar_agente("Director", {
            "descripcion": flujo["objetivo"]
        })
        flujo["pasos"].append({"agente": "Director", "resultado": r_director})

        # 2. Arquitecto: propone estructura
        r_arq = self.orch.runner.ejecutar_agente("Arquitecto", {
            "descripcion": flujo["objetivo"]
        })
        flujo["pasos"].append({"agente": "Arquitecto", "resultado": r_arq})

        # 3. Developer: propone codigo en sandbox
        r_dev = self.orch.runner.ejecutar_agente("Developer", {
            "descripcion": "Modelo de empresa virtual con clientes y productos"
        })
        flujo["pasos"].append({"agente": "Developer", "resultado": r_dev})

        # 4. Quantum_RD: optimiza precios con Qiskit
        r_q = self.orch.runner.ejecutar_agente("Quantum_RD", {
            "descripcion": flujo["objetivo"]
        })
        flujo["pasos"].append({"agente": "Quantum_RD", "resultado": r_q})

        # 5. Correr el simulador real
        self.orch.logger.info("simulador_ejecutando", dias=dias)
        try:
            from simulator.empresa import Empresa
            from experiments.quantum_annealer import QuantumAnnealer

            empresa = Empresa(nombre="Empresa Integrada", seed=seed)
            empresa.generar_clientes(cantidad=clientes)
            empresa.generar_productos(cantidad=productos)

            # Aplicar optimizacion cuantica
            annealer = QuantumAnnealer(seed=seed)
            resultado_q = annealer.optimizar_precios(empresa.productos, iteraciones=20)
            annealer.aplicar_optimizacion(empresa.productos, resultado_q)

            # Optimizar clientes
            for c in empresa.clientes:
                c.probabilidad_compra = min(1.0, c.probabilidad_compra * 1.2)
                c.churn_probabilidad = max(0.001, c.churn_probabilidad * 0.5)

            reporte_simulacion = empresa.simular(dias)
            flujo["simulacion"] = {
                "facturacion": reporte_simulacion["facturacion"],
                "costos": reporte_simulacion["costos"],
                "margen": reporte_simulacion["margenes"]["margen"],
                "margen_pct": reporte_simulacion["margenes"]["margen_pct"],
                "clientes_activos": reporte_simulacion["clientes_activos"],
                "clientes_totales": reporte_simulacion["clientes_totales"],
                "ventas_totales": reporte_simulacion["ventas_totales"],
                "motor_quantum": resultado_q["motor"],
            }
        except Exception as e:
            self.orch.logger.error("simulador_error", error=str(e))
            flujo["simulacion"] = {"error": str(e)}

        # 6. Tester: valida el sistema
        r_test = self.orch.runner.ejecutar_agente("Tester", {
            "descripcion": flujo["objetivo"],
            "modo_flujo": True,
        })
        flujo["pasos"].append({"agente": "Tester", "resultado": r_test})

        # 7. Auditor: valida GOVERNANCE
        r_aud = self.orch.runner.ejecutar_agente("Auditor", {
            "descripcion": flujo["objetivo"]
        })
        flujo["pasos"].append({"agente": "Auditor", "resultado": r_aud})

        if not r_aud.get("aprobado", True):
            flujo["estado"] = "bloqueado_por_auditor"
            flujo["violaciones"] = r_aud.get("violaciones", [])
            return flujo

        # 8. Business: analiza viabilidad con datos reales
        r_biz = self.orch.runner.ejecutar_agente("Business", {
            "descripcion": flujo["objetivo"]
        })
        flujo["pasos"].append({"agente": "Business", "resultado": r_biz})

        flujo["estado"] = "completado"
        flujo["timestamp"] = datetime.now().isoformat()

        # Guardar en memoria
        self.orch.memory.recordar(
            "simulacion_completa",
            flujo["objetivo"],
            facturacion=flujo["simulacion"].get("facturacion", 0),
            margen=flujo["simulacion"].get("margen", 0),
            margen_pct=flujo["simulacion"].get("margen_pct", 0),
        )

        self.resultado = flujo
        self.orch.logger.info("simulador_fin", estado="completado")

        return flujo