
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "queries.db"


def get_connection():
    """Create a connection to the SQLite database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """Create the queries table if it does not exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                department TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT
            )
        """)


def is_recent_duplicate(
    student_name,
    title,
    description,
    category,
    department,
    priority,
):
    """Check whether the same query was submitted recently."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id
            FROM queries
            WHERE LOWER(TRIM(student_name)) = LOWER(TRIM(?))
              AND LOWER(TRIM(title)) = LOWER(TRIM(?))
              AND description = ?
              AND category = ?
              AND department = ?
              AND priority = ?
              AND created_at >= datetime('now', '-2 minutes')
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                student_name,
                title,
                description,
                category,
                department,
                priority,
            ),
        ).fetchone()

    return row["id"] if row else None


def insert_query(
    student_name,
    title,
    description,
    category,
    department,
    priority,
):
    """Save a new student query and return its reference number."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO queries (
                student_name,
                title,
                description,
                category,
                department,
                priority
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_name,
                title,
                description,
                category,
                department,
                priority,
            ),
        )

        return cursor.lastrowid


def get_queries():
    """Retrieve all queries, newest first."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM queries
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def update_query_status(query_id, new_status):
    """Update a query's status and track its resolution time."""
    allowed_statuses = ["Pending", "In Progress", "Resolved"]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid query status.")

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE queries
            SET status = ?,
                resolved_at = CASE
                    WHEN ? = 'Resolved' THEN CURRENT_TIMESTAMP
                    ELSE NULL
                END
            WHERE id = ?
            """,
            (new_status, new_status, query_id),
        )


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
    print(f"Database location: {DB_PATH}")