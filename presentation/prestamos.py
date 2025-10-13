from utils.consola import pausar, limpiar_consola
from utils.input import input_numero
from negocio import prestamos_service as svc
from negocio.buscador_service import busqueda_binaria_isbn
from negocio.usuario_service import obtener_nombre_usuario, obtener_usuario_completo


def _mostrar_item_ejemplar_disponible(ejemplar, numero, disponible):
    estado = "✓ Disponible" if disponible else "✗ Prestado"
    print(f"  [{numero}]. ID: {ejemplar['libro_id']}")
    
    nombre_prestado = "N/A"
    if 'prestamo_actual' in ejemplar and ejemplar['prestamo_actual']:
        nombre_prestado = obtener_nombre_usuario(ejemplar['prestamo_actual'])
    
    if disponible:
        print(f"         {estado}")
    else:
        print(f"         {estado} - Prestado a: {nombre_prestado}")
        

def _mostrar_item_prestamo_activo(prestamo, numero):
    """Muestra la información esencial de un préstamo activo para devolución."""
    nombre_usuario = obtener_nombre_usuario(prestamo['user_id'])
    print(f"  [{numero}]. Título: {prestamo['title']} (Género: {prestamo['genero'].capitalize()})")
    print(f"         ID Libro: {prestamo['libro_id']} | Prestado a: {nombre_usuario}")


def ejecutar_registrar_prestamo():
    limpiar_consola()
    print("=== Registrar préstamo por ISBN ===")
    
    # 1. Solicitar ID de Usuario y validar existencia
    user_id = input("ID de usuario: ").strip().upper()
    user_data = obtener_usuario_completo(user_id)
    if user_data is None:
        print("❌ Error: No se encontró el usuario con el ID proporcionado.")
        pausar()
        return
    
    nombre_usuario = obtener_nombre_usuario(user_id)
        
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
             print("\nEjemplares prestados actualmente:")
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
    
    print(f"\nIntentando prestar el libro ID {libro_id} ('{resultado_busqueda['title']}') al usuario {nombre_usuario}...")
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
    limpiar_consola()
    print("=== Registrar Devolución  ===")

    user_id = input("Ingrese el ID del usuario: ").strip().upper()
    user_data = obtener_usuario_completo(user_id)
    if user_data is None:
        print("❌ Error: No se encontró el usuario con el ID proporcionado.")
        pausar()
        return

    prestamos_activos = svc.obtener_prestamos_activos_usuario_con_info(user_id)

    if not prestamos_activos:
        nombre_usuario = obtener_nombre_usuario(user_id)
        print(f"✅ El usuario '{nombre_usuario}' no tiene préstamos activos para devolver.")
        pausar()
        return

    nombre_usuario = obtener_nombre_usuario(user_id)
    print(f"\n--- Préstamos activos de {nombre_usuario} ({user_id}) ---")
    
    for i, prestamo in enumerate(prestamos_activos, 1):
        _mostrar_item_prestamo_activo(prestamo, i)

    if len(prestamos_activos) == 1:
        seleccion = 1
        print("\nSelección automática: Se devolverá el único préstamo activo encontrado.")
    else:
        seleccion = input_numero("\nSeleccione el número del libro a devolver: ", minimo=1, maximo=len(prestamos_activos))

    prestamo_a_devolver = prestamos_activos[seleccion - 1]
    libro_id = prestamo_a_devolver['libro_id']
    
    print(f"\nConfirmando devolución para '{prestamo_a_devolver['title']}' (ID: {libro_id})...")

    try:
        # La función de negocio registrar_devolucion ahora recibe el genero y libro_id
        ok = svc.registrar_devolucion(genero, libro_id) 
        if ok:
            print(f"✅ Devolución de '{prestamo_a_devolver['title']}' registrada correctamente.")
        else:
            print("❌ No se pudo registrar la devolución (el préstamo ya estaba cerrado o hubo un error de archivo).")
    except Exception as e:
        print(f"❌ Error interno al registrar la devolución: {e}")
    pausar()


def ejecutar_listar_prestamos_vigentes():
    limpiar_consola()
    print("=== Préstamos vigentes ===")
    try:
        prestamos = svc.obtener_prestamos_activos()      
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    if not prestamos:
        print("No hay préstamos activos.")
        pausar()
        return

    for p in prestamos:
        libro_id = p.get("libro_id", "¿?")
        user_id = p.get("user_id", "¿?")
        f_prestamo = p.get("fecha_prestamo", "s/f")
        f_venc = p.get("fecha_vencimiento", "s/f")
        nombre_usuario = obtener_nombre_usuario(user_id)
        # Mostrar solo la información esencial
        print(f"- Libro ID: {libro_id} | Usuario: {nombre_usuario} (ID: {user_id}) | Prestado: {f_prestamo}")
    pausar()
