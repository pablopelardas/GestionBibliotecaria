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
