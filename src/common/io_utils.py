import csv, json, os, tempfile
from typing import List, Dict, Any

def read_csv(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path): return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path: str, rows: List[Dict[str, Any]]):
    if not rows:
        # создаём файл с шапкой по пустой схеме:
        with open(path, "w", newline="", encoding="utf-8") as f:
            pass
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def read_json(path: str):
    if not os.path.exists(path): return []
    with open(path, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # повреждённый файл — вернём пустой массив, чтобы не падать
            return []

def safe_write_json(path: str, data):
    # атомарная запись через временный файл
    dir_ = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try: os.remove(tmp)
            except: pass