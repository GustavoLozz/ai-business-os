"""Experimento 01: empresa virtual 30 dias, 3 estrategias comparadas."""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.empresa import Empresa
from simulator.escenario import escenario_clasico, escenario_quantum_inspired
from simulator.margen import formato_moneda, formato_pct
from experiments.quantum_annealer import QuantumAnnealer, qiskit_disponible
from experiments import RESULTADOS_DIR


def correr_experimento(dias=30, clientes=100, productos=5, seed=42):
    """Corre el experimento completo."""
    print("=" * 70)
    print("  EXPERIMENTO 01 - Empresa virtual 30 dias")
    print("=" * 70)
    print(f"  Dias: {dias} | Clientes: {clientes} | Productos: {productos}")
    print(f"  Qiskit disponible: {'SI' if qiskit_disponible() else 'NO (fallback clasico)'}")
    print("=" * 70)
    print()

    resultados = {}

    # --- Escenario 1: Clasico ---
    print("[1/3] Corriendo escenario clasico...")
    e1 = escenario_clasico()
    r1 = e1.ejecutar(dias=dias, clientes=clientes, productos=productos)
    resultados["clasico"] = {
        "nombre": "Clasico",
        "facturacion": r1["facturacion"],
        "costos": r1["costos"],
        "margen": r1["margenes"]["margen"],
        "margen_pct": r1["margenes"]["margen_pct"],
        "clientes_activos": r1["clientes_activos"],
        "ventas": r1["ventas_totales"],
    }
    print(f"      Facturacion: {formato_moneda(r1['facturacion'])}")
    print(f"      Margen:      {formato_moneda(r1['margenes']['margen'])} "
          f"({formato_pct(r1['margenes']['margen_pct'])})")
    print()

    # --- Escenario 2: Quantum-Inspired ---
    print("[2/3] Corriendo escenario quantum-inspired...")
    e2 = escenario_quantum_inspired()
    r2 = e2.ejecutar(dias=dias, clientes=clientes, productos=productos)
    resultados["quantum_inspired"] = {
        "nombre": "Quantum-Inspired",
        "facturacion": r2["facturacion"],
        "costos": r2["costos"],
        "margen": r2["margenes"]["margen"],
        "margen_pct": r2["margenes"]["margen_pct"],
        "clientes_activos": r2["clientes_activos"],
        "ventas": r2["ventas_totales"],
    }
    print(f"      Facturacion: {formato_moneda(r2['facturacion'])}")
    print(f"      Margen:      {formato_moneda(r2['margenes']['margen'])} "
          f"({formato_pct(r2['margenes']['margen_pct'])})")
    print()

    # --- Escenario 3: Cuantico (con Qiskit real) ---
    print("[3/3] Corriendo escenario cuantico (Qiskit annealing)...")
    emp3 = Empresa(nombre="Cuantico", seed=seed)
    emp3.generar_clientes(cantidad=clientes)
    emp3.generar_productos(cantidad=productos)

    annealer = QuantumAnnealer(seed=seed)
    resultado_annealing = annealer.optimizar_precios(emp3.productos, iteraciones=20)
    annealer.aplicar_optimizacion(emp3.productos, resultado_annealing)

    for c in emp3.clientes:
        c.probabilidad_compra = min(1.0, c.probabilidad_compra * 1.2)
        c.churn_probabilidad = max(0.001, c.churn_probabilidad * 0.5)

    r3 = emp3.simular(dias)
    resultados["cuantico"] = {
        "nombre": "Cuantico (Qiskit)",
        "facturacion": r3["facturacion"],
        "costos": r3["costos"],
        "margen": r3["margenes"]["margen"],
        "margen_pct": r3["margenes"]["margen_pct"],
        "clientes_activos": r3["clientes_activos"],
        "ventas": r3["ventas_totales"],
        "motor_quantum": resultado_annealing["motor"],
        "iteraciones_annealing": resultado_annealing["iteraciones"],
    }
    print(f"      Facturacion: {formato_moneda(r3['facturacion'])}")
    print(f"      Margen:      {formato_moneda(r3['margenes']['margen'])} "
          f"({formato_pct(r3['margenes']['margen_pct'])})")
    print(f"      Motor:       {resultado_annealing['motor']}")
    print()

    # --- Comparativa ---
    base_margen = resultados["clasico"]["margen"]
    print("=" * 70)
    print("  COMPARATIVA FINAL")
    print("=" * 70)
    print(f"  {'Estrategia':<25} {'Margen':>15} {'Mejora':>10}")
    print("-" * 70)
    for key in ["clasico", "quantum_inspired", "cuantico"]:
        r = resultados[key]
        if base_margen != 0:
            mejora = ((r["margen"] - base_margen) / abs(base_margen)) * 100
        else:
            mejora = 0.0
        r["mejora_pct"] = round(mejora, 2)
        print(f"  {r['nombre']:<25} {formato_moneda(r['margen']):>15} {formato_pct(mejora):>10}")
    print("=" * 70)

    mejor = max(resultados.values(), key=lambda x: x["margen"])
    print()
    print(f"  RECOMENDACION: usar estrategia '{mejor['nombre']}'")
    print(f"                 (margen {formato_moneda(mejor['margen'])})")
    print()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = RESULTADOS_DIR / f"experimento_01_{timestamp}.json"
    payload = {
        "experimento": "01",
        "fecha": timestamp,
        "parametros": {"dias": dias, "clientes": clientes, "productos": productos, "seed": seed},
        "resultados": resultados,
        "recomendacion": mejor["nombre"],
    }
    archivo.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Resultados guardados en: {archivo}")
    print("=" * 70)

    return payload


def main():
    parser = argparse.ArgumentParser(description="Experimento 01 - AI-BUSINESS-OS")
    parser.add_argument("--dias", type=int, default=30)
    parser.add_argument("--clientes", type=int, default=100)
    parser.add_argument("--productos", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    correr_experimento(
        dias=args.dias,
        clientes=args.clientes,
        productos=args.productos,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()