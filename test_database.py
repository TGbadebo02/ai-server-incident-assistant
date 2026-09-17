import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
import unittest
from unittest.mock import patch
import database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "test_incidents.db"

        self.connection_patch = patch(
            "database.get_connection",
            side_effect=lambda: sqlite3.connect(self.database_path),
        )
        self.connection_patch.start()

    def tearDown(self):
        self.connection_patch.stop()
        self.temp_directory.cleanup()

    def test_initialize_database_creates_table(self):
        database.initialize_database()
        database.initialize_database()

        connection = sqlite3.connect(self.database_path)

        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'incidents'
            """).fetchone()

        connection.close()

        self.assertIsNotNone(result)

    def test_save_incident(self):
        database.initialize_database()

        database.save_incident(
            "Server unavailable",
            "All customers",
            "2026-08-31 10:00",
        )

        connection = sqlite3.connect(self.database_path)
        incident = connection.execute("""
            SELECT description, affected_users, occurred_at, status
            FROM incidents
            """).fetchone()
        connection.close()

        self.assertEqual(incident[0], "Server unavailable")
        self.assertEqual(incident[1], "All customers")
        self.assertEqual(incident[2], "2026-08-31 10:00")
        self.assertEqual(incident[3], "open")

    def test_list_incidents_returns_empty_list(self):
        database.initialize_database()

        incidents = database.list_incidents()

        self.assertEqual(incidents, [])

    def test_list_incidents_returns_newest_first(self):
        database.initialize_database()

        database.save_incident(
            "First incident",
            "Team A",
            "2026-8-31 10:00",
        )

        database.save_incident(
            "Second incident",
            "Team B",
            "2026-08-31 11:00",
        )

        incidents = database.list_incidents()

        self.assertEqual(len(incidents), 2)
        self.assertEqual(incidents[0][1], "Second incident")
        self.assertEqual(incidents[1][1], "First incident")

    def test_save_incident_closes_connection_when_execute_fails(self):
        database.initialize_database()

        class FailingCursor:
            """Stands in for a real cursor and always fails on execute(),
            simulating a write error partway through save_incident()."""

            def execute(self, *args, **kwargs):
                raise sqlite3.Error("boom")

        class ConnectionSpy:
            """Wraps a real connection so we can observe close() calls
            while still delegating everything else to real sqlite3
            behavior."""

            def __init__(self, real_connection):
                self._real_connection = real_connection
                self.close_calls = 0

            def cursor(self):
                return FailingCursor()

            def commit(self):
                self._real_connection.commit()

            def close(self):
                self.close_calls += 1
                self._real_connection.close()

        connection_spy = ConnectionSpy(sqlite3.connect(self.database_path))

        with patch("database.get_connection", return_value=connection_spy):
            with self.assertRaises(sqlite3.Error):
                database.save_incident(
                    "Server unavailable",
                    "All customers",
                    "2026-08-31 10:00",
                )

        self.assertEqual(connection_spy.close_calls, 1)

    def test_creates_evidence_tables(self):
        # Initialize the database and check whether the evidence tables were created.
        database.initialize_database()

        # Open the database to verify the results of the initialization.
        with closing(sqlite3.connect(self.database_path)) as connection:
            results = connection.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """).fetchall()

        table_names = {row[0] for row in results}

        self.assertIn("incident_logs", table_names)
        self.assertIn("incident_metrics", table_names)

    # This test checks that incident_logs has exactly the columns we expect.
    def test_incident_logs_has_expected_columns(self):
        # Create all of the database tables inside the temporary test database.
        database.initialize_database()

        # Open the temporary database and close it automatically when finished.
        with closing(sqlite3.connect(self.database_path)) as connection:
            # Ask SQLite for information about every column in incident_logs.
            results = connection.execute(
                # PRAGMA table_info returns one row of information per column.
                "PRAGMA table_info(incident_logs)"
                # Collect all of the returned rows into a list called results.
            ).fetchall()

        # In each result row, item 1 is the column's name.
        # This creates a set containing only the actual column names.
        column_names = {row[1] for row in results}

        # Define the exact set of column names that incident_logs should contain.
        expected_columns = {
            "id",  # The unique ID of this log record.
            "incident_id",  # The incident that this log belongs to.
            "recorded_at",  # The date and time when the log was recorded.
            "level",  # The log severity, such as INFO, WARNING, or ERROR.
            "source",  # The server or application that produced the log.
            "message",  # The actual message contained in the log.
            "created_at",  # The date and time the log was saved in our database.
        }

        # The test passes only when the actual and expected column names match.
        self.assertEqual(expected_columns, column_names)

    def test_incident_metrics_has_expected_columns(self):
        database.initialize_database()

        with closing(sqlite3.connect(self.database_path)) as connection:
            results = connection.execute(
                "PRAGMA table_info(incident_metrics)"
            ).fetchall()

        column_names = {row[1] for row in results}

        expected_columns = {
            "id",
            "incident_id",
            "recorded_at",
            "name",
            "value",
            "unit",
            "created_at",
        }

        self.assertEqual(expected_columns, column_names)


if __name__ == "__main__":
    unittest.main()
