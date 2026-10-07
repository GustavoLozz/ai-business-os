"""Modelo de venta. Conecta cliente + producto."""


class Venta:
    def __init__(self, id, cliente_id, producto_id, cantidad, precio_unitario, dia=1):
        self.id = id
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.dia = dia

    def total(self):
        return self.precio_unitario * self.cantidad

    def reportar(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "total": self.total(),
            "dia": self.dia,
        }

    def __repr__(self):
        return f"<Venta {self.id}: {self.cantidad}x ${self.precio_unitario} = ${self.total()}>"


def registrar_venta(ventas, cliente_id, producto_id, cantidad, precio_unitario, dia=1):
    """Crea una Venta con ID autoincremental y la agrega a la lista."""
    siguiente_id = f"V{len(ventas) + 1:06d}"
    v = Venta(siguiente_id, cliente_id, producto_id, cantidad, precio_unitario, dia)
    ventas.append(v)
    return v


def total_ventas(ventas):
    """Suma total facturado."""
    return sum(v.total() for v in ventas)


def ventas_por_dia(ventas):
    """Devuelve diccionario {dia: total}."""
    resumen = {}
    for v in ventas:
        resumen[v.dia] = resumen.get(v.dia, 0) + v.total()
    return resumen


def ventas_por_producto(ventas):
    """Devuelve diccionario {producto_id: total}."""
    resumen = {}
    for v in ventas:
        resumen[v.producto_id] = resumen.get(v.producto_id, 0) + v.total()
    return resumen


def ventas_por_cliente(ventas):
    """Devuelve diccionario {cliente_id: total}."""
    resumen = {}
    for v in ventas:
        resumen[v.cliente_id] = resumen.get(v.cliente_id, 0) + v.total()
    return resumen