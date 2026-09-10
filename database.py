import sqlite3


def get_connection():
    connection = sqlite3.connect("incidents.db")
    return connection


def initialize_database():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS incidents("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "description TEXT NOT NULL, "
            "affected_users TEXT NOT NULL, "
            "occurred_at TEXT NOT NULL, "
            "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "status TEXT NOT NULL DEFAULT 'open')"
        )
        connection.commit()
    finally:
        connection.close()


def save_incident(description, affected_users, occurred_at):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
             INSERT INTO incidents (description, affected_users, occurred_at)
             VALUES (?, ?, ?)
             """,
            (description, affected_users, occurred_at),
        )
        connection.commit()
    finally:
        connection.close()


def list_incidents():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, description, affected_users, occurred_at, created_at, status
            FROM incidents
            ORDER BY id DESC
            """)

        incidents = cursor.fetchall()
        return incidents
    finally:
        connection.close()
