# API Reference

REST base path:

```text
/api/v1
```

Swagger UI:

```text
/api/v1/docs
```

WebSocket path:

```text
/ws/events
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
| `GET` | `/auth/me` | Resolve current auth context |

## Realtime

| Protocol | Endpoint | Description |
| --- | --- | --- |
| `WS` | `/ws/events` | Stream `event.created` and heartbeat envelopes |

## Example auth token response

```json
{
  "access_token": "<jwt>",
  "token_type": "Bearer",
  "expires_at": "2026-03-25T22:30:00Z",
  "expires_in_seconds": 3600,
  "principal": "dashboard-admin",
  "scopes": ["dashboard:write"]
}
```

## Example auth context response

```json
{
  "authenticated": true,
  "auth_required": true,
  "principal": "dashboard-admin",
  "auth_method": "api_key",
  "scopes": ["dashboard:write"],
  "expires_at": "2026-03-25T22:30:00Z"
}
```

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

## Example WebSocket event envelope

```json
{
  "event": "event.created",
  "data": {
    "id": "22222222-2222-2222-2222-222222222222",
    "device_id": "11111111-1111-1111-1111-111111111111",
    "device_name": "Jetson-Line-03",
    "event_type": "detection",
    "confidence": 0.94,
    "label": "cap",
    "frame_ts": "2026-03-25T20:45:00Z",
    "metadata": {
      "bbox": [120, 60, 40, 42]
    },
    "created_at": "2026-03-25T20:45:03Z"
  },
  "sent_at": "2026-03-25T20:45:03Z"
}
```
