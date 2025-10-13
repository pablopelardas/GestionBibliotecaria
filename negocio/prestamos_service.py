import json
from pathlib import Path
from datetime import datetime
import os # Necesario para la función auxiliar

DATA_DIR = Path(__file__).parent.parent / "data"
LIBROS_DIR = DATA_DIR / "libros"
PRESTAMOS_DIR = DATA_DIR / "prestamos"
PRESTAMOS_DIR.mkdir(parents=True, exist_ok=True)
PRESTAMOS_FILE = PRESTAMOS_DIR / "prestamos.json"


def _cargar_json(ruta: Path, por_defecto):
    """Carga un archivo JSON desde la ruta especificada."""
    if not ruta.exists():
        return por_defecto
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return por_defecto

def _guardar_json(ruta: Path, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def _obtener_metadata_libros():
    metadata = {}
    dir_libros = Path(__file__).parent.parent / "data" / "libros"

    if dir_libros.exists():
        for genero_dir in dir_libros.iterdir():
            if genero_dir.is_dir():
                genero = genero_dir.name
                # Lee todos los archivos JSON dentro de cada carpeta de género
                for archivo_libro in genero_dir.glob('*.json'):
                    try:
                        with open(archivo_libro, 'r', encoding='utf-8') as f:
                            libro = json.load(f)
                            if 'libro_id' in libro:
                                metadata[libro['libro_id']] = {
                                    'title': libro.get('title', 'Título Desconocido'),
                                    'genero': genero
                                }
                    except (json.JSONDecodeError, KeyError, AttributeError, FileNotFoundError):
                        pass # Ignorar archivos no JSON o faltantes
    return metadata


def obtener_prestamos_usuario(user_id: str):
    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    return [p for p in prestamos if p.get("user_id", "").upper() == user_id.upper()]


def obtener_prestamos_activos_usuario_con_info(user_id: str):
    prestamos_usuario = obtener_prestamos_usuario(user_id)
    metadata_libros = _obtener_metadata_libros()
    
    prestamos_activos_con_info = []
    
    for p in prestamos_usuario:
        # Filtrar solo por préstamos que no han sido devueltos
        if not p.get('devuelto', True):
            libro_id = p.get('libro_id')
            if libro_id and libro_id in metadata_libros:
                info = metadata_libros[libro_id]
                
                prestamos_activos_con_info.append({
                    "prestamo_numero": p.get('prestamo_numero'),
                    "libro_id": libro_id,
                    "genero": info['genero'],
                    "title": info['title'],
                    "user_id": p.get('user_id'),
                    "fecha_prestamo": p.get('fecha_prestamo')
                })
    return prestamos_activos_con_info


def registrar_prestamo(genero: str, libro_id: str, user_id: str) -> bool:
    ruta_libro = LIBROS_DIR / genero / f"{libro_id}.json"
    
    if not ruta_libro.exists():
        return False

    libro = _cargar_json(ruta_libro, {})
    
    if not libro or not libro.get("disponible", True):
        return False
    
    libro["disponible"] = False
    libro["prestamo_actual"] = user_id
    _guardar_json(ruta_libro, libro)
    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    prestamos.append({
        "prestamo_numero": len(prestamos) + 1, # Generar número de préstamo
        "prestamo": {
            "libro_id": libro_id,
            "genero": genero,
            "user_id": user_id,
            "fecha_prestamo": datetime.now().isoformat(timespec="seconds"),
            "regresado": False,
            "fecha_devolucion": None
        }
    })
    _guardar_json(PRESTAMOS_FILE, prestamos)
    return True

def registrar_devolucion(genero: str, libro_id: str) -> bool:
    ruta_libro = LIBROS_DIR /
