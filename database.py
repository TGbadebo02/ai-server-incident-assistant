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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incident_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                level TEXT NOT NULL,
                source TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (incident_id)
                    REFERENCES incidents(id) ON DELETE CASCADE
            )
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incident_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (incident_id)
                    REFERENCES incidents(id) ON DELETE CASCADE
            )
            """)

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
