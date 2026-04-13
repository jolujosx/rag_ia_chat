# app/db.py

import os
import pickle
from pathlib import Path
from typing import Optional

# Directorio para almacenar datos serializados (en disco, no en RAM)
STORAGE_DIR = Path("app/storage")
STORAGE_DIR.mkdir(exist_ok=True)

def _get_user_path(user_id: str) -> Path:
    """Genera una ruta segura para el usuario."""
    # Sanitizar user_id para evitar path traversal
    safe_id = "".join(c for c in user_id if c.isalnum() or c in "._-")
    return STORAGE_DIR / f"{safe_id}.pkl"

def guardar_motor(user_id: str, trozos_texto: list):
    """
    Guarda SOLO los fragmentos de texto del PDF (no el motor completo).
    Es ligero, persistente y seguro.
    """
    try:
        data = {
            "trozos": trozos_texto,
            "version": "1.0"
        }
        with open(_get_user_path(user_id), "wb") as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"[ERROR] guardar_motor: {e}")
        return False

def obtener_motor(user_id: str) -> Optional[list]:
    """
    Recupera los fragmentos de texto para reconstruir el motor bajo demanda.
    Devuelve None si no existe.
    """
    try:
        path = _get_user_path(user_id)
        if not path.exists():
            return None
        
        with open(path, "rb") as f:
            data = pickle.load(f)
        return data.get("trozos")
    except Exception as e:
        print(f"[ERROR] obtener_motor: {e}")
        return None

def eliminar_motor(user_id: str):
    """Limpia el almacenamiento del usuario (opcional)."""
    try:
        path = _get_user_path(user_id)
        if path.exists():
            path.unlink()
    except Exception as e:
        print(f"[ERROR] eliminar_motor: {e}")