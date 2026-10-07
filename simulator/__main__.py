"""CLI del simulador empresarial.

Uso:
  python -m simulator --simular 30
  python -m simulator --comparar
  python -m simulator --clientes 200 --dias 30
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.empresa import Empresa
from simulator.escenario import comparar_escenarios, imprimir_comparativa


def main():
    parser = argparse.ArgumentParser(description="AI-BUSINESS-OS - Simulador Empresarial")
    parser.add_argument("--simular", type=int, metavar="DIAS",
                        help="Simula N dias de una empresa virtual")
    parser.add_argument("--comparar", action="store_true",
                        help="Compara 3 estrategias (clasico vs quantum-inspired vs cuantico)")
    parser.add_argument("--dias", type=int, default=30, help="Dias a simular (default 30)")
    parser.add_argument("--clientes", type=int, default=100, help="Cantidad de clientes (default 100)")
    parser.add_argument("--productos", type=int, default=5, help="Cantidad de productos (default 5)")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    parser.add_argument("--seed", type=int, default=42, help="Semilla aleatoria (default 42)")

    args = parser.parse_args()

    if args.comparar:
        resultados = comparar_escenarios(
            dias=args.dias, clientes=args.clientes, productos=args.productos
        )
        if args.json:
            print(json.dumps(resultados, indent=2, ensure_ascii=False))
        else:
            print(imprimir_comparativa(resultados))
        return

    if args.simular:
        dias = args.simular
        empresa = Empresa(nombre="Empresa Simulada", seed=args.seed)
        empresa.generar_clientes(cantidad=args.clientes)
        empresa.generar_productos(cantidad=args.productos)
        reporte = empresa.simular(dias)
        if args.json:
            print(json.dumps(reporte, indent=2, ensure_ascii=False))
        else:
            print(empresa.reporte_imprimible())
        return

    parser.print_help()


if __name__ == "__main__":
    main()