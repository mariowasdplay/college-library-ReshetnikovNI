from typing import List, Optional
from pathlib import Path
from common.io_utils import read_csv, write_csv, read_json, safe_write_json
from common.models import Book, IssueRecord

DATA = Path(__file__).resolve().parents[2] / "data"
BOOKS = DATA / "books.csv"
USERS = DATA / "users.csv"   # (на будущее)
ISSUES = DATA / "issues.json"

class Storage:
    def load_books(self) -> List[Book]:
        rows = read_csv(str(BOOKS))
        return [Book.from_dict({
            "isbn": r.get("isbn",""),
            "title": r.get("title",""),
            "author": r.get("author",""),
            "genre": r.get("genre",""),
            "total_copies": int(r.get("total_copies", 0) or 0),
            "available_copies": int(r.get("available_copies", 0) or 0),
        }) for r in rows]

    def save_books(self, books: List[Book]):
        rows = [b.to_dict() for b in books]
        write_csv(str(BOOKS), rows)

    def load_issues(self) -> List[IssueRecord]:
        data = read_json(str(ISSUES)) or []
        out: List[IssueRecord] = []
        for d in data:
            out.append(IssueRecord(
                user_id=str(d["user_id"]),
                isbn=str(d["isbn"]),
                issued_on=str(d["issued_on"]),
                returned_on=d.get("returned_on")
            ))
        return out

    def save_issues(self, issues: List[IssueRecord]):
        safe_write_json(str(ISSUES), [i.to_dict() for i in issues])

    # вспомогательные:
    def find_book(self, books: List[Book], isbn: str) -> Optional[Book]:
        for b in books:
            if b.isbn == isbn: return b
        return None