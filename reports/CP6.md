# Отчет CP6: Файловый ввод-вывод (CSV/JSON)

## 1. Описание форматов и примеры

### 1.1. Формат books.csv

| Поле | Тип данных | Инвариант |
| :--- | :--- | :--- |
| **isbn** | Строка | Уникален |
| **title** | Строка | Не пустое |
| **available_copies** | Целое число | available_copies <= total_copies |

**Пример строки CSV:**
```csv
isbn,title,author,genre,total_copies,available_copies
978-5-17-094770-4,"Морфий","Булгаков М.А.","Классика",5,3