import logging
import random
from flask import Flask, request, jsonify
from .database import StringScorerDB


class StringScorerServer:
    def __init__(self):
        self.setup_logging()
        self.logger.debug("Initializing StringScorerServer.")
        self.app = Flask(__name__)
        self.initialize_db()
        self.configure_routes()

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)
        log_handler = logging.StreamHandler()
        log_formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        log_handler.setFormatter(log_formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.DEBUG)

    def initialize_db(self):
        self.logger.debug("Initializing database with app context.")
        self.db = StringScorerDB(self.app, "sqlite:///textscore.db")

        with self.app.app_context():
            self.db.initialize_db()
        self.logger.debug("Database tables created.")

    def configure_routes(self):
        @self.app.route("/score_text", methods=["POST"])
        def score_text():
            self.logger.debug("Received request to score text.")

            data = request.json
            text = data.get("text")

            # Placeholder for scoring function
            scores = {"vectara": random.random(), "toxicity": random.random()}
            self.logger.debug(f"Scoring complete. Text: {text}, Score: {scores}")

            log_entry = self.db.create_log_entry(text, scores)
            self.logger.debug(f"Logged to database: {log_entry}")

            return jsonify(scores)

    def start_server(self):
        self.logger.debug("Initialization complete. Starting Flask server.")
        self.app.run(debug=True, port=54321)


def entrypoint():
    server = StringScorerServer()
    server.start_server()