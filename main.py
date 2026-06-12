import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional



class Theme:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


    TEAL = "\033[96m"
    WHITE = "\033[97m"
    AMBER = "\033[93m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    GRAY = "\033[90m"

    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def header(title: str) -> None:
        print(f"{Theme.TEAL}{'╔' + '═'*58 + '╗'}{Theme.RESET}")
        print(f"{Theme.TEAL}║{Theme.RESET}{Theme.BOLD}{Theme.WHITE}{title.center(58)}{Theme.RESET}{Theme.TEAL}║{Theme.RESET}")
        print(f"{Theme.TEAL}{'╚' + '═'*58 + '╝'}{Theme.RESET}")

    @staticmethod
    def line() -> None:
        print(f"{Theme.GRAY}{'─'*60}{Theme.RESET}")

    @staticmethod
    def ok(msg: str) -> None:
        print(f"{Theme.GREEN}✔ {msg}{Theme.RESET}")

    @staticmethod
    def warn(msg: str) -> None:
        print(f"{Theme.AMBER}⚠ {msg}{Theme.RESET}")

    @staticmethod
    def err(msg: str) -> None:
        print(f"{Theme.RED}✖ {msg}{Theme.RESET}")

    @staticmethod
    def input(prompt: str) -> str:
        return input(f"{Theme.TEAL}➜ {Theme.RESET}{prompt}")

    @staticmethod
    def pause() -> None:
        input(f"{Theme.DIM}{Theme.GRAY}\nEnter ile devam...{Theme.RESET}")



# 1) Book Class

@dataclass
class Book:
    name: str
    author: str
    year: int

    def __str__(self) -> str:
        return f"{self.name} | {self.author} | {self.year}"



# 2) Library Class

class Library:
    def __init__(self, db_path: str = "books.json") -> None:
        self.db_path = db_path
        self.books: List[Book] = []
        self._load()

    @staticmethod
    def _norm(s: str) -> str:
        return " ".join(s.strip().lower().split())

    def _load(self) -> None:
        if not os.path.exists(self.db_path):
            self.books = []
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
        except Exception:
            self.books = []

    def _save(self) -> None:
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump([asdict(b) for b in self.books], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # --- 6 Required operations ---
    def add_book(self, name: str, author: str, year: int) -> None:
        self.books.append(Book(name=name, author=author, year=year))
        self._save()

    def remove_book(self, name: str) -> bool:
        target = self._norm(name)
        for i, b in enumerate(self.books):  # linear search
            if self._norm(b.name) == target:
                self.books.pop(i)
                self._save()
                return True
        return False

    def search_by_name(self, name: str) -> List[Book]:
        key = self._norm(name)
        results: List[Book] = []
        for b in self.books:  # linear search
            if key in self._norm(b.name):
                results.append(b)
        return results

    def search_by_author(self, author: str) -> List[Book]:
        key = self._norm(author)
        results: List[Book] = []
        for b in self.books:  # linear search
            if key in self._norm(b.author):
                results.append(b)
        return results

    def list_books(self) -> List[Book]:
        return list(self.books)



# Input Validators

def read_non_empty(label: str) -> str:
    while True:
        s = Theme.input(label).strip()
        if s:
            return s
        Theme.warn("Boş olamaz. Tekrar gir.")

def read_year(label: str) -> int:
    while True:
        s = Theme.input(label).strip()
        try:
            y = int(s)
            if 1 <= y <= 2100:
                return y
            Theme.warn("Yıl 1-2100 arası olmalı.")
        except ValueError:
            Theme.warn("Yıl sayı olmalı (ör: 2022).")





def show_books(books: List[Book], title: str) -> None:
    Theme.header(title)
    if not books:
        Theme.warn("Kayıt yok.")
        return

    # Table header
    Theme.line()
    print(f"{Theme.BOLD}{'#'.ljust(3)}{'Kitap Adı'.ljust(25)}{'Yazar'.ljust(22)}Yıl{Theme.RESET}")
    Theme.line()

    for idx, b in enumerate(books, start=1):
        name = b.name if len(b.name) <= 24 else b.name[:24] + "…"
        author = b.author if len(b.author) <= 21 else b.author[:21] + "…"
        print(f"{str(idx).ljust(3)}{name.ljust(25)}{author.ljust(22)}{b.year}")

    Theme.line()



# 6-Option Menu

def print_menu() -> None:
    Theme.line()
    print(f"{Theme.BOLD}{Theme.WHITE}1{Theme.RESET} - Kitap Ekle")
    print(f"{Theme.BOLD}{Theme.WHITE}2{Theme.RESET} - Kitap Sil")
    print(f"{Theme.BOLD}{Theme.WHITE}3{Theme.RESET} - Kitap Ara (İsme Göre)")
    print(f"{Theme.BOLD}{Theme.WHITE}4{Theme.RESET} - Kitap Ara (Yazara Göre)")
    print(f"{Theme.BOLD}{Theme.WHITE}5{Theme.RESET} - Tüm Kitapları Listele")
    print(f"{Theme.BOLD}{Theme.WHITE}6{Theme.RESET} - Çıkış")
    Theme.line()


def main() -> None:
    lib = Library()

    while True:
        Theme.clear()
        Theme.header("LIBRARY MANAGEMENT SYSTEM (6 İster)")
        print(f"{Theme.DIM}{Theme.GRAY}OOP + List + Linear Search | Console Menu{Theme.RESET}\n")

        print_menu()
        choice = Theme.input("Seçim (1-6): ").strip()

        # 1) Add
        if choice == "1":
            Theme.clear()
            Theme.header("Kitap Ekle")
            name = read_non_empty("Kitap Adı: ")
            author = read_non_empty("Yazar: ")
            year = read_year("Yayın Yılı: ")
            lib.add_book(name, author, year)
            Theme.ok("Kitap eklendi.")
            Theme.pause()

        # 2) Remove
        elif choice == "2":
            Theme.clear()
            Theme.header("Kitap Sil")
            name = read_non_empty("Silinecek kitap adı (tam): ")
            if lib.remove_book(name):
                Theme.ok("Kitap silindi.")
            else:
                Theme.err("Kitap bulunamadı.")
            Theme.pause()

        # 3) Search by name
        elif choice == "3":
            Theme.clear()
            q = read_non_empty("Aranacak kitap adı (parça olabilir): ")
            results = lib.search_by_name(q)
            show_books(results, "İsme Göre Arama Sonuçları")
            Theme.pause()

        # 4) Search by author
        elif choice == "4":
            Theme.clear()
            q = read_non_empty("Aranacak yazar adı (parça olabilir): ")
            results = lib.search_by_author(q)
            show_books(results, "Yazara Göre Arama Sonuçları")
            Theme.pause()

        # 5) List all
        elif choice == "5":
            Theme.clear()
            show_books(lib.list_books(), "Tüm Kitaplar")
            Theme.pause()

        # 6) Exit
        elif choice == "6":
            Theme.clear()
            Theme.header("Çıkış")
            Theme.ok("Program kapatıldı. Görüşürüz!")
            break

        else:
            Theme.warn("Geçersiz seçim! 1-6 arası gir.")
            Theme.pause()


if __name__ == "__main__":
    main() şimdi şunun sıra
