import logging
import random
import os
from flask import Flask, render_template, request, jsonify
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
        database_host = os.environ.get("DATABASE_HOST", "stringscorerdb")
        database_port = os.environ.get("DATABASE_PORT", "5432")
        database_name = os.environ.get("DATABASE_NAME", "stringscorerdb")
        database_user = os.environ.get("DATABASE_USER", "scorer")
        database_password = os.environ.get("DATABASE_PASSWORD", "scorer")
        database_connection = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"

        self.logger.debug(f"Initializing database with host: {database_connection}")
        self.db = StringScorerDB(self.app, database_connection)

        with self.app.app_context():
            self.db.initialize_db()
        self.logger.debug("Database tables created.")

    def configure_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/data")
        def data():
            # Fetch data from the database
            data = self.db.get_all_scores()
            return jsonify(data)

        @self.app.route("/score_text", methods=["POST"])
        def score_text():
            self.logger.debug("Received request to score text.")

            data = request.json
            text = data.get("text")

            # TODO: Implement actual  ML inferencing / scoring mechanism
            scores = {"vectara": random.random(), "toxicity": random.random()}
            self.logger.debug(f"Scoring complete. Text: {text}, Score: {scores}")

            log_entry = self.db.create_log_entry(text, scores)
            self.logger.debug(f"Logged to database: {log_entry}")

            return jsonify(scores)

    def start_server(self):
        self.logger.debug("Initialization complete. Starting Flask server.")
        self.app.run(debug=True, host="0.0.0.0", port=54321)


def entrypoint():
    server = StringScorerServer()
    server.start_server()
