"""InternalWebServer: Flask application entry point."""

import os
import platform
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

from links import LinkDataError, count_links, load_links

load_dotenv()

START_TIME = datetime.now(timezone.utc)


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        try:
            catalogue = load_links()
        except LinkDataError as exc:
            return render_template("error.html", message=str(exc)), 500
        return render_template(
            "index.html",
            catalogue=catalogue,
            total=count_links(catalogue),
        )

    @app.get("/api/links")
    def api_links():
        try:
            return jsonify(load_links())
        except LinkDataError as exc:
            return jsonify(error=str(exc)), 500

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
        port=int(os.getenv("PORT", "80")),
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
