"""InternalWebServer: Flask application entry point."""

import os
import platform
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

START_TIME = datetime.now(timezone.utc)


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/info")
    def info():
        uptime = datetime.now(timezone.utc) - START_TIME
        return jsonify(
            app="InternalWebServer",
            python=platform.python_version(),
            server_time=datetime.now(timezone.utc).isoformat(),
            uptime_seconds=int(uptime.total_seconds()),
        )

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="not found"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8080")),
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
