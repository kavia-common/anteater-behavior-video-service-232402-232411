from __future__ import annotations

from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api

from .routes.health import blp as health_blp
from .routes.behavior_video import blp as behavior_video_blp


app = Flask(__name__, static_folder="static", static_url_path="/static")
app.url_map.strict_slashes = False

# Allow cross-origin requests for easy preview/testing.
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAPI / Swagger UI configuration (flask-smorest).
app.config["API_TITLE"] = "Anteater Behavior Video API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(behavior_video_blp)


@app.errorhandler(404)
def _handle_404(err):
    """Return JSON 404 responses (including for unknown routes)."""
    return jsonify({"error": {"code": 404, "message": "Not Found"}}), 404


@app.errorhandler(500)
def _handle_500(err):
    """Return JSON 500 responses."""
    return jsonify({"error": {"code": 500, "message": "Internal Server Error"}}), 500
