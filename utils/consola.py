"""
Utilidades para manejo de consola.
"""

import os
import platform


def limpiar_consola():
    """
    Limpia la consola según el sistema operativo.
    """
    # Windows
    if platform.system() == "Windows":
        os.system('cls')
    # Linux, Mac, Unix
    else:
        os.system('clear')


def pausar():
    """
    Pausa la ejecución hasta que el usuario presione Enter.
    """
    input("\nPresione Enter para continuar...")
