from negocio import libro_service as svc
from utils.consola import limpiar_consola, pausar

def ejecutar_menu_libros():
    while True:
        limpiar_consola()
        print("\n--- Gestión de Libros ---")
        print("1. Alta de libro")
        print("2. Modificar libro")
        print("3. Eliminar libro")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            isbn = input("ISBN: ").strip()
            genero = input("Género: ").strip()

            libro = svc.alta_libro(titulo, autor, isbn, genero)
            print("✅ Libro agregado correctamente:", libro)
            pausar()

        elif opcion == "2":
            genero = input("Género: ").strip()
            libro_id = input("ID del libro: ").strip()
            campo = input("Campo a modificar (title/autor/isbn/genero): ").strip()
            valor = input("Nuevo valor: ").strip()

            resultado = svc.modificar_libro(genero, libro_id, {campo: valor})
            if resultado:
                print("✅ Libro actualizado:", resultado)
            else:
                print("❌ No se encontró el libro.")
            pausar()

        elif opcion == "3":
            genero = input("Género: ").strip()
            libro_id = input("ID del libro: ").strip()
            ok = svc.eliminar_libro(genero, libro_id)
            print("✅ Libro eliminado." if ok else "❌ No se encontró el libro.")
            pausar()

        elif opcion == "0":
            break
