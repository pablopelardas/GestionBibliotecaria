import csv
import json
from collections import Counter
from pathlib import Path


class ReportGenerator:
    def __init__(self):
        """
        Inicializa el generador de reportes.
        Carga automáticamente los datos desde los archivos.
        """
        self.base_dir = Path(__file__).parent.parent
        self.reports_dir = self.base_dir / 'reports'
        self.reports_dir.mkdir(exist_ok=True)
        self.users = self._cargar_usuarios()
        self.books = self._cargar_libros()
        self.loans = self._cargar_prestamos()

    def _cargar_usuarios(self):
        """Carga usuarios desde usuarios.json"""
        archivo = self.base_dir / 'data' / 'usuarios' / 'usuarios.json'
        with open(archivo, 'r', encoding='utf-8') as f:
            usuarios_lista = json.load(f)

        # Convertir a diccionario con user_id como clave
        usuarios = {}
        for user_data in usuarios_lista:
            user_id = user_data['user_id']
            usuario = user_data['user'].copy()
            usuario['user_id'] = user_id
            usuarios[user_id] = usuario

        return usuarios

    def _cargar_libros(self):
        """Carga todos los libros desde la estructura de directorios por género"""
        dir_libros = self.base_dir / 'data' / 'libros'
        libros = {}

        # Recorrer todos los directorios de géneros
        for genero_dir in dir_libros.iterdir():
            if genero_dir.is_dir():
                # Leer todos los archivos JSON del género
                for archivo_libro in genero_dir.glob('*.json'):
                    try:
                        with open(archivo_libro, 'r', encoding='utf-8') as f:
                            libro = json.load(f)
                            libro_id = libro.get('libro_id')
                            if libro_id:
                                libros[libro_id] = libro
                    except json.JSONDecodeError:
                        pass

        return libros

    def _cargar_prestamos(self):
        """Carga préstamos desde prestamos.json"""
        archivo = self.base_dir / 'data' / 'prestamos' / 'prestamos.json'
        with open(archivo, 'r', encoding='utf-8') as f:
            prestamos_lista = json.load(f)

        # Convertir a diccionario con prestamo_numero como clave
        prestamos = {}
        for prestamo_data in prestamos_lista:
            # Verificar que el elemento tenga la estructura correcta
            if not isinstance(prestamo_data, dict):
                continue

            # Puede venir en dos formatos: con 'prestamo' anidado o directo
            if 'prestamo_numero' in prestamo_data and 'prestamo' in prestamo_data:
                # Formato: {"prestamo_numero": 1, "prestamo": {...}}
                prestamo_num = prestamo_data['prestamo_numero']
                prestamo = prestamo_data['prestamo'].copy()
                prestamo['prestamo_numero'] = prestamo_num
            elif 'prestamo_numero' in prestamo_data:
                # Formato directo: {"prestamo_numero": 1, "user_id": ..., "libro_id": ...}
                prestamo = prestamo_data.copy()
                prestamo_num = prestamo['prestamo_numero']
            else:
                # Elemento sin prestamo_numero, ignorar
                continue

            # Agregar campo 'status' para compatibilidad
            prestamo['status'] = 'returned' if prestamo.get('regresado', False) else 'active'
            prestamos[prestamo_num] = prestamo

        return prestamos

    # 1. Totals
    def report_totals(self, export=False):
        total_users = len(self.users)
        total_books = len(self.books)
        active_loans = sum(1 for loan in self.loans.values() if not loan.get("regresado", False))

        report = {
            "Total de Usuarios": total_users,
            "Total de Libros": total_books,
            "Préstamos Activos": active_loans,
        }

        self._print_report("Totales de la Biblioteca", report)

        if export:
            self._export_to_csv("report_totals.csv", report)

    # 2. Most Borrowed Books
    def report_most_borrowed_books(self, top_n=5, export=False, only_active=False):
        # Si only_active=True, contar solo préstamos no devueltos
        borrowed_books = [
            loan.get("libro_id")
            for loan in self.loans.values()
            if loan.get("libro_id") and (not only_active or not loan.get("regresado", False))
        ]
        counter = Counter(borrowed_books)

        report = []
        for book_id, count in counter.most_common(top_n):
            libro = self.books.get(book_id, {})
            report.append({
                "Libro": libro.get("title", "Desconocido"),
                "Autor": libro.get("autor", "Desconocido"),
                "Veces Prestado": count
            })

        self._print_table("Libros Más Prestados", report)

        if export:
            self._export_list_to_csv("report_most_borrowed_books.csv", report)

        return report

    # 3. Users with Most Borrowed Books
    def report_top_users(self, top_n=5, export=False):
        # Contar préstamos por usuario (histórico)
        user_counts = {}
        for loan in self.loans.values():
            user_id = loan.get("user_id")
            if not user_id:
                continue
            user_counts[user_id] = user_counts.get(user_id, 0) + 1

        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

        report = []
        for uid, count in sorted_users[:top_n]:
            usuario = self.users.get(uid, {})
            libros_actuales = len(usuario.get("libros_prestados", []))
            report.append({
                "Usuario": usuario.get("nombre", "Desconocido"),
                "Préstamos Totales": count,
                "Libros Actuales": libros_actuales
            })

        self._print_table("Usuarios con Más Préstamos", report, headers=["Usuario", "Préstamos Totales", "Libros Actuales"])

        if export:
            self._export_list_to_csv("report_top_users.csv", report)

        return report

    # 4. Books Available vs Borrowed
    def report_books_status(self, export=False):
        available = sum(1 for b in self.books.values() if b.get("disponible", False))
        borrowed = len(self.books) - available

        report = {
            "Libros Disponibles": available,
            "Libros Prestados": borrowed,
        }

        self._print_report("Disponibilidad de Libros", report)

        if export:
            self._export_to_csv("report_books_status.csv", report)

        return report

    # ---- Helpers ----
    def _print_report(self, title, data: dict):
        print(f"\n=== {title} ===")
        for key, value in data.items():
            print(f"{key}: {value}")

    def _print_table(self, title, rows: list, headers: list = None):
        print(f"\n=== {title} ===")
        if not rows:
            print("No data available.")
            return
        # Si se proporcionan headers explícitos (lista), úsalos; si no, toma keys del primer row
        if isinstance(rows, dict):
            rows = [rows]
        if headers is None:
            headers = list(rows[0].keys())
        print(" | ".join(headers))
        print("-" * 40)
        for row in rows:
            print(" | ".join(str(row.get(h, '')) for h in headers))

    def _export_to_csv(self, filename, data: dict):
        path = self.reports_dir / filename
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            for key, value in data.items():
                writer.writerow([key, value])
        print(f"CSV report saved as {path}")

    def _export_list_to_csv(self, filename, data: list):
        if not data:
            print("No data to export.")
            return
        path = self.reports_dir / filename
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV report saved as {path}")

    # 5. Estadísticas por Género (usando MATRIZ)
    def report_estadisticas_por_genero(self):
        """
        Genera un reporte de estadísticas por género usando una MATRIZ.
        La matriz tiene:
        - Filas: cada género
        - Columnas: Total, Disponibles, Prestados, % Disponibilidad

        Returns:
            list: Matriz con las estadísticas por género
        """
        # Obtener lista de géneros únicos
        generos = set()
        for libro in self.books.values():
            genero = libro.get('genero', 'otros')
            generos.add(genero)

        generos = sorted(list(generos))

        # Crear matriz vacía: filas = géneros, columnas = [Total, Disponibles, Prestados, % Disponibilidad]
        # Inicializar matriz con ceros
        matriz = []
        for i in range(len(generos)):
            # [total, disponibles, prestados, porcentaje_disponibilidad]
            matriz.append([0, 0, 0, 0.0])

        # Llenar la matriz con los datos
        for i in range(len(generos)):
            genero = generos[i]
            for libro in self.books.values():
                if libro.get('genero', 'otros') == genero:
                    matriz[i][0] += 1  # Total
                    if libro.get('disponible', False):
                        matriz[i][1] += 1  # Disponibles
                    else:
                        matriz[i][2] += 1  # Prestados

            # Calcular porcentaje de disponibilidad
            if matriz[i][0] > 0:
                matriz[i][3] = (matriz[i][1] / matriz[i][0]) * 100

        # Imprimir la matriz en formato tabla
        print("\n=== Estadísticas por Género (Matriz) ===")
        print(f"{'Género':<15} | {'Total':>8} | {'Disponibles':>12} | {'Prestados':>10} | {'% Disponib.':>12}")
        print("-" * 75)

        for i in range(len(generos)):
            genero = generos[i]
            print(f"{genero.capitalize():<15} | {matriz[i][0]:>8} | {matriz[i][1]:>12} | {matriz[i][2]:>10} | {matriz[i][3]:>11.1f}%")

        # Calcular totales usando ciclos tradicionales
        total_libros = 0
        total_disponibles = 0
        total_prestados = 0

        for i in range(len(matriz)):
            total_libros += matriz[i][0]
            total_disponibles += matriz[i][1]
            total_prestados += matriz[i][2]

        porcentaje_total = (total_disponibles / total_libros * 100) if total_libros > 0 else 0

        print("-" * 75)
        print(f"{'TOTAL':<15} | {total_libros:>8} | {total_disponibles:>12} | {total_prestados:>10} | {porcentaje_total:>11.1f}%")

        return matriz