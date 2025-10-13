"""
Funciones de presentación para el módulo de búsquedas.
Maneja la interacción con el usuario para las diferentes búsquedas.
"""

from utils.consola import limpiar_consola, pausar
from utils.paginacion import mostrar_resultados_paginados, mostrar_item_libro
from negocio.buscador_service import (
    busqueda_binaria_isbn,
    busqueda_recursiva_texto,
    buscar_por_genero,
    listar_generos,
    buscar_por_libro_id
)
from negocio.usuario_service import obtener_nombre_usuario
from utils.input import input_numero


def ejecutar_busqueda_isbn():
    """Ejecuta búsqueda binaria por ISBN"""
    print("\n=== Búsqueda por ISBN ===")
    isbn = input("Ingrese el ISBN a buscar: ").strip()

    if not isbn:
        print("❌ Debe ingresar un ISBN")
        return

    resultado = busqueda_binaria_isbn(isbn)

    if resultado:
        print(f"\n✓ Libro encontrado:")
        print(f"  ISBN: {resultado['isbn']}")
        print(f"  Título: {resultado['title']}")
        print(f"  Autor: {resultado['autor']}")
        print(f"  Género: {resultado['genero']}")
        print(f"  Total ejemplares: {len(resultado['ejemplares'])}")

        # Mostrar estado de ejemplares
        disponibles = sum(1 for e in resultado['ejemplares'] if e['disponible'])
        prestados = len(resultado['ejemplares']) - disponibles

        print(f"\n  Disponibilidad:")
        print(f"    Disponibles: {disponibles}")
        print(f"    Prestados: {prestados}")

        # Preguntar si quiere ver detalles
        ver_detalles = input("\n¿Desea ver detalles de los ejemplares? (s/n): ").strip().lower()
        if ver_detalles == 's':
            for i, ejemplar in enumerate(resultado['ejemplares'], 1):
                print(f"\n  Ejemplar {i}:")
                print(f"    ID: {ejemplar['libro_id']}")
                print(f"    Disponible: {'Sí' if ejemplar['disponible'] else 'No'}")
                if not ejemplar['disponible']:
                    nombre_usuario = obtener_nombre_usuario(ejemplar['prestamo_actual'])
                    print(f"    Prestado a: {nombre_usuario} ({ejemplar['prestamo_actual']})")
                print(f"    Préstamos históricos: {len(ejemplar['historial_prestamos'])}")
    else:
        print(f"\n❌ No se encontró ningún libro con ISBN: {isbn}")


def ejecutar_busqueda_texto():
    """Ejecuta búsqueda recursiva por texto libre"""
    print("\n=== Búsqueda por Texto Libre ===")
    print("Busca en título, autor o ISBN")
    texto = input("Ingrese el texto a buscar: ").strip()

    if not texto:
        print("❌ Debe ingresar un texto")
        return

    print(f"\nBuscando '{texto}'...")
    resultados = busqueda_recursiva_texto(texto)

    if resultados:
        print(f"\n✓ Se encontraron {len(resultados)} coincidencias")

        # Si hay pocos resultados, mostrar todos
        if len(resultados) <= 10:
            for i, libro in enumerate(resultados, 1):
                print(f"\n{i}. {libro['title']}")
                print(f"   Autor: {libro['autor']}")
                print(f"   ISBN: {libro['isbn']}")
                print(f"   Género: {libro['genero']}")
                print(f"   Disponible: {'Sí' if libro['disponible'] else 'No'}")
        else:
            # Si hay muchos, usar paginación
            ver_todos = input(f"\n¿Desea ver todos los resultados? (s/n): ").strip().lower()
            if ver_todos == 's':
                mostrar_resultados_paginados(resultados, mostrar_item_libro, "Resultados de Búsqueda", por_pagina=10)
            else:
                # Mostrar solo los primeros
                for i, libro in enumerate(resultados[:10], 1):
                    print(f"\n{i}. {libro['title']}")
                    print(f"   Autor: {libro['autor']}")
                    print(f"   ISBN: {libro['isbn']}")
                    print(f"   Género: {libro['genero']}")
                    print(f"   Disponible: {'Sí' if libro['disponible'] else 'No'}")
                print(f"\n... y {len(resultados) - 10} resultados más")
    else:
        print(f"\n❌ No se encontraron coincidencias para: '{texto}'")


