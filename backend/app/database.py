import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "analyzer.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repository_url TEXT NOT NULL,
                repository_name TEXT NOT NULL,
                overall_score REAL NOT NULL,
                result_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_analysis(repository_url: str, result: dict[str, Any]) -> int:
    with _connect() as connection:
        cursor = connection.execute(
            "INSERT INTO analyses(repository_url, repository_name, overall_score, result_json) VALUES (?, ?, ?, ?)",
            (
                repository_url,
                result["repository"]["full_name"],
                result["scores"]["overall"],
                json.dumps(result),
            ),
        )
        return int(cursor.lastrowid)


def list_history(limit: int = 20) -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, repository_url, repository_name, overall_score, created_at FROM analyses ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
