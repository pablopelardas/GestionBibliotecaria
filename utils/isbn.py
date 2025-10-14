"""
Utilidades para manejo de ISBNs.
"""


def normalizar_isbn(isbn):
    """
    Normaliza un ISBN eliminando guiones, espacios y convirtiendo a mayúsculas.
    Esto permite comparar ISBNs independientemente de su formato.

    Ejemplos:
        "978-6-3130-1103-2" -> "9786313011032"
        "978 6 3130 1103 2" -> "9786313011032"
        "9786313011032" -> "9786313011032"

    Args:
        isbn (str): ISBN en cualquier formato

    Returns:
        str: ISBN normalizado (solo números y letras, sin guiones ni espacios)
    """
    if not isbn:
        return ""

    # Eliminar guiones, espacios y convertir a mayúsculas
    isbn_normalizado = isbn.replace("-", "").replace(" ", "").upper()
    return isbn_normalizado
