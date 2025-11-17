# main.py
import sys
from utils.input import input_numero
from utils.consola import limpiar_consola, pausar
from utils.reportes import ReportGenerator
reportes = ReportGenerator()
from presentation.busquedas import (
    ejecutar_busqueda_isbn,
    ejecutar_busqueda_texto,
    ejecutar_busqueda_genero,
    ejecutar_busqueda_por_id
)
from presentation.usuarios import (
    ejecutar_agregar_usuario,
    ejecutar_modificar_usuario,
    ejecutar_eliminar_usuario,
    ejecutar_listar_usuarios
)
from presentation.libros import (
    ejecutar_agregar_libro,
    ejecutar_modificar_libro,
    ejecutar_eliminar_libro,
    ejecutar_listar_libros,
    ejecutar_listar_generos,
    ejecutar_listar_autores
)

from presentation.prestamos import (
    ejecutar_registrar_prestamo,
    ejecutar_registrar_devolucion,
    ejecutar_listar_prestamos_vigentes
)



def menu_principal():
    while True:
        limpiar_consola()
        print("\n==============================")
        print("   SISTEMA DE BIBLIOTECA")
        print("==============================")
        print("1. Gestión de Usuarios")
        print("2. Gestión de Libros")
        print("3. Préstamos y Devoluciones")
        print("4. Reportes y Búsquedas")
        print("0. Salir")
        print("==============================")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=4)

        if opcion == 1:
            limpiar_consola()
            menu_usuarios()
        elif opcion == 2:
            limpiar_consola()
            menu_libros()
        elif opcion == 3:
            limpiar_consola()
            menu_prestamos()
        elif opcion == 4:
            limpiar_consola()
            menu_reportes()
        elif opcion == 0:
            limpiar_consola()
            print("¡Hasta pronto!")
            sys.exit()


def menu_usuarios():
    while True:
        limpiar_consola()
        print("\n--- Gestión de Usuarios ---")
        print("1. Alta de usuario")
        print("2. Modificar usuario")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=4)

        if opcion == 1:
            limpiar_consola()
            ejecutar_agregar_usuario()
            pausar()
        elif opcion == 2:
            limpiar_consola()
            ejecutar_modificar_usuario()
            pausar()
        elif opcion == 3:
            limpiar_consola()
            ejecutar_eliminar_usuario()
            pausar()
        elif opcion == 4:
            limpiar_consola()
            ejecutar_listar_usuarios()
            pausar()
        elif opcion == 0:
            return

def menu_libros():
    while True:
        limpiar_consola()
        print("\n--- Gestión de Libros ---")
        print("1. Alta de libro")
        print("2. Modificar libro")
        print("3. Eliminar libro")
        print("4. Listar libros")
        print("5. Listar géneros")
        print("6. Listar autores")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=6)

        if opcion == 1:
            limpiar_consola()
            ejecutar_agregar_libro()
            pausar()
        elif opcion == 2:
            limpiar_consola()
            ejecutar_modificar_libro()
            pausar()
        elif opcion == 3:
            limpiar_consola()
            ejecutar_eliminar_libro()
            pausar()
        elif opcion == 4:
            limpiar_consola()
            ejecutar_listar_libros()
            pausar()
        elif opcion == 5:
            limpiar_consola()
            ejecutar_listar_generos()
            pausar()
        elif opcion == 6:
            limpiar_consola()
            ejecutar_listar_autores()
            pausar()
        elif opcion == 0:
            return


def menu_prestamos():
    while True:
        limpiar_consola()
        print("\n--- Gestión de Préstamos ---")
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("3. Listar préstamos vigentes")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=3)

        if opcion == 1:
            limpiar_consola()
            ejecutar_registrar_prestamo()
            pausar()
        elif opcion == 2:
            limpiar_consola()
            ejecutar_registrar_devolucion()
            pausar()
        elif opcion == 3:
            limpiar_consola()
            ejecutar_listar_prestamos_vigentes()
            pausar()
        elif opcion == 0:
            return


def menu_reportes():
    while True:
        limpiar_consola()
        print("\n--- Reportes y Búsquedas ---")
        print("1. Libros más prestados")
        print("2. Usuarios con más préstamos")
        print("3. Estadísticas por género (Matriz)")
        print("4. Búsqueda por ISBN")
        print("5. Búsqueda por texto libre")
        print("6. Búsqueda por género")
        print("7. Búsqueda por ID de ejemplar")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=7)

        if opcion == 1:
            limpiar_consola()
            reportes.report_most_borrowed_books()
            pausar()
        elif opcion == 2:
            limpiar_consola()
            reportes.report_top_users()
            pausar()
        elif opcion == 3:
            limpiar_consola()
            reportes.report_estadisticas_por_genero()
            pausar()
        elif opcion == 4:
            limpiar_consola()
            ejecutar_busqueda_isbn()
            pausar()
        elif opcion == 5:
            limpiar_consola()
            ejecutar_busqueda_texto()
            pausar()
        elif opcion == 6:
            limpiar_consola()
            ejecutar_busqueda_genero()
            pausar()
        elif opcion == 7:
            limpiar_consola()
            ejecutar_busqueda_por_id()
            pausar()
        elif opcion == 0:
            return


if __name__ == "__main__":
    menu_principal()
