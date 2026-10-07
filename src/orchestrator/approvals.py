"""Sistema de aprobaciones (consola + archivo JSON)."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
APROB_FILE = ROOT / "pendiente_aprobacion.json"


class Approvals:
    def __init__(self):
        self.pendientes = {}

    def pedir(self, task_id, motivo, detalle=None):
        solicitud = {
            "task_id": task_id, "motivo": motivo, "detalle": detalle or {},
            "fecha": datetime.now().isoformat(), "estado": "pendiente",
        }
        self.pendientes[task_id] = solicitud
        self._guardar()
        return solicitud

    def _guardar(self):
        APROB_FILE.write_text(
            json.dumps(list(self.pendientes.values()), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def aprobar(self, task_id):
        if task_id in self.pendientes:
            self.pendientes[task_id]["estado"] = "aprobada"
            self._guardar()
            return True
        return False

    def rechazar(self, task_id):
        if task_id in self.pendientes:
            self.pendientes[task_id]["estado"] = "rechazada"
            self._guardar()
            return True
        return False

    def listar_pendientes(self):
        return [a for a in self.pendientes.values() if a["estado"] == "pendiente"]