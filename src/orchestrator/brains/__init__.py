"""Interfaz Brain - cerebro comun para los agentes de AI-BUSINESS-OS."""
from .base import Brain
from .null_brain import NullBrain
from .openrouter_brain import OpenRouterBrain


def crear_brain(tipo=None):
    """Crea un cerebro segun la configuracion.

    Args:
        tipo: "openrouter" | "null" | None (auto-detecta)

    Auto-deteccion:
        - Si hay OPENROUTER_API_KEY en .env -> OpenRouterBrain
        - Sino -> NullBrain
    """
    if tipo == "openrouter":
        return OpenRouterBrain()
    if tipo == "null":
        return NullBrain()
    if tipo is None:
        from ..config import Config
        if Config.OPENROUTER_API_KEY:
            return OpenRouterBrain()
        return NullBrain()
    raise ValueError(f"Tipo de cerebro desconocido: {tipo}")


__all__ = ["Brain", "NullBrain", "OpenRouterBrain", "crear_brain"]