import json
from pathlib import Path
from datetime import datetime
import os 

DATA_DIR = Path(__file__).parent.parent / "data"
LIBROS_DIR = DATA_DIR / "libros"
PRESTAMOS_DIR = DATA_DIR / "prestamos"
PRESTAMOS_DIR.mkdir(parents=True, exist_ok=True)
PRESTAMOS_FILE = PRESTAMOS_DIR / "prestamos.json"


def _cargar_json(ruta: Path, por_defecto):
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
                        pass
    return metadata


def obtener_prestamos_usuario(user_id: str):
    prestamos_lista = _cargar_json(PRESTAMOS_FILE, [])
    # Se asegura de acceder a user_id dentro del diccionario 'prestamo'
    return [
        p for p in prestamos_lista 
        if p.get("prestamo", {}).get("user_id", "").upper() == user_id.upper()
    ]
    
def obtener_historial_prestamos_usuario_con_info(user_id: str):
    prestamos_usuario_anidados = obtener_prestamos_usuario(user_id) 
    metadata_libros = _obtener_metadata_libros()
    historial_con_info = []
    for item in prestamos_usuario_anidados:
        p = item.get('prestamo', {})
        libro_id = p.get('libro_id')
        if libro_id and libro_id in metadata_libros:
            libro_meta = metadata_libros[libro_id]
            
            historial_con_info.append({
                "prestamo_numero": item.get('prestamo_numero'),
                "libro_id": libro_id,
                "genero": libro_meta['genero'],
                "title": libro_meta['title'],
                "user_id": p.get('user_id'),
                "fecha_prestamo": p.get('fecha_prestamo'),
                "regresado": p.get('regresado', False),
                "fecha_devolucion": p.get('fecha_devolucion')
            })
            
    return historial_con_info

def obtener_prestamos_activos_usuario_con_info(user_id: str):
    # Usa la función de historial y filtra por los que NO han sido regresados
    historial = obtener_historial_prestamos_usuario_con_info(user_id)
    return [p for p in historial if not p.get('regresado', True)]


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
    """Registra una devolución, marcando el libro como disponible."""
    ruta_libro = LIBROS_DIR / genero / f"{libro_id}.json"
    if not ruta_libro.exists():
        return False

    # 1. Actualizar estado del préstamo
    prestamos_lista = _cargar_json(PRESTAMOS_FILE, [])
    encontrado = False
    
    for item in prestamos_lista:
        p = item.get("prestamo", {})
        # Buscar el préstamo ACTIVO (regresado: false) con el ID del libro
        if p.get("libro_id") == libro_id and not p.get("regresado", True):
            p["regresado"] = True
            p["fecha_devolucion"] = datetime.now().isoformat(timespec="seconds")
            encontrado = True
            break

    if not encontrado:
        return False
    libro = _cargar_json(ruta_libro, {})
    libro["disponible"] = True
    libro["prestamo_actual"] = None
    
    _guardar_json(ruta_libro, libro)
    _guardar_json(PRESTAMOS_FILE, prestamos_lista)
    return True


def obtener_prestamos_activos():
    """Retorna una lista de todos los préstamos vigentes (solo el diccionario interno)."""
    prestamos = _cargar_json(PRESTAMOS_FILE, [])
    return [p.get("prestamo") for p in prestamos if not p.get("prestamo", {}).get("regresado", False)]

