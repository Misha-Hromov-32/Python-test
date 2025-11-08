import sqlite3
from typing import Dict, Optional

from .core.config import get_settings
from .data import users_list
from .security import hash_password

settings = get_settings()


def get_db_connection() -> sqlite3.Connection:
    settings.database_path.parent.mkdir(exist_ok=True, parents=True)
    return sqlite3.connect(settings.database_path)


def init_db() -> None:
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def ensure_default_users() -> None:
    with get_db_connection() as connection:
        for user in users_list:
            connection.execute(
                """
                INSERT OR IGNORE INTO users (username, password)
                VALUES (?, ?)
                """,
                (user.username, hash_password(user.password)),
            )


def get_user(username: str) -> Optional[Dict[str, str]]:
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT username, password, created_at
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        row = cursor.fetchone()

    if not row:
        return None

    return {
        "username": row[0],
        "password": row[1],
        "created_at": row[2],
    }

