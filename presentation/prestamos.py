from utils.consola import pausar
from utils.input import input_numero
from negocio import prestamos_service as svc


def ejecutar_registrar_prestamo():
    print("=== Registrar préstamo ===")
    user_id = input("ID de usuario: ").strip()
    libro_id = input("ID del libro: ").strip()
    genero = input("Género del libro: ")

    try:
        ok = svc.registrar_prestamo(genero, libro_id, user_id) 
        if ok:
            print("✅ Préstamo registrado correctamente.")
        else:
            print("❌ No se pudo registrar el préstamo (verifique libro/usuario).")
    except Exception as e:
        print(f"❌ Error: {e}")


def ejecutar_registrar_devolucion():
    print("=== Registrar devolución ===")
    libro_id = input("ID del libro: ").strip()

    try:
        ok = svc.registrar_devolucion(libro_id)         
        if ok:
            print("✅ Devolución registrada correctamente.")
        else:
            print("❌ No se pudo registrar la devolución (verifique el libro/prestamo activo).")
    except Exception as e:
        print(f"❌ Error: {e}")


def ejecutar_listar_prestamos_vigentes():
    print("=== Préstamos vigentes ===")
    try:
        prestamos = svc.obtener_prestamos_activos()      
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    if not prestamos:
        print("No hay préstamos activos.")
        return

    for p in prestamos:
        libro_id = p.get("libro_id", "¿?")
        user_id = p.get("user_id", "¿?")
        f_prestamo = p.get("fecha_prestamo", "s/f")
        f_venc = p.get("fecha_vencimiento", "s/f")
        print(f"- Libro: {libro_id} | Usuario: {user_id} | Prestado: {f_prestamo} | Vence: {f_venc}")

