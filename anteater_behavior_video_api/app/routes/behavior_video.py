from __future__ import annotations

import os
from typing import Any, Dict

from flask import current_app, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields


blp = Blueprint(
    "Anteater Behavior Video",
    __name__,
    url_prefix="/api/v1",
    description="Endpoints for retrieving video data for a given anteater behavior.",
)


class VideoMetadataSchema(Schema):
    """Marshmallow schema describing the JSON response for a behavior video."""

    anteater_id = fields.String(required=True, description="Unique identifier for the anteater.")
    behavior_id = fields.String(required=True, description="Unique identifier for the behavior.")
    video_url = fields.String(required=True, description="Resolvable URL to the behavior video.")
    metadata = fields.Dict(
        required=True,
        description="Video metadata such as duration in seconds and format.",
        keys=fields.String(),
        values=fields.Raw(),
    )


def _video_file_exists(relative_video_path: str) -> bool:
    """Return True if the referenced video exists in the Flask static folder."""
    static_folder = current_app.static_folder or ""
    abs_path = os.path.join(static_folder, relative_video_path)
    return os.path.isfile(abs_path)


def _build_video_response(anteater_id: str, behavior_id: str) -> Dict[str, Any]:
    """
    Build the response payload for an anteater behavior video.

    For this basic implementation, we map to a deterministic static file path:
    static/videos/{anteater_id}/{behavior_id}.mp4

    If that file does not exist, we respond with a JSON 404.
    """
    relative_video_path = os.path.join("videos", anteater_id, f"{behavior_id}.mp4")
    if not _video_file_exists(relative_video_path):
        abort(
            404,
            message="Video not found for the specified anteater/behavior.",
            errors={"anteater_id": anteater_id, "behavior_id": behavior_id},
        )

    # Use Flask's static URL resolver so it works across environments.
    video_url = url_for("static", filename=relative_video_path, _external=False)

    # Placeholder metadata; in a real system you might probe the file or store metadata in DB.
    return {
        "anteater_id": anteater_id,
        "behavior_id": behavior_id,
        "video_url": video_url,
        "metadata": {"duration": 12.3, "format": "mp4"},
    }


@blp.route("/anteater/<string:anteater_id>/behaviors/<string:behavior_id>/video")
class AnteaterBehaviorVideo(MethodView):
    """Fetch video metadata for a given anteater behavior."""

    @blp.response(200, VideoMetadataSchema)
    def get(self, anteater_id: str, behavior_id: str) -> Dict[str, Any]:
        """
        Get video data for a specific anteater behavior.

        Returns a JSON payload:
        - anteater_id
        - behavior_id
        - video_url (served from this service's /static path)
        - metadata (duration, format)

        404 is returned when the expected static video file is not present.
        """
        return _build_video_response(anteater_id=anteater_id, behavior_id=behavior_id)
