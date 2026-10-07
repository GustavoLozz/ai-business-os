"""Calculo de margenes y rentabilidad."""


def calcular_margen(ingresos, costos):
    """Devuelve dict con margen absoluto y porcentaje."""
    margen = ingresos - costos
    if ingresos == 0:
        pct = 0.0
    else:
        pct = (margen / ingresos) * 100
    return {
        "ingresos": ingresos,
        "costos": costos,
        "margen": margen,
        "margen_pct": round(pct, 2),
    }


def resumen_margenes(ventas_totales, costos_totales):
    """Devuelve un resumen formateado para reporte."""
    m = calcular_margen(ventas_totales, costos_totales)
    return {
        "facturacion": m["ingresos"],
        "costos": m["costos"],
        "margen": m["margen"],
        "margen_pct": m["margen_pct"],
        "rentable": m["margen"] > 0,
    }


def formato_moneda(valor):
    """Formatea un numero como moneda simple."""
    return f"${valor:,.0f}"


def formato_pct(valor):
    """Formatea un porcentaje."""
    return f"{valor:.1f}%"