import json
import os
import uuid
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "libros"
INDICE_FILE = DATA_DIR / "indice_isbn.json"

def _guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def _cargar_json(ruta):
    if not ruta.exists():
        return None
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def alta_libro(titulo, autor, isbn, genero):
    """
    Crea un nuevo ejemplar JSON dentro de data/libros/{genero}/
    y actualiza el índice ISBN.
    """
    genero_dir = DATA_DIR / genero
    genero_dir.mkdir(parents=True, exist_ok=True)

    libro_id = str(uuid.uuid4())
    nuevo_libro = {
        "id": libro_id,
        "title": titulo,
        "autor": autor,
        "isbn": isbn,
        "genero": genero,
        "disponible": True
    }

    ruta_archivo = genero_dir / f"{libro_id}.json"
    _guardar_json(ruta_archivo, nuevo_libro)

    _actualizar_indice_isbn(isbn, titulo, autor, genero, str(ruta_archivo))
    return nuevo_libro


def modificar_libro(genero, libro_id, nuevos_datos):
    """
    Modifica los datos de un libro existente.
    """
    ruta_archivo = DATA_DIR / genero / f"{libro_id}.json"
    if not ruta_archivo.exists():
        return None

    libro = _cargar_json(ruta_archivo)
    libro.update(nuevos_datos)
    _guardar_json(ruta_archivo, libro)
    return libro


def eliminar_libro(genero, libro_id):
    """
    Elimina el archivo JSON de un libro.
    """
    ruta_archivo = DATA_DIR / genero / f"{libro_id}.json"
    if ruta_archivo.exists():
        os.remove(ruta_archivo)
        return True
    return False


def _actualizar_indice_isbn(isbn, titulo, autor, genero, ruta):
    """
    Agrega el nuevo libro al índice de ISBN.
    """
    indice = _cargar_json(INDICE_FILE) or []

    # Buscar si ya existe el ISBN
    for entrada in indice:
        if entrada["isbn"] == isbn:
            entrada["ejemplares"].append({"ruta": ruta})
            break
    else:
        indice.append({
            "isbn": isbn,
            "title": titulo,
            "autor": autor,
            "genero": genero,
            "ejemplares": [{"ruta": ruta}]
        })

    _guardar_json(INDICE_FILE, indice)
