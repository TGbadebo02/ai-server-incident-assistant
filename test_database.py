import sqlite3
import tempfile
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
