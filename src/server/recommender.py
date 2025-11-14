from collections import Counter
from typing import List, Dict
from common.models import IssueRecord, Book

def recommend_for_user(user_id: string, books: List[Book], issues: List[IssueRecord], k: int = 3):
    # простая эвристика: жанры, которые чаще выдавал этот пользователь,
    # плюс самые популярные в целом
    user_genres = Counter()
    global_genres = Counter()
    by_isbn = {b.isbn: b for b in books}

    for it in issues:
        b = by_isbn.get(it.isbn)
        if not b: continue
        global_genres[b.genre] += 1
        if it.user_id == user_id:
            user_genres[b.genre] += 1

    # приоритезируем жанры пользователя, затем популярные
    order = [g for g,_ in user_genres.most_common()] + [g for g,_ in global_genres.most_common()]
    seen = set(); out = []
    for g in order:
        for b in books:
            if b.genre == g and b.available_copies > 0 and b.isbn not in seen:
                out.append(b); seen.add(b.isbn)
            if len(out) >= k: return out
    # fallback: любые доступные
    for b in books:
        if b.available_copies > 0 and b.isbn not in seen:
            out.append(b)
        if len(out) >= k: break
    return out