import tkinter as tk
from ui_screens import MainUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Колледж-Библиотека")
    root.geometry("720x520")
    MainUI(root)
    root.mainloop()