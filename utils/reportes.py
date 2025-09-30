import csv
from collections import Counter


class ReportGenerator:
    def __init__(self, users: dict, books: dict, loans: dict):
        self.users = users
        self.books = books
        self.loans = loans

    # 1. Totals
    def report_totals(self, export=False):
        total_users = len(self.users)
        total_books = len(self.books)
        active_loans = sum(1 for loan in self.loans.values() if loan["status"] == "active")

        report = {
            "Total Users": total_users,
            "Total Books": total_books,
            "Active Loans": active_loans,
        }

        self._print_report("Library Totals", report)

        if export:
            self._export_to_csv("report_totals.csv", report)

    # 2. Most Borrowed Books
    def report_most_borrowed_books(self, top_n=5, export=False):
        borrowed_books = [loan["book_id"] for loan in self.loans.values()]
        counter = Counter(borrowed_books)

        report = []
        for book_id, count in counter.most_common(top_n):
            title = self.books.get(book_id, {}).get("title", "Unknown")
            report.append({"Book": title, "Times Borrowed": count})

        self._print_table("Most Borrowed Books", report)

        if export:
            self._export_list_to_csv("report_most_borrowed_books.csv", report)

    # 3. Users with Most Borrowed Books
    def report_top_users(self, top_n=5, export=False):
        user_counts = {uid: len(data["borrowed_books"]) for uid, data in self.users.items()}
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

        report = []
        for uid, count in sorted_users[:top_n]:
            report.append({"User": self.users[uid]["name"], "Books Borrowed": count})

        self._print_table("Top Users by Borrowed Books", report)

        if export:
            self._export_list_to_csv("report_top_users.csv", report)

    # 4. Books Available vs Borrowed
    def report_books_status(self, export=False):
        available = sum(1 for b in self.books.values() if b["available"])
        borrowed = len(self.books) - available

        report = {
            "Available Books": available,
            "Borrowed Books": borrowed,
        }

        self._print_report("Books Availability", report)

        if export:
            self._export_to_csv("report_books_status.csv", report)

    # ---- Helpers ----
    def _print_report(self, title, data: dict):
        print(f"\n=== {title} ===")
        for key, value in data.items():
            print(f"{key}: {value}")

    def _print_table(self, title, rows: list):
        print(f"\n=== {title} ===")
        if not rows:
            print("No data available.")
            return
        headers = rows[0].keys()
        print(" | ".join(headers))
        print("-" * 40)
        for row in rows:
            print(" | ".join(str(v) for v in row.values()))

    def _export_to_csv(self, filename, data: dict):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            for key, value in data.items():
                writer.writerow([key, value])
        print(f"CSV report saved as {filename}")

    def _export_list_to_csv(self, filename, data: list):
        if not data:
            print("No data to export.")
            return
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV report saved as {filename}")