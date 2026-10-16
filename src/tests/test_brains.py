"""Tests de los cerebros (Brain)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.orchestrator.brains import Brain, NullBrain, OpenRouterBrain, crear_brain
from src.orchestrator.config import Config


# --- Tests de NullBrain (no gastan tokens) ---

def test_null_brain_instancia():
    b = NullBrain()
    assert b is not None
    assert b.nombre == "NullBrain"


def test_null_brain_consultar_devuelve_none():
    b = NullBrain()
    assert b.consultar("Hola") is None


def test_null_brain_info():
    b = NullBrain()
    info = b.info()
    assert info["nombre"] == "NullBrain"
    assert info["tipo"] == "null"


def test_null_brain_disponible():
    b = NullBrain()
    assert b.disponible() is True


# --- Tests de OpenRouterBrain (SIN hacer llamadas reales) ---

def test_openrouter_brain_instancia():
    b = OpenRouterBrain()
    assert b is not None
    assert b.nombre == "OpenRouterBrain"
    assert b.modelo is not None


def test_openrouter_brain_disponible_con_key():
    b = OpenRouterBrain()
    assert isinstance(b.disponible(), bool)


def test_openrouter_brain_info():
    b = OpenRouterBrain()
    info = b.info()
    assert info["nombre"] == "OpenRouterBrain"
    assert info["tipo"] == "openrouter"
    assert "modelo" in info
    assert "llamadas" in info
    assert "errores" in info


def test_openrouter_brain_sin_key_no_disponible():
    """Con api_key vacia explicitamente, debe devolver False."""
    # Forzar que use None (que es falsy) y NO la del .env
    b = OpenRouterBrain.__new__(OpenRouterBrain)
    b.api_key = None
    b.modelo = "test"
    b.max_tokens = 100
    b.timeout = 5
    b.nombre = "OpenRouterBrain"
    b.llamadas = 0
    b.errores = 0
    b.tokens_entrada = 0
    b.tokens_salida = 0
    assert b.disponible() is False


def test_openrouter_brain_consultar_sin_key_devuelve_none():
    """Sin key, consultar debe devolver None sin hacer request."""
    b = OpenRouterBrain.__new__(OpenRouterBrain)
    b.api_key = None
    b.modelo = "test"
    b.max_tokens = 100
    b.timeout = 5
    b.nombre = "OpenRouterBrain"
    b.llamadas = 0
    b.errores = 0
    b.tokens_entrada = 0
    b.tokens_salida = 0
    assert b.consultar("Hola") is None


def test_openrouter_brain_costo_estimado_cero_inicial():
    b = OpenRouterBrain()
    assert b.costo_estimado_usd() == 0.0


# --- Tests de la funcion crear_brain ---

def test_crear_brain_auto_detecta():
    b = crear_brain()
    assert isinstance(b, (OpenRouterBrain, NullBrain))


def test_crear_brain_tipo_explicito_null():
    b = crear_brain("null")
    assert isinstance(b, NullBrain)


def test_crear_brain_tipo_explicito_openrouter():
    b = crear_brain("openrouter")
    assert isinstance(b, OpenRouterBrain)


def test_crear_brain_tipo_invalido():
    try:
        crear_brain("inexistente")
        assert False, "Debio lanzar ValueError"
    except ValueError:
        assert True