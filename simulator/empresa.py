"""Motor principal del simulador empresarial."""
import random
from .cliente import Cliente
from .producto import Producto
from .costo import Costo, total_costos, resumen_costos, costos_default
from .venta import Venta, registrar_venta, total_ventas, ventas_por_dia
from .margen import resumen_margenes, formato_moneda, formato_pct


class Empresa:
    def __init__(self, nombre="Empresa Virtual", seed=None):
        if seed is not None:
            random.seed(seed)
        self.nombre = nombre
        self.clientes = []
        self.productos = []
        self.costos = costos_default()
        self.ventas = []
        self.dias_simulados = 0
        self.historial_diario = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        return cliente

    def agregar_producto(self, producto):
        self.productos.append(producto)
        return producto

    def generar_clientes(self, cantidad=100):
        segmentos = [
            ("bajo", 20000, 0.08),
            ("medio", 50000, 0.15),
            ("alto", 120000, 0.25),
        ]
        for i in range(1, cantidad + 1):
            seg = random.choices(segmentos, weights=[0.5, 0.35, 0.15])[0]
            c = Cliente(
                id=f"C{i:04d}",
                nombre=f"Cliente {i:04d}",
                ingreso_mensual=seg[1],
                segmento=seg[0],
            )
            c.probabilidad_compra = seg[2]
            self.agregar_cliente(c)
        return self.clientes

    def generar_productos(self, cantidad=5):
        nombres = ["Basico", "Estandar", "Premium", "Deluxe", "Enterprise"]
        for i in range(1, cantidad + 1):
            nombre = nombres[(i - 1) % len(nombres)]
            costo = random.randint(100, 500)
            precio = int(costo * random.uniform(1.3, 2.5))
            p = Producto(
                id=f"P{i:03d}",
                nombre=f"Producto {nombre}",
                costo=costo,
                precio=precio,
                categoria="general",
            )
            self.agregar_producto(p)
        return self.productos

    def simular_dia(self, dia):
        """Simula un dia completo de operacion."""
        ventas_dia = []

        for cliente in self.clientes:
            if not cliente.activo:
                continue
            cliente.pasar_dia()
            if not cliente.activo:
                continue
            for producto in self.productos:
                if random.random() < cliente.probabilidad_compra:
                    cantidad = random.randint(1, 2)
                    v = registrar_venta(
                        self.ventas,
                        cliente.id,
                        producto.id,
                        cantidad,
                        producto.precio,
                        dia,
                    )
                    producto.registrar_venta(cantidad)
                    ventas_dia.append(v)

        # Registrar resumen del dia
        facturacion_dia = sum(v.total() for v in ventas_dia)
        self.historial_diario.append({
            "dia": dia,
            "ventas": len(ventas_dia),
            "facturacion": facturacion_dia,
            "clientes_activos": sum(1 for c in self.clientes if c.activo),
        })
        self.dias_simulados += 1
        return ventas_dia

    def simular(self, dias=30):
        """Simula N dias completos."""
        for dia in range(1, dias + 1):
            self.simular_dia(dia)
        return self.reporte()

    def reporte(self):
        """Devuelve el reporte completo de la simulacion."""
        facturacion = total_ventas(self.ventas)
        costos_fijos = total_costos([c for c in self.costos if c.tipo == "fijo"], 1)
        costos_variables = total_costos([c for c in self.costos if c.tipo == "variable"], self.dias_simulados)
        costos_totales = costos_fijos + costos_variables
        margenes = resumen_margenes(facturacion, costos_totales)

        return {
            "empresa": self.nombre,
            "dias_simulados": self.dias_simulados,
            "clientes_totales": len(self.clientes),
            "clientes_activos": sum(1 for c in self.clientes if c.activo),
            "productos": len(self.productos),
            "ventas_totales": len(self.ventas),
            "facturacion": facturacion,
            "costos": costos_totales,
            "margenes": margenes,
            "productos_detalle": [p.reportar() for p in self.productos],
            "top_clientes": sorted(
                [c.reportar() for c in self.clientes],
                key=lambda x: x["total_comprado"],
                reverse=True,
            )[:10],
        }

    def reporte_imprimible(self):
        """Devuelve el reporte formateado como texto."""
        r = self.reporte()
        lineas = [
            "=" * 60,
            f"  EMPRESA: {r['empresa']}",
            "=" * 60,
            f"  Dias simulados:     {r['dias_simulados']}",
            f"  Clientes totales:   {r['clientes_totales']}",
            f"  Clientes activos:   {r['clientes_activos']}",
            f"  Productos:          {r['productos']}",
            f"  Ventas totales:     {r['ventas_totales']}",
            "=" * 60,
            "  RESULTADO ECONOMICO",
            "=" * 60,
            f"  Facturacion:        {formato_moneda(r['facturacion'])}",
            f"  Costos:             {formato_moneda(r['costos'])}",
            f"  Margen:             {formato_moneda(r['margenes']['margen'])}",
            f"  Margen %:           {formato_pct(r['margenes']['margen_pct'])}",
            f"  Rentable:           {'SI' if r['margenes']['rentable'] else 'NO'}",
            "=" * 60,
        ]
        return "\n".join(lineas)

    def __repr__(self):
        return f"<Empresa {self.nombre} ({self.dias_simulados} dias, {len(self.ventas)} ventas)>"