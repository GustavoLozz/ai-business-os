"""Memoria persistente en JSON con escritura atomica y tolerante a corrupcion."""
import json
import os
import tempfile
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
MEM_FILE = ROOT / "memory" / "memory.json"


class Memory:
    def __init__(self, archivo=None):
        self.archivo = Path(archivo) if archivo else MEM_FILE
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        if not self.archivo.exists():
            self._guardar({"creado": datetime.now().isoformat(), "entradas": []})

    def _leer(self):
        """Lee el archivo. Si esta corrupto, devuelve estructura vacia."""
        try:
            contenido = self.archivo.read_text(encoding="utf-8")
            if not contenido.strip():
                return {"creado": datetime.now().isoformat(), "entradas": []}
            return json.loads(contenido)
        except (json.JSONDecodeError, OSError):
            # Recuperacion: archivo corrupto -> empezar de cero
            return {"creado": datetime.now().isoformat(), "entradas": []}

    def _guardar(self, data):
        """Escritura atomica: escribe a temp + rename."""
        try:
            fd, tmp_path = tempfile.mkstemp(
                dir=str(self.archivo.parent), suffix=".tmp"
            )
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.archivo)
        except OSError:
            # Fallback silencioso si hay conflicto de archivo
            pass

    def recordar(self, categoria, contenido, **extra):
        data = self._leer()
        entrada = {
            "timestamp": datetime.now().isoformat(),
            "categoria": categoria,
            "contenido": str(contenido)[:500],  # limite para no inflar
        }
        entrada.update({k: str(v)[:200] for k, v in extra.items()})
        data["entradas"].append(entrada)
        # Limite: mantener ultimas 200 entradas para no crecer infinito
        if len(data["entradas"]) > 200:
            data["entradas"] = data["entradas"][-200:]
        self._guardar(data)
        return entrada

    def buscar(self, categoria=None):
        data = self._leer()
        if categoria is None:
            return data.get("entradas", [])
        return [e for e in data.get("entradas", []) if e.get("categoria") == categoria]

    def estadisticas(self):
        data = self._leer()
        cats = {}
        for e in data.get("entradas", []):
            cat = e.get("categoria", "sin_categoria")
            cats[cat] = cats.get(cat, 0) + 1
        return {"total": len(data.get("entradas", [])), "por_categoria": cats}

    def resetear(self):
        """Resetea la memoria a estado limpio."""
        self._guardar({"creado": datetime.now().isoformat(), "entradas": []})