📚 Gestión Bibliotecaria

Gestión Bibliotecaria es una aplicación desarrollada en Python 3 que permite administrar de forma sencilla el funcionamiento de una biblioteca.
El proyecto está organizado en una arquitectura en capas, separando la lógica de negocio, la presentación y el manejo de datos.



🧩 Tecnologías utilizadas

Lenguaje: Python 3

Almacenamiento: Archivos JSON organizados en una estructura de directorios

Arquitectura: En capas

Presentación: interacción con el usuario

Lógica de Negocio: procesamiento de reglas del sistema

Datos: lectura y escritura de la información en formato JSON



⚙️ Instalación y ejecución

1. 📦 Descargar el proyecto
Descargá la carpeta completa (o el archivo .zip) del repositorio y extraelo en tu computadora.

2. 🐍 Ejecutar la aplicación
Abrí una terminal dentro de la carpeta del proyecto y escribí:
python main.py

3. ✅ ¡Listo!
El sistema iniciará y podrás comenzar a utilizar las funcionalidades disponibles.



👩‍💻 Equipo de desarrollo

| Rol           | Nombre                                 |
| ------------- | -------------------------------------- |
| Líder técnica | **Correa, Elizabeth Florencia Solana** |
| Backend       | **Miño, Sofía Micaela**                |
| QA / Test     | **Pelardas, Pablo Martín**             |
| Documentación | **Micheloni, Valentina**               |
| Presentación  | **Marturell Moyegas, Jean Carlos**     |



🗂️ Estructura del proyecto

GestiónBibliotecaria/
│
├── data/              # Archivos JSON con la información
├── negocio/           # Lógica de negocio (gestión de libros, usuarios, préstamos, etc.)
├── presentacion/      # Interfaz de usuario en consola
├── reports/           # Reportes generados por el sistema
├── utils/             # Funciones auxiliares y utilidades
│
├── .gitignore         # Archivos y carpetas que no se versionan
├── main.py            # Punto de entrada del sistema
└── README.md          # Documentación del proyecto