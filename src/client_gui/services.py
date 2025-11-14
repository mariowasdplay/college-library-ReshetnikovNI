import requests

API = "http://127.0.0.1:5001"

class ApiError(Exception): pass

def _req(method, path, **kw):
    try:
        r = requests.request(method, API + path, timeout=5, **kw)
    except requests.RequestException as e:
        raise ApiError(f"network error: {e}")
    try:
        data = r.json()
    except Exception:
        raise ApiError(f"http {r.status_code}: invalid json")
    if not data.get("ok"):
        raise ApiError(data.get("error","unknown error"))
    return data

def books_search(q: str):
    return _req("GET", "/books", params={"q": q}).get("items", [])

def books_add(item: dict):
    return _req("POST", "/books", json=item).get("item")

def issue(user_id: str, isbn: str):
    return _req("POST", "/issue", json={"user_id": user_id, "isbn": isbn})

def return_(user_id: str, isbn: str):
    return _req("POST", "/return", json={"user_id": user_id, "isbn": isbn})
