"""Configuracion central del sistema.

SEGURIDAD: lee UNICAMENTE desde el .env del proyecto.
Ignora las variables de entorno globales de Windows para evitar
que otras API keys ajenas al proyecto se filtren por accidente.
"""
from pathlib import Path

try:
    from dotenv import dotenv_values
    _DOTENV_DISPONIBLE = True
except ImportError:
    _DOTENV_DISPONIBLE = False

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env"

# Leer SOLO del .env local (no del entorno global)
if _DOTENV_DISPONIBLE and ENV_FILE.exists():
    _ENV = dotenv_values(ENV_FILE)
else:
    _ENV = {}


def _get_str(key, default=""):
    val = _ENV.get(key, default)
    if val is None:
        return default
    return str(val)


def _get_int(key, default=0):
    try:
        return int(_ENV.get(key, default))
    except (ValueError, TypeError):
        return default


def _get_float(key, default=0.0):
    try:
        return float(_ENV.get(key, default))
    except (ValueError, TypeError):
        return default


def _get_bool(key, default=False):
    val = str(_ENV.get(key, default)).lower()
    return val in ("true", "1", "yes", "si", "on")


class Config:
    """Configuracion del sistema. Solo lee del .env del proyecto."""

    # LLM / Cerebros
    OLLAMA_HOST = _get_str("OLLAMA_HOST", "")
    OLLAMA_MODEL = _get_str("OLLAMA_MODEL", "")
    OPENAI_API_KEY = _get_str("OPENAI_API_KEY", "")
    OPENAI_MODEL = _get_str("OPENAI_MODEL", "gpt-4o-mini")
    ANTHROPIC_API_KEY = _get_str("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = _get_str("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

    # Rutas
    AI_BUSINESS_OS_ROOT = Path(_get_str("AI_BUSINESS_OS_ROOT", str(ROOT)))

    # Governance
    MAX_INTENTOS_POR_TAREA = _get_int("MAX_INTENTOS_POR_TAREA", 3)
    MAX_TIEMPO_POR_TAREA_SEG = _get_int("MAX_TIEMPO_POR_TAREA_SEG", 300)
    MAX_COSTO_AGENTES_USD = _get_float("MAX_COSTO_AGENTES_USD", 1.00)
    REQUIERE_APROBACION = _get_bool("REQUIERE_APROBACION", True)

    # Logging
    LOG_LEVEL = _get_str("LOG_LEVEL", "INFO")
    LOG_FILE = _get_str("LOG_FILE", "logs/orchestrator.log")

    # Simulador
    SIMULADOR_DIAS_DEFAULT = _get_int("SIMULADOR_DIAS_DEFAULT", 30)
    SIMULADOR_CLIENTES_DEFAULT = _get_int("SIMULADOR_CLIENTES_DEFAULT", 100)
    SIMULADOR_PRODUCTOS_DEFAULT = _get_int("SIMULADOR_PRODUCTOS_DEFAULT", 5)
    SIMULADOR_SEED_DEFAULT = _get_int("SIMULADOR_SEED_DEFAULT", 42)

    # Quantum
    QISKIT_SHOTS = _get_int("QISKIT_SHOTS", 1024)
    QISKIT_ANNEALING_ITERACIONES = _get_int("QISKIT_ANNEALING_ITERACIONES", 20)

    @classmethod
    def reportar(cls):
        return {
            "dotenv_disponible": _DOTENV_DISPONIBLE,
            "env_file_existe": ENV_FILE.exists(),
            "solo_lee_del_env_local": True,
            "llm_configurado": bool(cls.OLLAMA_HOST or cls.OPENAI_API_KEY or cls.ANTHROPIC_API_KEY),
            "max_intentos": cls.MAX_INTENTOS_POR_TAREA,
            "log_level": cls.LOG_LEVEL,
            "simulador_defaults": {
                "dias": cls.SIMULADOR_DIAS_DEFAULT,
                "clientes": cls.SIMULADOR_CLIENTES_DEFAULT,
                "productos": cls.SIMULADOR_PRODUCTOS_DEFAULT,
                "seed": cls.SIMULADOR_SEED_DEFAULT,
            },
        }