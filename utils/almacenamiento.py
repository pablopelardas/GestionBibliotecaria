from __future__ import annotations
import json
from pathlib import Path
from typing import Any

# Raíz = carpeta donde está principal.py
ROOT = Path(__file__).resolve().parents[1]
DATOS = ROOT / "datos"
LIBROS_ROOT = DATOS / "libros"
PRESTAMOS_PATH = DATOS / "prestamos" / "prestamos.json"

def asegurar_carpetas() -> None:
    (DATOS / "prestamos").mkdir(parents=True, exist_ok=True)
    (DATOS / "libros").mkdir(parents=True, exist_ok=True)

def leer_json(path: Path, default: Any) -> Any:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        escribir_json(path, default)
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def escribir_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)

def buscar_libro_recursivo(libro_id: str) -> Path | None:
    """Busca recursivamente <libro_id>.json dentro de datos/libros/**"""
    objetivo = f"{libro_id}.json"
    for p in LIBROS_ROOT.rglob("*.json"):
        if p.name == objetivo:
            return p
    return None
