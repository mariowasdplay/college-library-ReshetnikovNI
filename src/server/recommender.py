from collections import Counter
from typing import List, Dict
from common.models import IssueRecord, Book 

def recommend_for_user(user_id: str, books: List[Book], issues: List[IssueRecord], k: int = 3) -> List[Book]:
    """
    Простая эвристика рекомендаций: 
    1. Жанры, которые чаще брал пользователь.
    2. Самые популярные жанры в целом.
    3. Любые доступные книги (fallback).
    Возвращает до k доступных книг.
    """
    user_genres = Counter()
    global_genres = Counter()
    by_isbn = {b.isbn: b for b in books}

    # 1. Анализ истории выдач для подсчета жанров
    for it in issues:
        b = by_isbn.get(it.isbn)
        if not b: continue # Пропускаем, если книги нет
        
        # Подсчет популярности жанров
        global_genres[b.genre] += 1
        if it.user_id == user_id:
            user_genres[b.genre] += 1

    # 2. Создание приоритетного списка жанров
    order = []
    seen_genres = set()
    
    for g, _ in user_genres.most_common():
        if g not in seen_genres:
            order.append(g)
            seen_genres.add(g)
            
    for g, _ in global_genres.most_common():
        if g not in seen_genres:
            order.append(g)
            seen_genres.add(g)

    # 3. Выбор рекомендованных книг по приоритету жанров
    seen_isbns = set(); out = []
    for g in order:
        for b in books:
            # Рекомендуем только доступные и ранее не рекомендованные книги
            if b.genre == g and b.available_copies > 0 and b.isbn not in seen_isbns:
                out.append(b)
                seen_isbns.add(b.isbn)
            if len(out) >= k: return out
            
    # 4. Fallback: любые доступные книги (если k не достигнуто)
    for b in books:
        if b.available_copies > 0 and b.isbn not in seen_isbns:
            out.append(b)
            seen_isbns.add(b.isbn)
        if len(out) >= k: break
        
    return out