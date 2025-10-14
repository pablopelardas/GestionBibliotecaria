"""
Funciones de presentación para el módulo de libros.
Maneja la interacción con el usuario para las diferentes opciones.
"""

from utils.consola import limpiar_consola, pausar
from negocio.libro_service import (
    agregar_libro,
    modificar_libro,
    eliminar_libro,
    listar_libros
)
from negocio.buscador_service import busqueda_binaria_isbn

# ALTA DE LIBRO
def ejecutar_agregar_libro():
    """Ejecuta agregar libro"""
    print("\n--- Alta de libro ---")

    isbn = input("Ingrese el ISBN: ").strip()

    #Chequeamos si ya existe el ISBN
    libro_existente = busqueda_binaria_isbn(isbn)

    if libro_existente:
        # Ya existe asi que agregamos un nuevo ejemplar automáticamente
        libro_id = agregar_libro({
            "isbn": isbn,
            "title": libro_existente["title"],
            "autor": libro_existente["autor"],
            "genero": libro_existente["genero"]
        })
        print(f"\nEl ISBN ya existe → nuevo ejemplar agregado con ID: {libro_id}")

    else:
        #No existe asi que pedimos datos del nuevo libro
        datos = {
            "isbn": isbn,
            "title": input("Ingrese el título: ").strip(),
            "autor": input("Ingrese el autor: ").strip(),
            "genero": input("Ingrese el género: ").strip().lower()
        }

        libro_id = agregar_libro(datos)
        print(f"\nNuevo libro agregado correctamente con ID: {libro_id}")

# MODIFICAR LIBRO
def ejecutar_modificar_libro():
    """Ejecuta modificar libro"""
    print("\n--- Modificar libro ---")

    libro_id = input("Ingrese el ID del libro que desea modificar: ")
    
    nuevos_datos = {}
    
    nuevo_titulo = input("Nuevo título (deje vacío para mantener el actual): ")
    if nuevo_titulo.strip() != "":
        nuevos_datos["title"] = nuevo_titulo

    nuevo_autor = input("Nuevo autor (deje vacío para mantener el actual): ")
    if nuevo_autor.strip() != "":
        nuevos_datos["autor"] = nuevo_autor

    if modificar_libro(libro_id, nuevos_datos):
        print("\n✅ Libro modificado correctamente.")
    else:
        print("\n❌ No se encontró el libro con el ID ingresado.")

# ELIMINAR LIBRO
def ejecutar_eliminar_libro():
    """Ejecuta eliminar libro"""
    print("\n--- Eliminar libro ---")

    libro_id = input("Ingrese el ID del libro que desea eliminar: ")

    if eliminar_libro(libro_id):
        print("\n✅ Libro eliminado correctamente.")
    else:
        print("\n❌ No se encontró el libro con el ID ingresado.")

# LISTAR LIBROS
def ejecutar_listar_libros():
    """Ejecuta el listado de libros y muestra los resultados"""
    print("\n---📚 Listado de libros 📚---")

    libros = listar_libros()

    if not libros:
        print("❌ No hay libros registrados.")
    else:
        for libro in libros:
            print(f"- {libro['title']} - {libro['autor']} | {libro['genero']}")

    pausar()