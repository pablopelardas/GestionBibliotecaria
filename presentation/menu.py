# main.py
import sys
from utils.input import input_numero
from utils.consola import limpiar_consola, pausar
from presentation.busquedas import (
    ejecutar_busqueda_isbn,
    ejecutar_busqueda_texto,
    ejecutar_busqueda_genero
)
from presentation.usuarios import (
    ejecutar_agregar_usuario,
    ejecutar_modificar_usuario,
    ejecutar_eliminar_usuario,
    ejecutar_listar_usuarios
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
        print("5. Buscar libro")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=5)

        if opcion == 1:
            limpiar_consola()
            print("👉 Aquí iría la lógica de alta de libro")
            pausar()
        elif opcion == 2:
            limpiar_consola()
            print("👉 Aquí iría la lógica de modificar libro")
            pausar()
        elif opcion == 3:
            limpiar_consola()
            print("👉 Aquí iría la lógica de eliminar libro")
            pausar()
        elif opcion == 4:
            limpiar_consola()
            print("👉 Aquí iría la lógica de listar libros")
            pausar()
        elif opcion == 5:
            limpiar_consola()
            print("👉 Aquí iría la lógica de búsqueda de libro")
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
            print("👉 Aquí iría la lógica de registrar préstamo")
            pausar()
        elif opcion == 2:
            limpiar_consola()
            print("👉 Aquí iría la lógica de registrar devolución")
            pausar()
        elif opcion == 3:
            limpiar_consola()
            print("👉 Aquí iría la lógica de listar préstamos")
            pausar()
        elif opcion == 0:
            return


def menu_reportes():
    while True:
        limpiar_consola()
        print("\n--- Reportes y Búsquedas ---")
        print("1. Libros más prestados")
        print("2. Usuarios con más préstamos")
        print("3. Búsqueda por ISBN")
        print("4. Búsqueda por texto libre")
        print("5. Búsqueda por género")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=5)

        if opcion == 1:
            limpiar_consola()
            print("👉 Aquí iría la lógica de reporte de libros más prestados")
            pausar()
        elif opcion == 2:
            limpiar_consola()
            print("👉 Aquí iría la lógica de usuarios con más préstamos")
            pausar()
        elif opcion == 3:
            limpiar_consola()
            ejecutar_busqueda_isbn()
            pausar()
        elif opcion == 4:
            limpiar_consola()
            ejecutar_busqueda_texto()
            pausar()
        elif opcion == 5:
            limpiar_consola()
            ejecutar_busqueda_genero()
        elif opcion == 0:
            return


if __name__ == "__main__":
    menu_principal()
