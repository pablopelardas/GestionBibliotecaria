"""
Servicio de usuarios.
Funciones para obtener información de usuarios.
"""

import json
from pathlib import Path


# Variable global para cachear usuarios en memoria
_usuarios_cache = None


def obtener_directorio_base():
    """Obtiene el directorio base del proyecto"""
    return Path(__file__).parent.parent


def cargar_usuarios():
    """
    Carga los usuarios desde usuarios.json.

    Returns:
        dict: Diccionario con user_id como clave y datos del usuario como valor
    """
    global _usuarios_cache

    if _usuarios_cache is None:
        base_dir = obtener_directorio_base()
        archivo_usuarios = base_dir / 'data' / 'usuarios' / 'usuarios.json'

        _usuarios_cache = {}

        with open(archivo_usuarios, 'r', encoding='utf-8') as f:
            usuarios = json.load(f)

        for usuario_data in usuarios:
            user_id = usuario_data['user_id']
            _usuarios_cache[user_id] = usuario_data['user']

    return _usuarios_cache


def obtener_nombre_usuario(user_id):
    """
    Obtiene el nombre de un usuario por su ID.

    Args:
        user_id (str): ID del usuario

    Returns:
        str: Nombre del usuario o el ID si no se encuentra
    """
    if user_id is None:
        return "N/A"

    try:
        usuarios = cargar_usuarios()
        if user_id in usuarios:
            return usuarios[user_id]['nombre']
        return user_id
    except:
        return user_id


def obtener_usuario_completo(user_id):
    """
    Obtiene toda la información de un usuario por su ID.

    Args:
        user_id (str): ID del usuario

    Returns:
        dict: Datos completos del usuario o None si no se encuentra
    """
    try:
        usuarios = cargar_usuarios()
        return usuarios.get(user_id, None)
    except:
        return None


def listar_usuarios() -> list[dict]:
    """
    Retorna la lista completa de usuarios.
    
    Retorno:
        list[dict]: lista de usuarios en formato diccionario
    """
    try:
        usuarios = cargar_usuarios()
        return [{"user_id": uid, "user": udata} for uid, udata in usuarios.items()]
    except Exception:
        return []


def agregar_usuario(datos: dict) -> bool:
    """
    Agrega un nuevo usuario al sistema.

    Args:
        datos (dict): Diccionario con los datos del usuario. 
                      Debe contener 'user_id' y 'user'.

    Returns:
        bool: True si se agregó correctamente, False en caso de error
    """
    try:
        global _usuarios_cache
        usuarios = cargar_usuarios()

        user_id = datos.get("user_id")
        user_data = datos.get("user")

        if not user_id or not user_data:
            return False 
        
        usuarios[user_id] = user_data

        base_dir = obtener_directorio_base()
        archivo_usuarios = base_dir / 'data' / 'usuarios' / 'usuarios.json'

        lista_usuarios = [{"user_id": uid, "user": udata} for uid, udata in usuarios.items()]

        with open(archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(lista_usuarios, f, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        return False


def modificar_usuario(user_id: str, datos: dict) -> bool:
    """
    Modifica un usuario existente en el sistema.

    Args:
        user_id (str): ID del usuario a modificar.
        datos (dict): Diccionario con los nuevos datos del usuario.

    Returns:
        bool: True si se modificó correctamente, False si no se encontró o hubo error.
    """
    try:
        global _usuarios_cache
        usuarios = cargar_usuarios()

        if user_id not in usuarios:
            return False

        usuarios[user_id].update(datos)

        base_dir = obtener_directorio_base()
        archivo_usuarios = base_dir / 'data' / 'usuarios' / 'usuarios.json'

        lista_usuarios = [{"user_id": uid, "user": udata} for uid, udata in usuarios.items()]

        with open(archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(lista_usuarios, f, ensure_ascii=False, indent=4)

        return True
    except Exception:
        return False


def eliminar_usuario(user_id: str) -> bool:
    """
    Elimina un usuario del sistema.

    Args:
        user_id (str): ID del usuario a eliminar.

    Returns:
        bool: True si se eliminó correctamente, False si no existe o hubo error.
    """
    try:
        global _usuarios_cache
        usuarios = cargar_usuarios()

        if user_id not in usuarios:
            return False

        usuarios.pop(user_id)

        base_dir = obtener_directorio_base()
        archivo_usuarios = base_dir / 'data' / 'usuarios' / 'usuarios.json'

        lista_usuarios = [{"user_id": uid, "user": udata} for uid, udata in usuarios.items()]

        with open(archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(lista_usuarios, f, ensure_ascii=False, indent=4)

        return True
    except Exception:
        return False