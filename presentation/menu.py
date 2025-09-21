# main.py
import sys
from utils.input import input_numero

def menu_principal():
    while True:
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
            menu_usuarios()
        elif opcion == 2:
            menu_libros()
        elif opcion == 3:
            menu_prestamos()
        elif opcion == 4:
            menu_reportes()
        elif opcion == 0:
            print("¡Hasta pronto!")
            sys.exit()


def menu_usuarios():
    while True:
        print("\n--- Gestión de Usuarios ---")
        print("1. Alta de usuario")
        print("2. Modificar usuario")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=4)

        if opcion == 1:
            print("👉 Aquí iría la lógica de alta de usuario")
        elif opcion == 2:
            print("👉 Aquí iría la lógica de modificar usuario")
        elif opcion == 3:
            print("👉 Aquí iría la lógica de eliminar usuario")
        elif opcion == 4:
            print("👉 Aquí iría la lógica de listar usuarios")
        elif opcion == 0:
            return

def menu_libros():
    while True:
        print("\n--- Gestión de Libros ---")
        print("1. Alta de libro")
        print("2. Modificar libro")
        print("3. Eliminar libro")
        print("4. Listar libros")
        print("5. Buscar libro")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=5)

        if opcion == 1:
            print("👉 Aquí iría la lógica de alta de libro")
        elif opcion == 2:
            print("👉 Aquí iría la lógica de modificar libro")
        elif opcion == 3:
            print("👉 Aquí iría la lógica de eliminar libro")
        elif opcion == 4:
            print("👉 Aquí iría la lógica de listar libros")
        elif opcion == "5":
            print("👉 Aquí iría la lógica de búsqueda de libro")
        elif opcion == 0:
            return


def menu_prestamos():
    while True:
        print("\n--- Gestión de Préstamos ---")
        print("1. Registrar préstamo")
        print("2. Registrar devolución")
        print("3. Listar préstamos vigentes")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=3)

        if opcion == 1:
            print("👉 Aquí iría la lógica de registrar préstamo")
        elif opcion == 2:
            print("👉 Aquí iría la lógica de registrar devolución")
        elif opcion == 3:
            print("👉 Aquí iría la lógica de listar préstamos")
        elif opcion == 0:
            return


def menu_reportes():
    while True:
        print("\n--- Reportes y Búsquedas ---")
        print("1. Libros más prestados")
        print("2. Usuarios con más préstamos")
        print("3. Búsqueda por ISBN")
        print("4. Búsqueda por texto libre")
        print("0. Volver al menú principal")

        opcion = input_numero("Seleccione una opción: ", minimo=0, maximo=4)

        if opcion == 1:
            print("👉 Aquí iría la lógica de reporte de libros más prestados")
        elif opcion == 2:
            print("👉 Aquí iría la lógica de usuarios con más préstamos")
        elif opcion == 3:
            print("👉 Aquí iría la búsqueda binaria por ISBN")
        elif opcion == 4:
            print("👉 Aquí iría la búsqueda de texto libre")
        elif opcion == 0:
            return


if __name__ == "__main__":
    menu_principal()
