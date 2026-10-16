"""OpenRouterBrain - cerebro LLM usando OpenRouter.

Usa la API de OpenRouter (https://openrouter.ai) para consultar modelos
como DeepSeek, GPT-4, Claude, Llama, etc.

Requiere: OPENROUTER_API_KEY en el .env
"""
import json
import urllib.request
import urllib.error
from .base import Brain


class OpenRouterBrain(Brain):
    URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key=None, modelo=None, max_tokens=None, timeout=30):
        from ..config import Config
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.modelo = modelo or Config.OPENROUTER_MODEL or "deepseek/deepseek-v4-flash-0731"
        self.max_tokens = max_tokens or Config.OPENROUTER_MAX_TOKENS or 1000
        self.timeout = timeout
        self.nombre = "OpenRouterBrain"
        self.llamadas = 0
        self.errores = 0
        self.tokens_entrada = 0
        self.tokens_salida = 0

    def disponible(self):
        return bool(self.api_key)

    def consultar(self, prompt, **kwargs):
        """Consulta a OpenRouter. Devuelve string o None si falla."""
        if not self.disponible():
            return None

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        system = kwargs.get("system", None)

        mensajes = []
        if system:
            mensajes.append({"role": "system", "content": system})
        mensajes.append({"role": "user", "content": prompt})

        payload = {
            "model": self.modelo,
            "messages": mensajes,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.URL,
                data=data,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/gustavo/ai-business-os",
                    "X-Title": "AI-BUSINESS-OS",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))

            self.llamadas += 1

            # Extraer uso de tokens
            usage = body.get("usage", {})
            self.tokens_entrada += usage.get("prompt_tokens", 0)
            self.tokens_salida += usage.get("completion_tokens", 0)

            # Extraer contenido
            choices = body.get("choices", [])
            if not choices:
                self.errores += 1
                return None

            contenido = choices[0].get("message", {}).get("content", "")
            return contenido.strip() if contenido else None

        except urllib.error.HTTPError as e:
            self.errores += 1
            try:
                error_body = e.read().decode("utf-8")
                print(f"[OpenRouterBrain] HTTP {e.code}: {error_body[:200]}")
            except Exception:
                print(f"[OpenRouterBrain] HTTP {e.code}")
            return None
        except urllib.error.URLError as e:
            self.errores += 1
            print(f"[OpenRouterBrain] URL error: {e.reason}")
            return None
        except Exception as e:
            self.errores += 1
            print(f"[OpenRouterBrain] Error: {e}")
            return None

    def info(self):
        return {
            "nombre": self.nombre,
            "modelo": self.modelo,
            "disponible": self.disponible(),
            "llamadas": self.llamadas,
            "errores": self.errores,
            "tokens_entrada": self.tokens_entrada,
            "tokens_salida": self.tokens_salida,
            "tipo": "openrouter",
        }

    def costo_estimado_usd(self):
        """Estima el costo total basado en tokens usados.

        Precios DeepSeek V4 Flash (2026-10):
        - Entrada: $0.0144 USD / M tokens
        - Salida:  $0.576 USD / M tokens
        """
        costo_entrada = (self.tokens_entrada / 1_000_000) * 0.0144
        costo_salida = (self.tokens_salida / 1_000_000) * 0.576
        return round(costo_entrada + costo_salida, 6)