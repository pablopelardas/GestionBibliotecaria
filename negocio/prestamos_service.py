import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"
LIBROS_DIR = DATA_DIR / "libros"
PRESTAMOS_DIR = DATA_DIR / "prestamos"
PRESTAMOS_DIR.mkdir(parents=True, exist_ok=True)
PRESTAMOS_FILE = PRESTAMOS_DIR / "prestamos.json"


def _cargar_json(ruta, por_defecto):
    if not ruta.exists():
        return por_defecto
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def _guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def registrar_prestamo(genero: str, libro_id: str, user_id: str) -> bool:
    ruta_libro = LIBROS_DIR / genero / f"{libro_id}.json"
    if not ruta_libro.exists():
        return False

    libro = _cargar_json(ruta_libro, {})
    if not libro or not libro.get("disponible", True):
        return False
    libro["disponible"] = False
    _guardar_json(ruta_libro, libro)

    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    prestamos.append({
        "libro_id": libro_id,
        "genero": genero,
        "user_id": user_id,
        "fecha_prestamo": datetime.now().isoformat(timespec="seconds"),
        "devuelto": False,
        "fecha_devolucion": None
    })
    _guardar_json(PRESTAMOS_FILE, prestamos)
    return True


def registrar_devolucion(genero: str, libro_id: str) -> bool:
    ruta_libro = LIBROS_DIR / genero / f"{libro_id}.json"
    if not ruta_libro.exists():
        return False

    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    encontrado = False
    for p in prestamos:
        if p["libro_id"] == libro_id and not p["devuelto"]:
            p["devuelto"] = True
            p["fecha_devolucion"] = datetime.now().isoformat(timespec="seconds")
            encontrado = True
            break

    if not encontrado:
        return False
    libro = _cargar_json(ruta_libro, {})
    libro["disponible"] = True
    _guardar_json(ruta_libro, libro)
    _guardar_json(PRESTAMOS_FILE, prestamos)
    return True


def obtener_prestamos_activos():
    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    return [p for p in prestamos if not p.get("devuelto", False)]


def obtener_prestamos_usuario(user_id: str):
    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    return [p for p in prestamos if p.get("user_id") == user_id]
