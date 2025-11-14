import tkinter as tk
from tkinter import messagebox
from .services import books_search, books_add, issue, return_, ApiError

class MainUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        # Поиск
        tk.Label(self, text="Поиск книги:").pack(anchor="w")
        row = tk.Frame(self); row.pack(fill="x")
        self.q = tk.Entry(row); self.q.pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Искать", command=self.on_search).pack(side="right")
        self.listbox = tk.Listbox(self, height=12); self.listbox.pack(fill="both", expand=True, pady=6)

        # Действия
        act = tk.Frame(self); act.pack(fill="x")
        tk.Button(act, text="Выдать", command=self.on_issue).pack(side="left")
        tk.Button(act, text="Принять возврат", command=self.on_return).pack(side="left")
        # Добавление книги (минимум)
        add = tk.Frame(self); add.pack(fill="x", pady=8)
        tk.Label(add, text="Добавить книгу (isbn;title;author;genre;total):").pack(anchor="w")
        self.add_e = tk.Entry(add); self.add_e.pack(fill="x")
        tk.Button(add, text="Добавить", command=self.on_add).pack(anchor="e")

        self.user_id = "u001"  # упрощение: фиксированный читатель

    def _selected_isbn(self):
        s = self.listbox.curselection()
        if not s:
            messagebox.showinfo("Инфо","Выберите книгу в списке"); return None
        raw = self.listbox.get(s[0])
        # формат: "<isbn> :: <title> by <author>  (avail/total)"
        return raw.split(" :: ",1)[0]

    def on_search(self):
        items = books_search(self.q.get().strip())
        self.listbox.delete(0, tk.END)
        for it in items:
            line = f'{it["isbn"]} :: {it["title"]} by {it["author"]}  ({it["available_copies"]}/{it["total_copies"]})'
            self.listbox.insert(tk.END, line)

    def on_add(self):
        try:
            isbn,title,author,genre,total = [x.strip() for x in self.add_e.get().split(";")]
            total = int(total)
            item = {
                "isbn": isbn, "title": title, "author": author,
                "genre": genre, "total_copies": total
            }
            books_add(item)
            messagebox.showinfo("OK", "Книга добавлена")
            self.on_search()
        except ValueError:
            messagebox.showerror("Ошибка","Неверный формат. Пример: 978-5-..;Название;Автор;Жанр;2")
        except ApiError as e:
            messagebox.showerror("API", str(e))

    def on_issue(self):
        isbn = self._selected_isbn()
        if not isbn: return
        try:
            issue(self.user_id, isbn)
            messagebox.showinfo("OK","Выдано")
            self.on_search()
        except ApiError as e:
            messagebox.showerror("API", str(e))

    def on_return(self):
        isbn = self._selected_isbn()
        if not isbn: return
        try:
            return_(self.user_id, isbn)
            messagebox.showinfo("OK","Принято")
            self.on_search()
        except ApiError as e:
            messagebox.showerror("API", str(e))
src/client_gui/app.py

import tkinter as tk
from .ui_screens import MainUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Колледж-Библиотека")
    root.geometry("720x520")
    MainUI(root)
    root.mainloop()