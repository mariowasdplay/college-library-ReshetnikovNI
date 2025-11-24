import tkinter as tk
<<<<<<< HEAD
from .ui_screens import MainUI
=======
from ui_screens import MainUI
>>>>>>> 3bf9f132078a5fea7b37245ea7a8dde86dfb0f22

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Колледж-Библиотека")
    root.geometry("720x520")
    MainUI(root)
    root.mainloop()