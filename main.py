from presentation.menu import menu_principal
from negocio.buscador_service import reconstruir_indice_isbn

def main():
    # Reconstruir índice al inicio para garantizar sincronización
    reconstruir_indice_isbn()
    print()  # Línea en blanco para separar del menú

    # Iniciar el menú principal
    menu_principal()

if __name__ == "__main__":
    main()