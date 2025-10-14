"""
Servicio de libros.
Funciones para agregar, modificar, eliminar o listar libros.
"""
import json
import os
import uuid

# Carpeta base de todos los géneros
RUTA_BASE = os.path.join("data", "libros")


# Funciones AUXILIARES

def guardar_json(ruta, datos):
    """Guarda un archivo JSON en la ruta indicada."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def cargar_json(ruta):
    """Carga y devuelve los datos de un archivo JSON."""
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return None

def obtener_ruta_genero(genero):
    """Devuelve la ruta completa para un género determinado."""
    return os.path.join(RUTA_BASE, genero)


# Funciones PRINCIPALES

def agregar_libro(datos):
    """
    Agrega un nuevo libro o ejemplar a la biblioteca
    Si el ISBN ya existe en el índice, agrega el ejemplar a esa entrada.
    Si no existe, crea una nueva.
    
    Args:
        datos (dict): contiene 'isbn', 'title', 'autor' y 'genero'
    
    Returns:
        str: ID único del libro agregado
    """
    indice_path = os.path.join(RUTA_BASE, "indice_isbn.json")
    libros_path = os.path.join(RUTA_BASE, "libros.json")

    # Cargar índice de ISBN
    if os.path.exists(indice_path):
        with open(indice_path, "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)
    else:
        indice = []

    # Cargar listado general de libros (ejemplares)
    if os.path.exists(libros_path):
        with open(libros_path, "r", encoding="utf-8") as archivo:
            lista_libros = json.load(archivo)
    else:
        lista_libros = []

    isbn = datos["isbn"]
    genero = datos["genero"].lower()
    carpeta_genero = obtener_ruta_genero(genero)
    os.makedirs(carpeta_genero, exist_ok=True)

    # Crear archivo individual del ejemplar
    libro_id = str(uuid.uuid4())
    ruta_archivo = os.path.join(carpeta_genero, f"{libro_id}.json")

    ejemplar = {
        "libro_id": libro_id,
        "isbn": isbn,
        "title": datos["title"],
        "autor": datos["autor"],
        "genero": genero,
        "disponible": True,
        "prestamo_actual": None,
        "historial_prestamos": []
    }

    guardar_json(ruta_archivo, ejemplar)

    # Buscar si el ISBN ya existe en el índice
    libro_existente = None
    for libro in indice:
        if libro["isbn"] == isbn:
            libro_existente = libro
            break

    if libro_existente is not None:
        # Si ya existe → agregar ejemplar
        libro_existente["ejemplares"].append({
            "libro_id": libro_id,
            "disponible": True,
            "ruta": ruta_archivo
        })
    else:
        # Si no existe → crear nueva entrada
        nuevo_libro = {
            "isbn": isbn,
            "title": datos["title"],
            "autor": datos["autor"],
            "genero": genero,
            "ejemplares": [
                {
                    "libro_id": libro_id,
                    "disponible": True,
                    "ruta": ruta_archivo
                }
            ]
        }
        indice.append(nuevo_libro)

    # Agregar el ejemplar también al archivo libros.json
    lista_libros.append({
        "libro_id": libro_id,
        "libro": {
            "title": datos["title"],
            "autor": datos["autor"],
            "disponible": True
        }
    })

    # Guardar ambos archivos actualizados
    guardar_json(indice_path, indice)
    guardar_json(libros_path, lista_libros)

    return libro_id


def modificar_libro(libro_id, nuevos_datos):
    """
    Modifica un libro en todas las estructuras:
    - Actualiza el archivo individual del ejemplar
    - Actualiza libros.json
    - Actualiza los datos en indice_isbn.json

    Args:
        libro_id (str): ID del libro a modificar
        nuevos_datos (dict): datos a actualizar
    
    Returns:
        bool: True si se modificó correctamente, False si no se encontró
    """
    #Rutas
    indice_path = os.path.join(RUTA_BASE, "indice_isbn.json")
    libros_path = os.path.join(RUTA_BASE, "libros.json")

    #Cargar índices
    indice = cargar_json(indice_path) or []
    lista_libros = cargar_json(libros_path) or []

    encontrado = False

    #Buscar el archivo individual del libro
    for genero in os.listdir(RUTA_BASE):
        carpeta_genero = obtener_ruta_genero(genero)
        archivo = os.path.join(carpeta_genero, f"{libro_id}.json")

        if os.path.exists(archivo):
            libro = cargar_json(archivo)
            libro.update(nuevos_datos)
            guardar_json(archivo, libro)
            encontrado = True

            #Actualizar también en libros.json
            for item in lista_libros:
                if item["libro_id"] == libro_id:
                    item["libro"]["title"] = nuevos_datos.get("title", item["libro"]["title"])
                    item["libro"]["autor"] = nuevos_datos.get("autor", item["libro"]["autor"])
                    break

            #Actualizar en indice_isbn.json
            for item in indice:
                if item["isbn"] == libro["isbn"]:
                    item["title"] = nuevos_datos.get("title", item["title"])
                    item["autor"] = nuevos_datos.get("autor", item["autor"])
                    break

            break  #dejamos de buscar

    #Guardar actualizaciones
    if encontrado:
        guardar_json(libros_path, lista_libros)
        guardar_json(indice_path, indice)
        return True
    else:
        return False


def eliminar_libro(libro_id):
    """
    Elimina un ejemplar de libro en todas las estructuras:
    - Archivo individual del ejemplar
    - Entrada en libros.json
    - Ejemplar dentro de indice_isbn.json

    Args:
        libro_id (str): ID del libro a eliminar
    
    Returns:
        bool: True si se eliminó correctamente, False si no se encontró
    """
    indice_path = os.path.join(RUTA_BASE, "indice_isbn.json")
    libros_path = os.path.join(RUTA_BASE, "libros.json")

    indice = cargar_json(indice_path) or []
    lista_libros = cargar_json(libros_path) or []

    eliminado = False
    isbn_encontrado = None

    # Buscar y eliminar el archivo del ejemplar
    for genero in os.listdir(RUTA_BASE):
        carpeta_genero = obtener_ruta_genero(genero)
        archivo = os.path.join(carpeta_genero, f"{libro_id}.json")

        if os.path.exists(archivo):
            libro = cargar_json(archivo)
            isbn_encontrado = libro["isbn"]
            os.remove(archivo)
            eliminado = True
            break

    if not eliminado:
        return False

    # 🔹 Eliminar del archivo libros.json
    lista_libros = [l for l in lista_libros if l["libro_id"] != libro_id]

    # 🔹 Eliminar del índice de ISBN
    for libro in indice:
        if libro["isbn"] == isbn_encontrado:
            libro["ejemplares"] = [e for e in libro["ejemplares"] if e["libro_id"] != libro_id]
            # Si ya no quedan ejemplares de ese ISBN, también se borra el libro del índice
            if len(libro["ejemplares"]) == 0:
                indice.remove(libro)
            break

    # Guardar cambios
    guardar_json(libros_path, lista_libros)
    guardar_json(indice_path, indice)

    return True


def listar_libros() -> list[dict]:
    """
    Retorna una lista con todos los libros que haya registrados en la biblioteca.

    Recorre las carpetas por género dentro de data/libros/
    y carga la información de cada archivo JSON.

    Returns:
        list[dict]: lista de libros en formato diccionario
    """
    libros = []
    try:
        for genero in os.listdir(RUTA_BASE):
            ruta_genero = os.path.join(RUTA_BASE, genero)
            if os.path.isdir(ruta_genero):
                for archivo in os.listdir(ruta_genero):
                    if archivo.endswith(".json"):
                        ruta_archivo = os.path.join(ruta_genero, archivo)
                        with open(ruta_archivo, "r", encoding="utf-8") as f:
                            libro = json.load(f)
                            libros.append(libro)
        return libros
    except Exception as e:
        print(f"Error al listar libros: {e}")
        return []
