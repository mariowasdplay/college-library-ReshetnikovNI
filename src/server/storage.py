from typing import List, Optional
from pathlib import Path
from common.io_utils import read_csv, write_csv, read_json, safe_write_json
from common.models import Book, IssueRecord
import logging

DATA = Path(__file__).resolve().parents[2] / "data"
BOOKS = DATA / "books.csv"
USERS = DATA / "users.csv"
ISSUES = DATA / "issues.json"

class TraceMixin:
    """Миксин для добавления трассировки (логирования) операций ввода/вывода."""
    def trace(self, tag, **kw):
        logging.info("TRACE %s %s", tag, kw)

class Storage(TraceMixin):
    def load_books(self) -> List[Book]:
        self.trace("load_books", path=str(BOOKS))
        rows = read_csv(str(BOOKS))
        return [Book(
            isbn=r.get("isbn",""),
            title=r.get("title",""),
            author=r.get("author",""),
            genre=r.get("genre",""),
            # ИСПРАВЛЕНИЕ: Все аргументы после первого позиционного должны быть именованными
            total_copies=int(r.get("total_copies", 0) or 0),
            available_copies=int(r.get("available_copies", 0) or 0),
        ) for r in rows]

    def save_books(self, books: List[Book]):
        self.trace("save_books", path=str(BOOKS), count=len(books))
        rows = [b.to_dict() for b in books]
        write_csv(str(BOOKS), rows)

    def load_issues(self) -> List[IssueRecord]:
        self.trace("load_issues", path=str(ISSUES))
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
        self.trace("save_issues", path=str(ISSUES), count=len(issues))
        safe_write_json(str(ISSUES), [i.to_dict() for i in issues])

    def find_book(self, books: List[Book], isbn: str) -> Optional[Book]:
        for b in books:
            if b.isbn == isbn: return b
        return None