# API Reference

Base path:

```text
/api/v1
```

Swagger UI:

```text
/api/v1/docs
```

## Devices

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/devices` | List all devices |
| `POST` | `/devices` | Register a device |
| `GET` | `/devices/<id>` | Get device detail and recent events |
| `PATCH` | `/devices/<id>/status` | Update status and last seen |

## Events

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/events` | List paginated vision events |
| `POST` | `/events` | Create a vision event |
| `GET` | `/events/stats` | Event aggregates |

## Inspections

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/inspections` | List paginated inspection results |
| `POST` | `/inspections` | Create an inspection result |
| `GET` | `/inspections/summary` | Inspection aggregates |

## Stats

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/stats/overview` | Dashboard overview payload |

## Auth

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/token` | Issue JWT from API key |

## Example create device payload

```json
{
  "name": "Jetson-Line-03",
  "type": "jetson",
  "location": "Packaging Cell C",
  "status": "online"
}
```

## Example create event payload

```json
{
  "device_id": "11111111-1111-1111-1111-111111111111",
  "event_type": "detection",
  "confidence": 0.94,
  "label": "cap",
  "frame_ts": "2026-03-25T20:45:00Z",
  "metadata": {
    "bbox": [120, 60, 40, 42],
    "source": "camera-a"
  }
}
```

## Example create inspection payload

```json
{
  "device_id": "11111111-1111-1111-1111-111111111111",
  "job_id": "JOB-20260325-001",
  "result": "fail",
  "defect_type": "seal_breach",
  "score": 0.88,
  "image_path": "/captures/2026/03/25/frame-001.jpg"
}
```
