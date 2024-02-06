import json

from flask_sqlalchemy import SQLAlchemy


class StringScorerDB:
    def __init__(self, app, db_uri):
        self.app = app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.db = SQLAlchemy()
        self.db.init_app(self.app)

        self.LogEntry = setup_models(self.db)

    def initialize_db(self):
        self.db.create_all()

    def create_log_entry(self, text: str, scores: dict):
        if not isinstance(scores, dict):
            raise ValueError("scores must be a dictionary")

        scores_json = json.dumps(scores)
        log_entry = self.LogEntry(text=text, scores=scores_json)
        self.db.session.add(log_entry)
        self.db.session.commit()
        return log_entry

    def get_all_scores(self):
        entries = self.LogEntry.query.all()
        return [{"text": entry.text, "scores": json.loads(entry.scores)} for entry in entries]


def setup_models(db):
    class LogEntry(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(500), nullable=False)
        scores = db.Column(db.JSON, nullable=False)

        def __repr__(self):
            return f"<LogEntry {self.text[:50]}: {self.scores}>"

    return LogEntry
