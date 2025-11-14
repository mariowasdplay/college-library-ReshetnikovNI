from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime

ISO = "%Y-%m-%d"

@dataclass
class Book:
    isbn: str
    title: str
    author: str
    genre: str
    total_copies: int
    available_copies: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Book":
        return Book(
            isbn=str(d["isbn"]),
            title=str(d["title"]),
            author=str(d["author"]),
            genre=str(d.get("genre", "")),
            total_copies=int(d["total_copies"]),
            available_copies=int(d["available_copies"]),
        )

@dataclass
class User:
    user_id: str
    name: str

    def to_dict(self): return asdict(self)

@dataclass
class IssueRecord:
    user_id: str
    isbn: str
    issued_on: str  # YYYY-MM-DD
    returned_on: Optional[str] = None

    def to_dict(self): return asdict(self)

    @staticmethod
    def today() -> str:
        return datetime.now().strftime(ISO)