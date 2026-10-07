"""Agentes de AI-BUSINESS-OS.

Los 7 agentes especializados:
- Director:      descompone objetivos en subtareas
- Arquitecto:    propone estructura tecnica
- Developer:     escribe codigo en sandbox
- Quantum_RD:    experimenta con quantum-inspired
- Tester:        corre tests automaticamente
- Auditor:       valida GOVERNANCE y bloquea si algo no cumple
- Business:      analiza viabilidad comercial
"""
from .base import Agent
from .director import Director
from .architect import Architect
from .developer import Developer
from .quantum_rd import QuantumRD
from .tester import Tester
from .auditor import Auditor
from .business import Business

__all__ = [
    "Agent",
    "Director",
    "Architect",
    "Developer",
    "QuantumRD",
    "Tester",
    "Auditor",
    "Business",
]


def crear_todos(cerebro=None):
    """Crea una instancia de cada agente."""
    return {
        "Director":   Director(cerebro=cerebro),
        "Arquitecto": Architect(cerebro=cerebro),
        "Developer":  Developer(cerebro=cerebro),
        "Quantum_RD": QuantumRD(cerebro=cerebro),
        "Tester":     Tester(cerebro=cerebro),
        "Auditor":    Auditor(cerebro=cerebro),
        "Business":   Business(cerebro=cerebro),
    }