def ejecutar_busqueda_genero():
    """Ejecuta búsqueda por género"""
    print("\n=== Búsqueda por Género ===")

    # Mostrar géneros disponibles
    generos = listar_generos()
    print("\nGéneros disponibles:")
    for i, genero in enumerate(generos, 1):
        print(f"  {i}. {genero.capitalize()}")

    # Seleccionar género
    opcion = input_numero("\nSeleccione un género (número): ", minimo=1, maximo=len(generos))
    genero_seleccionado = generos[opcion - 1]

    print(f"\nBuscando libros de '{genero_seleccionado}'...")
    resultados = buscar_por_genero(genero_seleccionado)

    if resultados:
        print(f"\n✓ Se encontraron {len(resultados)} libros de {genero_seleccionado}:")

        # Estadísticas
        disponibles = sum(1 for libro in resultados if libro['disponible'])
        prestados = len(resultados) - disponibles

        print(f"\nEstadísticas:")
        print(f"  Total: {len(resultados)}")
        print(f"  Disponibles: {disponibles}")
        print(f"  Prestados: {prestados}")

        # Mostrar lista con paginación
        ver_lista = input("\n¿Desea ver la lista de libros? (s/n): ").strip().lower()
        if ver_lista == 's':
            mostrar_resultados_paginados(resultados, mostrar_item_libro, f"Libros de {genero_seleccionado.capitalize()}")
    else:
        print(f"\n❌ No se encontraron libros del género: {genero_seleccionado}")


def ejecutar_busqueda_por_id():
    """Ejecuta búsqueda por ID de ejemplar"""
    print("\n=== Búsqueda por ID de Ejemplar ===")
    libro_id = input("Ingrese el ID del ejemplar a buscar: ").strip()

    if not libro_id:
        print("❌ Debe ingresar un ID")
        return

    print(f"\nBuscando ejemplar con ID '{libro_id}'...")
    resultado = buscar_por_libro_id(libro_id)

    if resultado:
        libro = resultado['libro']
        print(f"\n✓ Ejemplar encontrado:")
        print(f"  ID: {libro['libro_id']}")
        print(f"  ISBN: {resultado['isbn']}")
        print(f"  Título: {libro['title']}")
        print(f"  Autor: {libro['autor']}")
        print(f"  Género: {libro['genero']}")
        print(f"  Disponible: {'Sí' if libro['disponible'] else 'No'}")

        # Si está prestado, mostrar información
        if not libro['disponible']:
            nombre_usuario = obtener_nombre_usuario(libro['prestamo_actual'])
            print(f"  Prestado a: {nombre_usuario} ({libro['prestamo_actual']})")
            if 'fecha_prestamo' in libro:
                print(f"  Fecha de préstamo: {libro['fecha_prestamo']}")

        # Mostrar historial de préstamos
        if 'historial_prestamos' in libro and libro['historial_prestamos']:
            print(f"\n  Historial de préstamos: {len(libro['historial_prestamos'])} préstamos")
            ver_historial = input("\n¿Desea ver el historial completo? (s/n): ").strip().lower()
            if ver_historial == 's':
                for i, prestamo in enumerate(libro['historial_prestamos'], 1):
                    print(f"\n  Préstamo {i}:")
                    print(f"    Usuario: {prestamo.get('user_id', 'N/A')}")
                    print(f"    Fecha: {prestamo.get('fecha_prestamo', 'N/A')}")
                    if prestamo.get('fecha_devolucion'):
                        print(f"    Devolución: {prestamo['fecha_devolucion']}")
                    else:
                        print(f"    Devolución: Préstamo activo")

        # Mostrar ruta del archivo (útil para desarrolladores/administradores)
        mostrar_ruta = input("\n¿Desea ver la ubicación del archivo? (s/n): ").strip().lower()
        if mostrar_ruta == 's':
            print(f"\n  Archivo: {resultado['ruta']}")
    else:
        print(f"\n❌ No se encontró ningún ejemplar con ID: {libro_id}")
