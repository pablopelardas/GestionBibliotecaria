def input_numero(mensaje, minimo=None, maximo=None):
    """
    Solicita al usuario un número válido por consola.
    
    :param mensaje: Texto a mostrar al usuario.
    :param minimo: Valor mínimo aceptado (opcional).
    :param maximo: Valor máximo aceptado (opcional).
    :return: Número entero validado.
    """
    while True:
        valor = input(mensaje).strip()
        if not valor.isdigit():
            print("Error: Debe ingresar un número válido.")
            continue

        numero = int(valor)

        if minimo is not None and numero < minimo:
            print(f"Error: El número debe ser mayor o igual a {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            print(f"Error: El número debe ser menor o igual a {maximo}.")
            continue

        return numero
