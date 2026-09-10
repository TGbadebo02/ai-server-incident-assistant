import sqlite3
import unittest
from unittest.mock import patch

import chatbot


class TestChatbotErrorHandling(unittest.TestCase):
    @patch("chatbot.initialize_database", side_effect=sqlite3.Error("boom"))
    @patch("builtins.print")
    def test_main_exits_when_database_cannot_initialize(self, mock_print, mock_init):
        chatbot.main()

        mock_init.assert_called_once()
        mock_print.assert_any_call(
            "Chatbot: The incident database could not be initialized.\n"
        )

    @patch("chatbot.initialize_database")
    @patch("chatbot.list_incidents", side_effect=sqlite3.Error("boom"))
    @patch("builtins.input", side_effect=["list incidents", "quit"])
    @patch("builtins.print")
    def test_main_handles_list_incidents_failure(
        self, mock_print, mock_input, mock_list, mock_init
    ):
        chatbot.main()

        mock_list.assert_called_once()
        mock_print.assert_any_call(
            "Chatbot: The incidents could not be retrieved.\n"
        )

    @patch("chatbot.initialize_database")
    @patch("chatbot.save_incident", side_effect=sqlite3.Error("boom"))
    @patch(
        "builtins.input",
        side_effect=["Server down", "All users", "2026-09-01 10:00", "quit"],
    )
    @patch("builtins.print")
    def test_main_handles_save_incident_failure(
        self, mock_print, mock_input, mock_save, mock_init
    ):
        chatbot.main()

        mock_save.assert_called_once()
        mock_print.assert_any_call(
            "Chatbot: The incident could not be saved. Please try again.\n"
        )


if __name__ == "__main__":
    unittest.main()
