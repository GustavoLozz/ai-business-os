"""Agente Developer. Escribe y modifica codigo en sandbox."""
from .base import Agent


class Developer(Agent):
    def __init__(self, cerebro=None):
        super().__init__(
            nombre="Developer",
            rol="Escribe y modifica codigo",
            permisos=["escribir_codigo", "modificar_codigo", "crear_archivos"],
            cerebro=cerebro,
        )
        # El Developer NUNCA escribe en produccion: solo propone codigo
        self.sandbox = []

    def _ejecutar_especifico(self, tarea):
        descripcion = tarea.get("descripcion", "") if isinstance(tarea, dict) else str(tarea)
        self._log("programando", descripcion=descripcion)

        prompt = (
            f"Escribe un esqueleto de codigo Python para esta tarea. "
            f"Devuelve SOLO un JSON con la forma "
            f'{{"archivos": [{{"nombre": "...", "contenido": "..."}}], "notas": "..."}}. '
            f"Tarea: {descripcion}"
        )
        respuesta_llm = self._usar_cerebro(prompt)

        if respuesta_llm:
            propuesta = self._parsear_respuesta(respuesta_llm, descripcion)
        else:
            propuesta = self._programar_simbolico(descripcion)

        # Guardar en sandbox (NUNCA en produccion)
        self.sandbox.append(propuesta)
        self._log("propuesta_lista", archivos=len(propuesta.get("archivos", [])))

        return {
            "agente": self.nombre,
            "descripcion": descripcion,
            "propuesta": propuesta,
            "sandbox": True,
            "requiere_aprobacion": True,  # por GOVERNANCE
            "metodo": "llm" if respuesta_llm else "simbolico",
        }

    def _parsear_respuesta(self, respuesta, descripcion):
        import json
        try:
            if isinstance(respuesta, str):
                limpio = respuesta.strip()
                if limpio.startswith("```"):
                    limpio = limpio.split("```")[1]
                    if limpio.startswith("json"):
                        limpio = limpio[4:]
                return json.loads(limpio)
        except Exception as e:
            self._log("error_parseo_llm", error=str(e))
        return self._programar_simbolico(descripcion)

    def _programar_simbolico(self, descripcion):
        """Genera un esqueleto determinista de codigo."""
        base = descripcion.lower()

        if "cliente" in base:
            return {
                "archivos": [{
                    "nombre": "clientes.py",
                    "contenido": (
                        "class Cliente:\n"
                        "    def __init__(self, id, nombre, ingreso_mensual):\n"
                        "        self.id = id\n"
                        "        self.nombre = nombre\n"
                        "        self.ingreso_mensual = ingreso_mensual\n"
                        "        self.compras = []\n"
                        "\n"
                        "    def agregar_compra(self, producto, cantidad):\n"
                        "        self.compras.append({'producto': producto, 'cantidad': cantidad})\n"
                    ),
                }],
                "notas": "Modelo basico de cliente con ingreso y compras.",
            }
        elif "producto" in base:
            return {
                "archivos": [{
                    "nombre": "productos.py",
                    "contenido": (
                        "class Producto:\n"
                        "    def __init__(self, id, nombre, costo, precio):\n"
                        "        self.id = id\n"
                        "        self.nombre = nombre\n"
                        "        self.costo = costo\n"
                        "        self.precio = precio\n"
                        "\n"
                        "    def margen(self):\n"
                        "        return (self.precio - self.costo) / self.precio if self.precio else 0\n"
                    ),
                }],
                "notas": "Modelo basico de producto con costo, precio y margen.",
            }
        elif "costo" in base:
            return {
                "archivos": [{
                    "nombre": "costos.py",
                    "contenido": (
                        "class Costo:\n"
                        "    def __init__(self, categoria, monto):\n"
                        "        self.categoria = categoria\n"
                        "        self.monto = monto\n"
                    ),
                }],
                "notas": "Modelo basico de costo por categoria.",
            }
        elif "venta" in base:
            return {
                "archivos": [{
                    "nombre": "ventas.py",
                    "contenido": (
                        "class Venta:\n"
                        "    def __init__(self, cliente, producto, cantidad, fecha):\n"
                        "        self.cliente = cliente\n"
                        "        self.producto = producto\n"
                        "        self.cantidad = cantidad\n"
                        "        self.fecha = fecha\n"
                        "\n"
                        "    def total(self):\n"
                        "        return self.producto.precio * self.cantidad\n"
                    ),
                }],
                "notas": "Modelo basico de venta.",
            }
        else:
            return {
                "archivos": [{
                    "nombre": "modulo.py",
                    "contenido": (
                        "def ejecutar(parametros):\n"
                        "    '''Esqueleto generado por el Developer.'''\n"
                        "    return {'status': 'pendiente', 'parametros': parametros}\n"
                    ),
                }],
                "notas": f"Esqueleto generico para: {descripcion[:80]}",
            }