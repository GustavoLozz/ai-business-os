"""Logger estructurado del Orchestrator."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = ROOT / "logs" / "orchestrator.log"


class Logger:
    def __init__(self, archivo=None):
        self.archivo = Path(archivo) if archivo else LOG_FILE
        self.archivo.parent.mkdir(parents=True, exist_ok=True)

    def log(self, nivel, mensaje, **extra):
        entrada = {"timestamp": datetime.now().isoformat(), "nivel": nivel, "mensaje": mensaje}
        entrada.update(extra)
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
        return entrada

    def info(self, msg, **extra): return self.log("INFO", msg, **extra)
    def warning(self, msg, **extra): return self.log("WARNING", msg, **extra)
    def error(self, msg, **extra): return self.log("ERROR", msg, **extra)
    def audit(self, msg, **extra): return self.log("AUDIT", msg, **extra)