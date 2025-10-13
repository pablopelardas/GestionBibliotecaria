"""
Utilidad para mostrar resultados paginados de manera genérica.
"""

from utils.consola import limpiar_consola, pausar
from utils.input import input_numero


def mostrar_resultados_paginados(resultados, funcion_mostrar_item, titulo="Resultados", por_pagina=15):
    """
    Muestra resultados con paginación de manera genérica.

    Args:
        resultados (list): Lista de elementos a mostrar
        funcion_mostrar_item (function): Función que recibe (item, numero) y lo imprime
        titulo (str): Título para mostrar en cada página
        por_pagina (int): Cantidad de resultados por página

    Ejemplo de uso:
        def mostrar_libro(libro, numero):
            print(f"{numero}. {libro['title']}")
            print(f"   Autor: {libro['autor']}")

        mostrar_resultados_paginados(libros, mostrar_libro, "Libros de Ficción")
    """
    if not resultados:
        print("No hay resultados para mostrar")
        return

    pagina_actual = 0
    total_paginas = (len(resultados) + por_pagina - 1) // por_pagina

    while True:
        limpiar_consola()

        # Calcular rango de resultados para esta página
        inicio = pagina_actual * por_pagina
        fin = min(inicio + por_pagina, len(resultados))

        # Mostrar encabezado
        print(f"\n{'='*60}")
        print(f"{titulo}")
        print(f"{'='*60}")
        print(f"Página {pagina_actual + 1} de {total_paginas}")
        print(f"Mostrando registros {inicio + 1} al {fin} de {len(resultados)} total")
        print(f"{'='*60}")

        # Mostrar resultados de la página actual
        for i in range(inicio, fin):
            funcion_mostrar_item(resultados[i], i + 1)
            print()  # Línea en blanco entre items

        # Mostrar opciones de navegación
        print(f"{'-'*60}")
        print("Opciones:")

        if pagina_actual > 0:
            print("  [A] Página anterior")

        if pagina_actual < total_paginas - 1:
            print("  [S] Página siguiente")

        if total_paginas > 1:
            print(f"  [1-{total_paginas}] Ir a página específica")

        print("  [0] Volver")

        # Obtener opción del usuario
        opcion = input("\nSeleccione una opción: ").strip().lower()

        if opcion == 'a' and pagina_actual > 0:
            pagina_actual -= 1
        elif opcion == 's' and pagina_actual < total_paginas - 1:
            pagina_actual += 1
        elif opcion == '0':
            break
        elif opcion.isdigit():
            # Ir a página específica
            numero_pagina = int(opcion)
            if 1 <= numero_pagina <= total_paginas:
                pagina_actual = numero_pagina - 1
            else:
                print(f"❌ Número de página inválido. Debe estar entre 1 y {total_paginas}")
                pausar()
        else:
            print("❌ Opción inválida")
            pausar()


def mostrar_item_libro(libro, numero):
    """
    Función helper para mostrar un libro en formato de lista.

    Args:
        libro (dict): Diccionario con datos del libro
        numero (int): Número del item en la lista
    """
    estado = "✓ Disponible" if libro['disponible'] else "✗ Prestado"
    print(f"{numero}. {libro['title']}")
    print(f"   Autor: {libro['autor']}")
    print(f"   ISBN: {libro['isbn']}")
    print(f"   Género: {libro['genero']}")
    print(f"   Estado: {estado}")


def mostrar_item_usuario(usuario, numero):
    """
    Función helper para mostrar un usuario en formato de lista.

    Args:
        usuario (dict): Diccionario con datos del usuario
        numero (int): Número del item en la lista
    """
    print(f"{numero}. {usuario['nombre']}")
    print(f"   ID: {usuario['user_id']}")
    print(f"   Libros prestados: {len(usuario.get('libros_prestados', []))}")


def mostrar_item_prestamo(prestamo, numero):
    """
    Función helper para mostrar un préstamo en formato de lista.

    Args:
        prestamo (dict): Diccionario con datos del préstamo
        numero (int): Número del item en la lista
    """
    estado = "✓ Devuelto" if prestamo.get('regresado', False) else "✗ Activo"
    print(f"{numero}. Préstamo #{prestamo.get('prestamo_numero', 'N/A')}")
    print(f"   Usuario: {prestamo.get('user_id', 'N/A')}")
    print(f"   Libro: {prestamo.get('libro_id', 'N/A')}")
    print(f"   Estado: {estado}")
