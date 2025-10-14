"""
Servicio de libros.
Funciones para agregar, modificar, eliminar o listar libros.
"""
import json
import os
import uuid
from utils.isbn import normalizar_isbn
from negocio.buscador_service import reconstruir_indice_isbn

# Carpeta base de todos los géneros
RUTA_BASE = os.path.join("data", "libros")


# Funciones AUXILIARES

def guardar_json(ruta, datos):
    """Guarda un archivo JSON en la ruta indicada."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def cargar_json(ruta):
    """Carga y devuelve los datos de un archivo JSON."""
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return None

def obtener_ruta_genero(genero):
    """Devuelve la ruta completa para un género determinado."""
    return os.path.join(RUTA_BASE, genero)


# Funciones PRINCIPALES

def agregar_libro(datos):
    """
    Agrega un nuevo libro a la biblioteca.

    Args:
        datos (dict): contiene 'isbn', 'title', 'autor' y 'genero'

    Returns:
        str: ID único del libro agregado
    """
    genero = datos.get("genero", "").lower()
    carpeta_genero = obtener_ruta_genero(genero)

    # Creamos la carpeta del género si no existe ya
    os.makedirs(carpeta_genero, exist_ok=True)

    # Generamos el ID único para el nuevo libro
    libro_id = str(uuid.uuid4())

    # Normalizar ISBN antes de guardar
    isbn_normalizado = normalizar_isbn(datos["isbn"])

    libro = {
        "libro_id": libro_id,
        "isbn": isbn_normalizado,  # Guardar ISBN normalizado
        "title": datos["title"],
        "autor": datos["autor"],
        "genero": genero,
        "disponible": True,
        "prestamo_actual": None,
        "historial_prestamos": []
    }

    ruta_archivo = os.path.join(carpeta_genero, f"{libro_id}.json")
    guardar_json(ruta_archivo, libro)

    # Reconstruir el índice ISBN para mantener sincronización
    reconstruir_indice_isbn()

    return libro_id


def modificar_libro(libro_id, nuevos_datos):
    """
    Modifica un libro en el sistema.

    Args:
        libro_id (str): ID del libro a modificar
        nuevos_datos (dict): datos a actualizar

    Returns:
        bool: True si se modificó correctamente, False si no se encontró
    """
    # Buscar el archivo individual del libro
    for genero in os.listdir(RUTA_BASE):
        carpeta_genero = obtener_ruta_genero(genero)

        # Saltar archivos que no son directorios
        if not os.path.isdir(carpeta_genero):
            continue

        archivo = os.path.join(carpeta_genero, f"{libro_id}.json")

        if os.path.exists(archivo):
            libro = cargar_json(archivo)
            libro.update(nuevos_datos)
            guardar_json(archivo, libro)

            # Reconstruir el índice ISBN para mantener sincronización
            reconstruir_indice_isbn()

            return True

    # No se encontró el libro
    return False


def eliminar_libro(libro_id):
    """
    Elimina un ejemplar de libro del sistema.

    Args:
        libro_id (str): ID del libro a eliminar

    Returns:
        bool: True si se eliminó correctamente, False si no se encontró
    """
    # Buscar y eliminar el archivo del ejemplar
    for genero in os.listdir(RUTA_BASE):
        carpeta_genero = obtener_ruta_genero(genero)

        # Saltar archivos que no son directorios
        if not os.path.isdir(carpeta_genero):
            continue

        archivo = os.path.join(carpeta_genero, f"{libro_id}.json")

        if os.path.exists(archivo):
            os.remove(archivo)

            # Reconstruir el índice ISBN para mantener sincronización
            reconstruir_indice_isbn()

            return True

    # No se encontró el libro
    return False


def listar_libros() -> list[dict]:
    """
    Retorna una lista con todos los libros que haya registrados en la biblioteca.

    Recorre las carpetas por género dentro de data/libros/
    y carga la información de cada archivo JSON.

    Returns:
        list[dict]: lista de libros en formato diccionario
    """
    libros = []
    try:
        for genero in os.listdir(RUTA_BASE):
            ruta_genero = os.path.join(RUTA_BASE, genero)
            if os.path.isdir(ruta_genero):
                for archivo in os.listdir(ruta_genero):
                    if archivo.endswith(".json"):
                        ruta_archivo = os.path.join(ruta_genero, archivo)
                        with open(ruta_archivo, "r", encoding="utf-8") as f:
                            libro = json.load(f)
                            libros.append(libro)
        return libros
    except Exception as e:
        print(f"Error al listar libros: {e}")
        return []
