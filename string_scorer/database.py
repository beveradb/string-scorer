import json

from flask_sqlalchemy import SQLAlchemy


class StringScorerDB:
    def __init__(self, app, user, password, host, port, name):
        """
        Initializes the database connection for the StringScorer application.

        :param app: Flask application instance.
        :param user: Database user name.
        :param password: Database password.
        :param host: Database host address.
        :param port: Database port number.
        :param name: Database name.
        """
        self.app = app

        db_uri = f"postgresql://{user}:{password}@{host}:{port}/{name}"
        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.db = SQLAlchemy()
        self.db.init_app(self.app)

        self.LogEntry = setup_models(self.db)

    def initialize_db(self):
        """
        Creates all tables in the database based on the models defined.
        """
        self.db.create_all()

    def create_log_entry(self, text: str, scores: dict):
        """
        Creates a log entry in the database.

        :param text: The text that was scored.
        :param scores: A dictionary containing the scores.
        :return: The created log entry object.
        """
        if not isinstance(scores, dict):
            raise ValueError("scores must be a dictionary")

        scores_json = json.dumps(scores)
        log_entry = self.LogEntry(text=text, scores=scores_json)
        self.db.session.add(log_entry)
        self.db.session.commit()
        return log_entry

    def get_all_scores(self):
        """
        Retrieves all scored entries from the database.

        :return: A list of dictionaries, each containing the text and its scores.
        """
        entries = self.LogEntry.query.all()
        return [{"text": entry.text, "scores": json.loads(entry.scores)} for entry in entries]


def setup_models(db):
    """
    Sets up the database models.

    :param db: The SQLAlchemy database instance.
    :return: The LogEntry model class.
    """

    class LogEntry(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(500), nullable=False)
        scores = db.Column(db.JSON, nullable=False)

        def __repr__(self):
            """
            Provides a string representation of a LogEntry instance.

            :return: A string representation of the LogEntry.
            """
            return f"<LogEntry {self.text[:50]}: {self.scores}>"

    return LogEntry
