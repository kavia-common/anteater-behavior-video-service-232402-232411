# anteater-behavior-video-service-232402-232411

Flask API service that returns video information for a given anteater behavior.

## Run (local / container)

From `anteater_behavior_video_api/`:

```bash
pip install -r requirements.txt
python run.py
```

The service listens on **http://localhost:3001**.

- Swagger UI: `http://localhost:3001/docs`
- OpenAPI JSON: `http://localhost:3001/openapi.json` (via flask-smorest)

## Endpoint

### GET `/api/v1/anteater/{anteater_id}/behaviors/{behavior_id}/video`

Returns JSON:

```json
{
  "anteater_id": "1",
  "behavior_id": "1",
  "video_url": "/static/videos/1/1.mp4",
  "metadata": { "duration": 12.3, "format": "mp4" }
}
```

If the video does not exist, returns a JSON 404.

## Static video files

The API expects videos at:

`anteater_behavior_video_api/app/static/videos/{anteater_id}/{behavior_id}.mp4`

Example file included for testing:

`app/static/videos/1/1.mp4`
