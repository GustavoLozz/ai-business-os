"""Interfaz Brain - cerebro comun para los agentes de AI-BUSINESS-OS.

Un Brain es un motor de razonamiento (LLM o simbolico) que los agentes
pueden usar para pensar mejor. Todos los cerebros implementan la misma
interfaz `consultar(prompt) -> str | None`.

Implementaciones disponibles:
- OpenRouterBrain: usa OpenRouter (cloud) con modelos como DeepSeek, GPT, Claude.
- NullBrain: cerebro vacio (siempre devuelve None, los agentes usan logica simbolica).

Uso:
    from src.orchestrator.brains import crear_brain
    brain = crear_brain()  # auto-detecta configuracion
    respuesta = brain.consultar("Hola, quien sos?")
"""
from .base import Brain
from .null_brain import NullBrain
from .openrouter_brain import OpenRouterBrain


def crear_brain(tipo=None):
    """Crea un cerebro segun la configuracion.

    Si tipo es None, auto-detecta:
    - Si hay OPENROUTER_API_KEY en .env -> OpenRouterBrain
    - Sino -> NullBrain
    """
    if tipo == "openrouter":
        return OpenRouterBrain()
    elif tipo == "null" or tipo is None:
        from ..config import Config
        if Config.OPENROUTER_API_KEY:
            return OpenRouterBrain()
        return NullBrain()
    else:
        raise ValueError(f"Tipo de cerebro desconocido: {tipo}")


__all__ = ["Brain", "NullBrain", "OpenRouterBrain", "crear_brain"]