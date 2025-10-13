from utils.consola import pausar, limpiar_consola
from utils.input import input_numero
from negocio import prestamos_service as svc
from negocio.buscador_service import busqueda_binaria_isbn
from negocio.usuario_service import obtener_nombre_usuario, obtener_usuario_completo


def _mostrar_item_ejemplar_disponible(ejemplar, numero, disponible):
    estado = "✓ Disponible" if disponible else "✗ Prestado"
    print(f"  [{numero}]. ID: {ejemplar['libro_id']}")
    if 'prestamo_actual' in ejemplar and ejemplar['prestamo_actual']:
        nombre_prestado = obtener_nombre_usuario(ejemplar['prestamo_actual'])
        print(f"         {estado} - Prestado a: {nombre_prestado}")
    else:
        print(f"         {estado}")

def ejecutar_registrar_prestamo():
    limpiar_consola()
    print("=== Registrar préstamo ===")
    
    user_id = input("ID de usuario: ").strip().upper()
    if obtener_usuario_completo(user_id) is None:
        print("❌ Error: No se encontró el usuario con el ID proporcionado.")
        pausar()
        return
 
    isbn = input("ISBN del libro: ").strip()
    resultado_busqueda = busqueda_binaria_isbn(isbn)

    if not resultado_busqueda:
        print(f"❌ No se encontró ningún libro con ISBN: {isbn}")
        pausar()
        return
    ejemplares_disponibles = [
        ejemplar for ejemplar in resultado_busqueda['ejemplares'] if ejemplar.get('disponible', False)
    ]
    
    if not ejemplares_disponibles:
        print(f"❌ El libro '{resultado_busqueda['title']}' no tiene ejemplares disponibles para préstamo.")
        ejemplares_prestados = [
             ejemplar for ejemplar in resultado_busqueda['ejemplares'] if not ejemplar.get('disponible', True)
        ]
        if ejemplares_prestados:
             print("\nEjemplares prestados:")
             for i, ejemplar in enumerate(ejemplares_prestados, 1):
                _mostrar_item_ejemplar_disponible(ejemplar, i, False)
        pausar()
        return

    print(f"\n--- Ejemplares disponibles para '{resultado_busqueda['title']}' (Género: {resultado_busqueda['genero']}) ---")
    
    for i, ejemplar in enumerate(ejemplares_disponibles, 1):
        _mostrar_item_ejemplar_disponible(ejemplar, i, True)

    if len(ejemplares_disponibles) == 1:
        seleccion = 1
        print("\nSelección automática: Se tomará el único ejemplar disponible.")
    else:
        seleccion = input_numero("\nSeleccione el número del ejemplar a prestar: ", minimo=1, maximo=len(ejemplares_disponibles))

    ejemplar_seleccionado = ejemplares_disponibles[seleccion - 1]
    libro_id = ejemplar_seleccionado['libro_id']
    genero = resultado_busqueda['genero']
    
    nombre_usuario = obtener_nombre_usuario(user_id)
    print(f"\nIntentando prestar el libro ID {libro_id} al usuario {nombre_usuario}...")

    try:
        ok = svc.registrar_prestamo(genero, libro_id, user_id) 
        if ok:
            print("✅ Préstamo registrado correctamente.")
        else:
            print("❌ No se pudo registrar el préstamo (error de disponibilidad o lógica de negocio).")
    except Exception as e:
        print(f"❌ Error interno al registrar el préstamo: {e}")
    pausar()


def ejecutar_registrar_devolucion():
    print("=== Registrar devolución ===")
    libro_id = input("ID del libro: ").strip()

    try:
        print("❌ La función de devolución requiere el género o una modificación en negocio/prestamos_service.py")
        pausar()
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
