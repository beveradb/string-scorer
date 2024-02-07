import unittest
from unittest import mock
from flask import Flask
from flask_socketio import SocketIO
from unittest.mock import patch
from string_scorer.server import StringScorerServer
from unittest.mock import MagicMock


class TestStringScorerServer(unittest.TestCase):

    def setUp(self):
        self.patcher1 = patch("string_scorer.server.StringScorerDB")
        self.patcher2 = patch("flask.Flask")
        self.patcher3 = patch("flask_socketio.SocketIO")
        self.patcher4 = patch("flask.Flask.add_url_rule")

        self.mock_db = self.patcher1.start()
        self.mock_flask = self.patcher2.start()
        self.mock_socketio = self.patcher3.start()
        self.mock_add_url_rule = self.patcher4.start()

        self.server = StringScorerServer()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()

    def test_server_initialization(self):
        self.mock_db.assert_called_once()

        assert self.server.app is not None
        assert self.server.db is not None
        assert self.server.socketio is not None
        assert isinstance(self.server.app, Flask), "server.app should be an instance of Flask"
        assert isinstance(self.server.socketio, SocketIO), "server.socketio should be an instance of SocketIO"

    @mock.patch("string_scorer.server.StringScorerInferencer")
    def test_score_text(self, mock_inferencer):
        # Setup a mock request object with the necessary json attribute
        mock_request = MagicMock()
        mock_request.json = {"text": "test text"}

        # Initialize the server
        server = StringScorerServer()

        # Call the method under test
        server.score_text(mock_request)

        # Assert that StringScorerInferencer was called as expected
        mock_inferencer.assert_called_once_with(logger=server.logger, models=["vectara", "toxicity"], input_text="test text")


if __name__ == "__main__":
    unittest.main()
