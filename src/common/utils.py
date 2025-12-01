import random
import string
from datetime import datetime

def generate_inventory_id() -> str:
    """
    Генерация случайного инвентарного номера.
    Пример: INV-94821
    """
    number = random.randint(10000, 99999)
    return f"INV-{number}"

def calculate_fine(return_date_str: str, due_date_str: str, daily_rate: float = 5.0) -> float:
    """
    Вычисление штрафа за просрочку.
    Алгоритм: (ДатаВозврата - ДатаСдачи) * Ставка.
    Если вернули вовремя или раньше — штраф 0.0.
    Результат округляется до 2 знаков.
    """
    fmt = "%Y-%m-%d"
    try:
        d_return = datetime.strptime(return_date_str, fmt)
        d_due = datetime.strptime(due_date_str, fmt)
        
        delta = (d_return - d_due).days
        if delta <= 0:
            return 0.0
        
        fine = delta * daily_rate
        return round(fine, 2)
    except ValueError:
        return 0.0

def filter_books(books: list, query: str) -> list:
    """
    Простой алгоритм поиска по каталогу.
    Ищет подстроку в названии или авторе.
    """
    q = query.lower().strip()
    if not q:
        return books
    
    result = []
    for book in books:
        # Поиск по названию или автору
        if q in book.title.lower() or q in book.author.lower():
            result.append(book)
    return result