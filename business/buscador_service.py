"""
Servicio de búsqueda de libros.
Implementa búsqueda binaria por ISBN y búsqueda recursiva por texto libre.
"""

import json
from pathlib import Path


# Variable global para cachear el índice en memoria
_indice_isbn_cache = None


def obtener_directorio_base():
    """Obtiene el directorio base del proyecto"""
    return Path(__file__).parent.parent


def obtener_directorio_libros():
    """Obtiene el directorio donde están los libros"""
    return obtener_directorio_base() / 'data' / 'libros'


def cargar_indice_isbn():
    """
    Carga el índice de ISBNs en memoria (ordenado).

    Returns:
        list: Lista de entradas del índice ordenadas por ISBN
    """
    global _indice_isbn_cache

    if _indice_isbn_cache is None:
        archivo_indice = obtener_directorio_libros() / 'indice_isbn.json'
        with open(archivo_indice, 'r', encoding='utf-8') as f:
            _indice_isbn_cache = json.load(f)

    return _indice_isbn_cache


def busqueda_binaria_isbn(isbn_buscado):
    """
    Búsqueda binaria RECURSIVA por ISBN en el índice ordenado.

    Args:
        isbn_buscado (str): ISBN a buscar

    Returns:
        dict: Información del libro con todos sus ejemplares, o None si no se encuentra
    """
    # Cargar índice
    indice = cargar_indice_isbn()

    # Llamar a la función recursiva
    return _busqueda_binaria_recursiva(indice, isbn_buscado, 0, len(indice) - 1)


def _busqueda_binaria_recursiva(indice, isbn_buscado, izquierda, derecha):
    """
    Implementación RECURSIVA de búsqueda binaria.

    Args:
        indice (list): Lista ordenada de libros por ISBN
        isbn_buscado (str): ISBN a buscar
        izquierda (int): Índice izquierdo del rango de búsqueda
        derecha (int): Índice derecho del rango de búsqueda

    Returns:
        dict: Información del libro o None si no se encuentra
    """
    # Caso base: no se encontró (rango vacío)
    if izquierda > derecha:
        return None

    # Calcular punto medio
    medio = (izquierda + derecha) // 2
    isbn_medio = indice[medio]['isbn']

    # Caso base: se encontró el ISBN
    if isbn_medio == isbn_buscado:
        return cargar_detalles_ejemplares(indice[medio])

    # Caso recursivo: buscar en mitad izquierda
    elif isbn_medio > isbn_buscado:
        return _busqueda_binaria_recursiva(indice, isbn_buscado, izquierda, medio - 1)

    # Caso recursivo: buscar en mitad derecha
    else:
        return _busqueda_binaria_recursiva(indice, isbn_buscado, medio + 1, derecha)


def cargar_detalles_ejemplares(entrada_indice):
    """
    Carga los detalles completos de todos los ejemplares de un ISBN.

    Args:
        entrada_indice (dict): Entrada del índice con información básica

    Returns:
        dict: Diccionario con información completa del libro y sus ejemplares
    """
    base_dir = obtener_directorio_base()

    resultado = {
        'isbn': entrada_indice['isbn'],
        'title': entrada_indice['title'],
        'autor': entrada_indice['autor'],
        'genero': entrada_indice['genero'],
        'ejemplares': []
    }

    for ejemplar_info in entrada_indice['ejemplares']:
        ruta = base_dir / ejemplar_info['ruta']
        if ruta.exists():
            with open(ruta, 'r', encoding='utf-8') as f:
                ejemplar = json.load(f)
                resultado['ejemplares'].append(ejemplar)

    return resultado


def busqueda_recursiva_texto(texto_busqueda, directorio=None):
    """
    Búsqueda recursiva por texto libre en todos los directorios.
    Busca coincidencias en título, autor o ISBN.

    Args:
        texto_busqueda (str): Texto a buscar
        directorio (Path, optional): Directorio donde buscar. Por defecto busca en data/libros

    Returns:
        list: Lista de libros que coinciden con la búsqueda
    """
    if directorio is None:
        directorio = obtener_directorio_libros()

    resultados = []
    texto_busqueda = texto_busqueda.lower()

    # Llamar función recursiva
    buscar_en_directorio_recursivo(directorio, texto_busqueda, resultados)

    return resultados


def buscar_en_directorio_recursivo(directorio, texto_busqueda, resultados):
    """
    Función recursiva que recorre directorios y archivos buscando coincidencias.

    Args:
        directorio (Path): Directorio actual
        texto_busqueda (str): Texto a buscar (en minúsculas)
        resultados (list): Lista donde se agregan los resultados (modificada por referencia)
    """
    try:
        # Listar contenido del directorio
        for item in directorio.iterdir():
            # Si es un directorio, llamada recursiva
            if item.is_dir():
                buscar_en_directorio_recursivo(item, texto_busqueda, resultados)

            # Si es un archivo JSON de libro
            elif item.is_file() and item.suffix == '.json' and item.name != 'indice_isbn.json':
                buscar_en_archivo(item, texto_busqueda, resultados)

    except PermissionError:
        # Ignorar directorios sin permisos
        pass


def buscar_en_archivo(ruta_archivo, texto_busqueda, resultados):
    """
    Busca coincidencias de texto en un archivo JSON de libro.

    Args:
        ruta_archivo (Path): Ruta del archivo a buscar
        texto_busqueda (str): Texto a buscar (en minúsculas)
        resultados (list): Lista donde se agregan los resultados
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            libro = json.load(f)

        # Verificar que sea un diccionario (no una lista)
        if not isinstance(libro, dict):
            return

        # Buscar en título, autor o ISBN
        if (texto_busqueda in libro.get('title', '').lower() or
            texto_busqueda in libro.get('autor', '').lower() or
            texto_busqueda in libro.get('isbn', '').lower()):

            resultados.append(libro)

    except (json.JSONDecodeError, KeyError, AttributeError):
        # Ignorar archivos con formato incorrecto
        pass


def buscar_por_genero(genero):
    """
    Busca todos los libros de un género específico.

    Args:
        genero (str): Nombre del género

    Returns:
        list: Lista de libros del género
    """
    genero_dir = obtener_directorio_libros() / genero
    if not genero_dir.exists():
        return []

    resultados = []
    for archivo in genero_dir.glob('*.json'):
        with open(archivo, 'r', encoding='utf-8') as f:
            libro = json.load(f)
            resultados.append(libro)

    return resultados


def listar_generos():
    """
    Lista todos los géneros disponibles.

    Returns:
        list: Lista de nombres de géneros ordenados
    """
    dir_libros = obtener_directorio_libros()
    generos = []

    for item in dir_libros.iterdir():
        if item.is_dir():
            generos.append(item.name)

    return sorted(generos)
