from negocio.usuario_service import (
    agregar_usuario,
    modificar_usuario,
    eliminar_usuario,
    listar_usuarios
)
from utils.consola import limpiar_consola, pausar
import uuid


def input_texto(prompt: str, obligatorio=True) -> str:
    while True:
        valor = input(prompt).strip()
        if obligatorio and not valor:
            print("❌ Este campo no puede estar vacío.")
        else:
            return valor


def input_libros(prompt: str) -> list[str]:
    valor = input(prompt).strip()
    if not valor:
        return []
    return [l.strip() for l in valor.split(",")]


def input_user_id(prompt: str) -> str:
    while True:
        user_id = input(prompt).strip()
        if not user_id:
            print("❌ El ID no puede estar vacío.")
        else:
            return user_id


def generar_user_id() -> str:
    """Genera un ID único similar a 3B8E51C86508430994FA91F6B6"""
    return uuid.uuid4().hex.upper()


def input_nombre(prompt: str) -> str:
    """Pide un nombre solo con letras y espacios y mínimo 3 caracteres"""
    while True:
        valor = input(prompt).strip()

        if not valor:
            print("❌ El nombre no puede estar vacío.")
        elif len(valor.replace(" ", "")) < 3:  # Contar solo letras reales
            print("❌ El nombre debe tener al menos 3 letras.")
        elif not all(c.isalpha() or c.isspace() for c in valor):
            print("❌ El nombre solo puede contener letras y espacios.")
        else:
            return valor


def ejecutar_agregar_usuario():
    """Alta de usuario con ID automático y libros prestados vacíos"""
    limpiar_consola()
    print("--- Agregar Usuario ---")

    usuarios = listar_usuarios()
    while True:
        user_id = generar_user_id()
        if not any(u['user_id'] == user_id for u in usuarios):
            break

    nombre = input_nombre("Ingrese el nombre del usuario: ")

    datos = {
        "user_id": user_id,
        "user": {
            "nombre": nombre,
            "libros_prestados": []  
        }
    }

    if agregar_usuario(datos):
        print(f"✅ Usuario agregado correctamente. ID generado: {user_id}")
    else:
        print("❌ Error al agregar usuario.")


def ejecutar_modificar_usuario():
    """Modificar usuario con validación de nombre y sin cambiar libros"""
    limpiar_consola()
    print("--- Modificar Usuario ---")
    usuarios = listar_usuarios()
    if not usuarios:
        print("❌ No hay usuarios registrados.")
        return

    user_id = input_user_id("Ingrese el ID del usuario a modificar: ")
    if not any(u['user_id'] == user_id for u in usuarios):
        print("❌ No se encontró el usuario.")
        return

    nombre = input_nombre("Ingrese nuevo nombre: ")

    if not nombre:
        print("❌ No se ingresaron cambios.")
        return

    cambios = {"nombre": nombre}

    if modificar_usuario(user_id, cambios):
        print("✅ Usuario modificado correctamente.")
    else:
        print("❌ Error al modificar usuario.")


def ejecutar_eliminar_usuario():
    """Eliminar usuario con validaciones"""
    limpiar_consola()
    print("--- Eliminar Usuario ---")
    usuarios = listar_usuarios()
    if not usuarios:
        print("❌ No hay usuarios registrados.")
        return

    user_id = input_user_id("Ingrese el ID del usuario a eliminar: ")
    if not any(u['user_id'] == user_id for u in usuarios):
        print("❌ No se encontró el usuario.")
        return

    if eliminar_usuario(user_id):
        print("✅ Usuario eliminado correctamente.")
    else:
        print("❌ Error al eliminar usuario.")


def ejecutar_listar_usuarios():
    """Listar usuarios"""
    limpiar_consola()
    print("--- Lista de Usuarios ---")
    usuarios = listar_usuarios()
    if not usuarios:
        print("❌ No hay usuarios registrados.")
        return

    for u in usuarios:
        print(f"ID: {u['user_id']} - Nombre: {u['user']['nombre']} - Libros prestados: {len(u['user']['libros_prestados'])}")