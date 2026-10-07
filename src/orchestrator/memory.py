"""Memoria persistente en JSON."""
import json
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
        return json.loads(self.archivo.read_text(encoding="utf-8"))

    def _guardar(self, data):
        self.archivo.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def recordar(self, categoria, contenido, **extra):
        data = self._leer()
        entrada = {"timestamp": datetime.now().isoformat(), "categoria": categoria, "contenido": contenido}
        entrada.update(extra)
        data["entradas"].append(entrada)
        self._guardar(data)
        return entrada

    def buscar(self, categoria=None):
        data = self._leer()
        if categoria is None:
            return data["entradas"]
        return [e for e in data["entradas"] if e["categoria"] == categoria]

    def estadisticas(self):
        data = self._leer()
        cats = {}
        for e in data["entradas"]:
            cats[e["categoria"]] = cats.get(e["categoria"], 0) + 1
        return {"total": len(data["entradas"]), "por_categoria": cats}