"""Interfaz base Brain.

Todos los cerebros (LLM o simbolicos) implementan `consultar(prompt)`.
Devuelven un string con la respuesta del modelo, o None si fallan.
"""
from abc import ABC, abstractmethod


class Brain(ABC):
    """Interfaz base para todos los cerebros."""

    @abstractmethod
    def consultar(self, prompt, **kwargs):
        """Consulta al cerebro.

        Args:
            prompt: texto de entrada
            **kwargs: parametros opcionales (temperature, max_tokens, etc.)

        Returns:
            str con la respuesta, o None si hay error.
        """
        pass

    @abstractmethod
    def info(self):
        """Devuelve info del cerebro (nombre, modelo, estado)."""
        pass

    def disponible(self):
        """Devuelve True si el cerebro esta listo para usar."""
        return False