import unittest
from unittest.mock import patch, MagicMock, mock_open
from string_scorer.database import StringScorerDB, setup_models


class TestStringScorerDB(unittest.TestCase):

    def setUp(self):
        self.patcher1 = patch("flask_sqlalchemy.SQLAlchemy")
        self.MockSQLAlchemy = self.patcher1.start()

        self.mock_app = MagicMock()
        self.mock_app.config = {}

        # Mock the app_context to return a context manager
        self.mock_app.app_context.return_value.__enter__ = MagicMock()
        self.mock_app.app_context.return_value.__exit__ = MagicMock()

        self.mock_db = MagicMock()
        self.LogEntry = MagicMock()
        setup_models(self.mock_db)

    def tearDown(self):
        self.patcher1.stop()

    def test_initialize_db(self):
        """
        Test the initialization of the StringScorerDB with a mock app and assert that
        the create_all method is called to set up the database tables.
        """
        # Push an application context
        with self.mock_app.app_context():
            # Initialize StringScorerDB with the mock app
            db = StringScorerDB(self.mock_app, "user", "password", "host", "5432", "name")
            db.initialize_db()

            # Assert that create_all was called on the db
            self.MockSQLAlchemy.return_value.create_all.assert_called_once()

    def test_create_log_entry(self):
        """
        Test the creation of a log entry in the database by asserting that an entry
        is added to the session and committed.
        """
        # Push an application context
        with self.mock_app.app_context():
            # Initialize StringScorerDB with the mock app
            db = StringScorerDB(self.mock_app, "user", "password", "host", "5432", "name")
            db.LogEntry = self.LogEntry  # Use the mocked LogEntry model

            text = "test text"
            scores = {"score": 1}

            # Call create_log_entry
            db.create_log_entry(text, scores)

            # Assert that an entry was added to the session and committed
            self.mock_db.session.add.assert_called_once()
            self.mock_db.session.commit.assert_called_once()

    def test_get_all_scores(self):
        """
        Test retrieving all scores from the database by asserting that the returned
        results match the expected output.
        """
        # Mock query.all() to return a list of LogEntry objects
        self.LogEntry.query.all.return_value = [MagicMock(text="test text 1", scores='{"score": 1}'), MagicMock(text="test text 2", scores='{"score": 2}')]

        # Initialize StringScorerDB with the mock app
        db = StringScorerDB(self.mock_app, "user", "password", "host", "5432", "name")
        db.LogEntry = self.LogEntry  # Use the mocked LogEntry model

        # Call get_all_scores
        results = db.get_all_scores()

        # Assert that the results match the expected output
        expected_results = [{"text": "test text 1", "scores": {"score": 1}}, {"text": "test text 2", "scores": {"score": 2}}]
        self.assertEqual(results, expected_results)

    def test_create_log_entry_with_invalid_scores(self):
        """
        Test that creating a log entry with scores not being a dictionary
        raises a ValueError.
        """
        with self.mock_app.app_context():
            db = StringScorerDB(self.mock_app, "user", "password", "host", "5432", "name")
            db.LogEntry = self.LogEntry  # Use the mocked LogEntry model

            text = "test text"
            scores = "not a dictionary"  # Invalid scores

            # Assert that ValueError is raised with the specific message
            with self.assertRaises(ValueError) as context:
                db.create_log_entry(text, scores)

            self.assertEqual(str(context.exception), "scores must be a dictionary")


if __name__ == "__main__":
    unittest.main()
