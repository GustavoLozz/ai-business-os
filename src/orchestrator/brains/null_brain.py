"""NullBrain - cerebro vacio.

Siempre devuelve None. Los agentes caen en su logica simbolica.
Es el fallback cuando no hay ningun LLM configurado.
"""
from .base import Brain


class NullBrain(Brain):
    def __init__(self):
        self.nombre = "NullBrain"
        self.modelo = "simbolico"
        self.disponible_estado = True

    def consultar(self, prompt, **kwargs):
        return None

    def info(self):
        return {
            "nombre": self.nombre,
            "modelo": self.modelo,
            "disponible": self.disponible_estado,
            "tipo": "null",
        }

    def disponible(self):
        return self.disponible_estado