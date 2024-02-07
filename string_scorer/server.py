import logging
import os
from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO

from string_scorer.inference import StringScorerInferencer
from string_scorer.database import StringScorerDB


class StringScorerServer:
    def __init__(self):
        self.setup_logging()
        self.logger.debug("Initializing StringScorerServer.")
        self.app = Flask(__name__, static_url_path="", static_folder="frontend/build")

        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
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
        db_host = os.environ.get("DATABASE_HOST", "stringscorerdb")
        db_port = os.environ.get("DATABASE_PORT", "5432")
        db_name = os.environ.get("DATABASE_NAME", "stringscorerdb")
        db_user = os.environ.get("DATABASE_USER", "scorer")
        db_password = os.environ.get("DATABASE_PASSWORD", "scorer")

        self.logger.debug(f"Initializing database with host: {db_host}")
        self.db = StringScorerDB(app=self.app, host=db_host, port=db_port, name=db_name, user=db_user, password=db_password)

        with self.app.app_context():
            self.db.initialize_db()
        self.logger.debug("Database tables created.")

    def score_text(self, request):
        self.logger.debug("Received request to score text.")

        data = request.json
        text = data.get("text")

        inferencer = StringScorerInferencer(logger=self.logger, models=["vectara", "toxicity"], input_text=text)
        scores = inferencer.run()

        self.logger.debug(f"Scoring complete. Text: {text}, Score: {scores}")

        log_entry = self.db.create_log_entry(text, scores)
        self.logger.debug(f"Logged to database: {log_entry}")

        self.socketio.emit("scoreUpdate", {"text": text, "scores": scores})

        return scores

    def configure_routes(self):
        @self.app.route("/")
        def index():
            return send_from_directory(self.app.static_folder, "index.html")

        @self.app.route("/data")
        def data():
            data = self.db.get_all_scores()
            return jsonify(data)

        @self.app.route("/score_text", methods=["POST"])
        def score_text_route():
            return jsonify(self.score_text(request))


def production_gunicorn_worker():
    server = StringScorerServer()
    return server.app


def start_local_dev_server():
    server = StringScorerServer()
    server.socketio.run(server.app, host="0.0.0.0", port=54321, debug=True)
