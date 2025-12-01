from flask import Flask, request, jsonify
from common.models import Book, IssueRecord
from server.storage import Storage
from datetime import datetime, timedelta # <-- timedelta добавлен для проверки просрочек
from server.recommender import recommend_for_user
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("api")

app = Flask(__name__)
st = Storage()

def error(message, code=400):
    """Вспомогательная функция для генерации ответов с ошибкой."""
    return jsonify({"ok": False, "error": message}), code

@app.get("/books")
def books_get():
    """Поиск книг: /books?q=строка"""
    q = (request.args.get("q") or "").strip().lower()
    books = st.load_books()
    if not q:
        return jsonify({"ok": True, "items": [b.to_dict() for b in books]})
    res = []
    for b in books:
        hay = f"{b.title} {b.author} {b.genre}".lower()
        if q in hay: res.append(b.to_dict())
    return jsonify({"ok": True, "items": res})

@app.post("/books")
def books_add():
    """Добавление книги."""
    data = request.get_json(force=True, silent=True) or {}
    need = ["isbn","title","author","genre","total_copies"]
    for k in need:
        if k not in data: return error(f"missing field: {k}")
    books = st.load_books()
    if any(b.isbn == data["isbn"] for b in books):
        return error("book already exists", 409)
    try:
        total = int(data["total_copies"])
    except ValueError:
        return error("total_copies must be an integer")
        
    b = Book(
        isbn=str(data["isbn"]),
        title=str(data["title"]),
        author=str(data["author"]),
        genre=str(data.get("genre","")),
        total_copies=total,
        available_copies=total
    )
    books.append(b)
    st.save_books(books)
    return jsonify({"ok": True, "item": b.to_dict()}), 201

@app.post("/issue")
def issue_book():
    """Выдача: {user_id, isbn}"""
    data = request.get_json(force=True, silent=True) or {}
    for k in ["user_id","isbn"]:
        if k not in data: return error(f"missing field: {k}")
    books = st.load_books()
    book = st.find_book(books, str(data["isbn"]))
    if not book: return error("book not found", 404)
    if book.available_copies <= 0: return error("no copies available", 409)

    issues = st.load_issues()
    # Проверим, что у пользователя нет активной выдачи этой книги
    for i in issues:
        if i.user_id == data["user_id"] and i.isbn == book.isbn and i.returned_on is None:
            return error("already issued to this user", 409)

    log.info("ISSUE user=%s isbn=%s", data["user_id"], data["isbn"])
    
    issues.append(IssueRecord(
        user_id=str(data["user_id"]),
        isbn=book.isbn,
        issued_on=datetime.now().strftime("%Y-%m-%d"),
        returned_on=None
    ))
    book.available_copies -= 1
    st.save_books(books); st.save_issues(issues)
    return jsonify({"ok": True})

@app.post("/return")
def return_book():
    """Возврат: {user_id, isbn}"""
    data = request.get_json(force=True, silent=True) or {}
    for k in ["user_id","isbn"]:
        if k not in data: return error(f"missing field: {k}")
    books = st.load_books()
    book = st.find_book(books, str(data["isbn"]))
    if not book: return error("book not found", 404)

    issues = st.load_issues()
    found = False
    for i in issues:
        if i.user_id == data["user_id"] and i.isbn == book.isbn and i.returned_on is None:
            i.returned_on = datetime.now().strftime("%Y-%m-%d")
            found = True
            break
    if not found: return error("active issue not found", 404)

    log.info("RETURN user=%s isbn=%s", data["user_id"], data["isbn"])
    
    book.available_copies += 1
    st.save_books(books); st.save_issues(issues)
    return jsonify({"ok": True})

@app.get("/reco")
def recommendations():
    """Рекомендации: /reco?user_id=..."""
    user_id = request.args.get("user_id")
    if not user_id:
        return error("missing user_id parameter", 400)
        
    books = st.load_books()
    issues = st.load_issues()
    
    reco_books = recommend_for_user(user_id, books, issues, k=3)
    
    return jsonify({"ok": True, "items": [b.to_dict() for b in reco_books]})

@app.get("/overdues")
def overdues_check():
    """Проверка просрочек. Возвращает список просроченных записей."""
    # Лимит: 14 дней
    OVERDUE_LIMIT_DAYS = 14
    
    issues = st.load_issues()
    books = st.load_books()
    book_map = {b.isbn: b for b in books}
    
    overdues = []
    today = datetime.now().date()
    
    for issue in issues:
        if issue.returned_on is None:
            try:
                issued_date = datetime.strptime(issue.issued_on, "%Y-%m-%d").date()
                
                days_passed = (today - issued_date).days
                
                if days_passed > OVERDUE_LIMIT_DAYS:
                    # Получаем заголовок книги, используя безопасный доступ (book_map.get)
                    book_data = book_map.get(issue.isbn)
                    book_title = book_data.title if book_data else "Unknown Book"
                    
                    overdues.append({
                        "user_id": issue.user_id,
                        "isbn": issue.isbn,
                        "issued_on": issue.issued_on,
                        "days_overdue": days_passed - OVERDUE_LIMIT_DAYS,
                        "book_title": book_title
                    })
            except ValueError:
                log.error("Invalid date format in issue record: %s", issue.issued_on)
                continue
                
    return jsonify({"ok": True, "overdues": overdues})


@app.errorhandler(500)
def _e500(e):
    """Обработчик внутренних ошибок."""
    log.error("Internal Server Error: %s", e)
    return error("internal error", 500)

if __name__ == "__main__":
    app.run(port=5001, debug=True)