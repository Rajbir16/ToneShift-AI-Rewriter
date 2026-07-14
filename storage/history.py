import json
import os
from datetime import datetime


class HistoryStore:
    def __init__(self, path=None):

        if path is None:
            path = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")
        self.path = os.path.abspath(path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def add(self, *, original_text: str, rewritten_text: str, audience: str, tone: str, target_length: int, formality: int, created_at: str):
        item = {
            "original_text": original_text,
            "rewritten_text": rewritten_text,
            "audience": audience,
            "tone": tone,
            "target_length": target_length,
            "formality": formality,
            "created_at": created_at,
        }
        data = self._read()
        data.append(item)
        data = data[-50:]
        self._write(data)

    def list(self):
        return self._read()

    def delete(self, created_at: str):
        data = self._read()
        filtered = [item for item in data if item["created_at"] != created_at]
        self._write(filtered)

    def clear(self):
        self._write([])

    def get(self, created_at: str):
        data = self._read()
        return next((item for item in data if item["created_at"] == created_at), None)

    def _read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
