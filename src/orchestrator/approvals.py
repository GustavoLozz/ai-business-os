"""Sistema de aprobaciones con persistencia y estado.

Mejorado segun auditoria externa de Claude (2026-10-16):
- Persiste y relee el JSON (no se pierde al cerrar el proceso).
- Escritura atomica (temp + os.replace), igual que Memory.
- Metodos: estado(), esta_aprobada(), obtener(), consumir().
- La aprobacion es de un solo uso (consumir).
"""
import json
import os
import tempfile
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
APROB_FILE = ROOT / "pendiente_aprobacion.json"


class Approvals:
    def __init__(self, archivo=None):
        self.archivo = Path(archivo) if archivo else APROB_FILE
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        self.pendientes = self._cargar()

    # ------------------------------------------------------------------
    # API publica
    # ------------------------------------------------------------------
    def pedir(self, task_id, motivo, detalle=None):
        """Crea una solicitud de aprobacion persistente."""
        solicitud = {
            "task_id": task_id,
            "motivo": motivo,
            "detalle": detalle or {},
            "fecha": datetime.now().isoformat(),
            "estado": "pendiente",
        }
        self.pendientes[task_id] = solicitud
        self._guardar()
        return solicitud

    def aprobar(self, task_id):
        """Marca una solicitud como aprobada."""
        if task_id in self.pendientes:
            self.pendientes[task_id]["estado"] = "aprobada"
            self.pendientes[task_id]["resuelto_en"] = datetime.now().isoformat()
            self._guardar()
            return True
        return False

    def rechazar(self, task_id):
        """Marca una solicitud como rechazada."""
        if task_id in self.pendientes:
            self.pendientes[task_id]["estado"] = "rechazada"
            self.pendientes[task_id]["resuelto_en"] = datetime.now().isoformat()
            self._guardar()
            return True
        return False

    def estado(self, task_id):
        """Devuelve el estado de una solicitud: pendiente/aprobada/rechazada/None."""
        if task_id not in self.pendientes:
            return None
        return self.pendientes[task_id].get("estado")

    def esta_aprobada(self, task_id):
        """Devuelve True si la solicitud esta aprobada."""
        return self.estado(task_id) == "aprobada"

    def obtener(self, task_id):
        """Devuelve la solicitud completa."""
        return self.pendientes.get(task_id)

    def consumir(self, task_id):
        """Marca la aprobacion como consumida (un solo uso).

        Devuelve True si estaba aprobada y ahora quedo consumida.
        Devuelve False si no existia o no estaba aprobada.
        """
        if task_id not in self.pendientes:
            return False
        if self.pendientes[task_id]["estado"] != "aprobada":
            return False
        self.pendientes[task_id]["estado"] = "consumida"
        self.pendientes[task_id]["consumido_en"] = datetime.now().isoformat()
        self._guardar()
        return True

    def listar_pendientes(self):
        """Lista solo las solicitudes pendientes."""
        return [a for a in self.pendientes.values() if a["estado"] == "pendiente"]

    def listar_todas(self):
        """Lista todas las solicitudes."""
        return list(self.pendientes.values())

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def _cargar(self):
        """Lee el archivo JSON. Devuelve dict indexado por task_id."""
        if not self.archivo.exists():
            return {}
        try:
            contenido = self.archivo.read_text(encoding="utf-8")
            if not contenido.strip():
                return {}
            data = json.loads(contenido)
            # Acepta tanto lista como dict
            if isinstance(data, list):
                return {item["task_id"]: item for item in data if "task_id" in item}
            if isinstance(data, dict):
                return data
            return {}
        except (json.JSONDecodeError, OSError, KeyError):
            return {}

    def _guardar(self):
        """Escritura atomica: temp + os.replace."""
        try:
            fd, tmp_path = tempfile.mkstemp(
                dir=str(self.archivo.parent), suffix=".tmp"
            )
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(
                    list(self.pendientes.values()),
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
            os.replace(tmp_path, self.archivo)
        except OSError:
            pass

    def recargar(self):
        """Recarga desde disco (util si otro proceso modifico el archivo)."""
        self.pendientes = self._cargar()