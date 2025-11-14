from flask import Flask, request, jsonify
from common.models import Book, IssueRecord
from storage import Storage
from datetime import datetime

app = Flask(__name__)
st = Storage()

def error(message, code=400):
    return jsonify({"ok": False, "error": message}), code

@app.get("/books")
def books_get():
    """Поиск книг: /books?q=строка  (ищет по названию/автору/жанру)"""
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
    """Добавление книги (для простоты без авторизации)."""
    data = request.get_json(force=True, silent=True) or {}
    need = ["isbn","title","author","genre","total_copies"]
    for k in need:
        if k not in data: return error(f"missing field: {k}")
    books = st.load_books()
    if any(b.isbn == data["isbn"] for b in books):
        return error("book already exists", 409)
    total = int(data["total_copies"])
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
    # проверим, что у пользователя нет активной выдачи этой книги
    for i in issues:
        if i.user_id == data["user_id"] and i.isbn == book.isbn and i.returned_on is None:
            return error("already issued to this user", 409)

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

    book.available_copies += 1
    st.save_books(books); st.save_issues(issues)
    return jsonify({"ok": True})

@app.errorhandler(500)
def _e500(e):
    return error("internal error", 500)

if __name__ == "__main__":
    app.run(port=5001, debug=True)