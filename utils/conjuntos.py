"""
Funciones que utilizan conjuntos (set) para listar los géneros disponibles y los autores
"""

def obtener_generos_unicos(lista_libros):
    """
    Retorna un conjunto con todos los géneros presentes en la lista de libros.
    Uso de conjuntos para evitar duplicados automáticamente.
    """
    generos = set()

    for libro in lista_libros:
        generos.add(libro.get("genero", ""))

    return generos

def obtener_autores_unicos(lista_libros):
    """
    Retorna un conjunto con los autores presentes en la biblioteca.
    """
    autores = set()
    for libro in lista_libros:
        autores.add(libro.get("autor", ""))
    return autores