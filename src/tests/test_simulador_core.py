"""Tests de los modulos base del simulador."""
from simulator.cliente import Cliente
from simulator.producto import Producto
from simulator.costo import Costo, total_costos
from simulator.venta import Venta, total_ventas
from simulator.margen import calcular_margen, resumen_margenes


def test_cliente_creacion():
    c = Cliente("C001", "Test Cliente", 50000, "medio")
    assert c.id == "C001"
    assert c.ingreso_mensual == 50000
    assert c.activo is True
    assert c.cantidad_compras() == 0


def test_cliente_comprar_forzado():
    c = Cliente("C001", "Test", 50000)
    c.probabilidad_compra = 1.0  # forzar compra
    p = Producto("P001", "Test Prod", 100, 200)
    venta = c.comprar(p, cantidad=1, dia=1)
    assert venta is not None
    assert venta["total"] == 200
    assert c.cantidad_compras() == 1


def test_producto_margen():
    p = Producto("P001", "Test", costo=100, precio=200)
    assert p.margen_unitario() == 100
    assert p.margen_porcentaje() == 50.0


def test_producto_margen_cero_precio():
    p = Producto("P001", "Test", costo=100, precio=0)
    assert p.margen_porcentaje() == 0.0


def test_producto_registrar_ventas():
    p = Producto("P001", "Test", costo=100, precio=200)
    p.registrar_venta(5)
    assert p.vendidos == 5
    assert p.ingresos_totales() == 1000
    assert p.costos_totales() == 500
    assert p.ganancia_total() == 500


def test_costo_fijo_y_variable():
    c_fijo = Costo("C001", "alquiler", 50000, tipo="fijo")
    c_var = Costo("C002", "logistica", 100, tipo="variable")
    assert c_fijo.aplicar(dias=30) == 50000  # fijo no multiplica
    assert c_var.aplicar(dias=30) == 3000    # variable multiplica


def test_total_costos():
    costos = [
        Costo("C001", "alquiler", 50000, tipo="fijo"),
        Costo("C002", "logistica", 100, tipo="variable"),
    ]
    assert total_costos(costos, dias=1) == 50100
    assert total_costos(costos, dias=30) == 53000


def test_venta_total():
    v = Venta("V001", "C001", "P001", cantidad=3, precio_unitario=200, dia=1)
    assert v.total() == 600


def test_total_ventas():
    ventas = [
        Venta("V001", "C001", "P001", 2, 200, 1),
        Venta("V002", "C002", "P002", 1, 500, 1),
    ]
    assert total_ventas(ventas) == 900


def test_calcular_margen():
    m = calcular_margen(ingresos=1000, costos=600)
    assert m["margen"] == 400
    assert m["margen_pct"] == 40.0
    assert m["ingresos"] == 1000
    assert m["costos"] == 600


def test_calcular_margen_ingresos_cero():
    m = calcular_margen(ingresos=0, costos=600)
    assert m["margen_pct"] == 0.0
    assert m["margen"] == -600


def test_resumen_margenes_rentable():
    r = resumen_margenes(ventas_totales=1000, costos_totales=600)
    assert r["rentable"] is True
    assert r["margen"] == 400


def test_resumen_margenes_no_rentable():
    r = resumen_margenes(ventas_totales=500, costos_totales=600)
    assert r["rentable"] is False
    assert r["margen"] == -100