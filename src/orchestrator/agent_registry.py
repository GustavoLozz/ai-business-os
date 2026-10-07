"""Registro de los 7 agentes del sistema."""
from datetime import datetime


AGENTES_BASE = [
    {"nombre": "Director",   "rol": "Planifica y prioriza objetivos"},
    {"nombre": "Arquitecto", "rol": "Disena estructura y arquitectura"},
    {"nombre": "Developer",  "rol": "Escribe y modifica codigo"},
    {"nombre": "Quantum_RD", "rol": "Experimenta con quantum-inspired"},
    {"nombre": "Tester",     "rol": "Crea y corre tests"},
    {"nombre": "Auditor",    "rol": "Revisa, audita y bloquea si es necesario"},
    {"nombre": "Business",   "rol": "Simula y analiza negocios"},
]


class AgentRegistry:
    def __init__(self):
        self.agentes = {
            a["nombre"]: dict(a, estado="registrado", registrado_en=datetime.now().isoformat())
            for a in AGENTES_BASE
        }

    def listar(self):
        return list(self.agentes.values())

    def obtener(self, nombre):
        return self.agentes.get(nombre)

    def activar(self, nombre):
        if nombre in self.agentes:
            self.agentes[nombre]["estado"] = "activo"
            return True
        return False

    def contar(self):
        return len(self.agentes)