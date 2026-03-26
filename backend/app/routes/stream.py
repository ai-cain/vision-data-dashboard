from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from flask import Flask
from simple_websocket import ConnectionClosed

from app.extensions import sock
from app.schemas.common import isoformat_value
from app.services.live_stream_service import live_event_stream


def register_stream_routes(app: Flask) -> None:
    @sock.route("/ws/events")
    def events_stream(ws: Any) -> None:
        subscription = live_event_stream.subscribe()
        try:
            _send_message(
                ws,
                {
                    "event": "stream.connected",
                    "data": {
                        "subscribers": live_event_stream.subscriber_count(),
                        "server_time": isoformat_value(datetime.now(timezone.utc)),
                    },
                    "sent_at": isoformat_value(datetime.now(timezone.utc)),
                },
            )

            while True:
                message = subscription.next_message(timeout=15.0)
                if message is None:
                    _send_message(
                        ws,
                        {
                            "event": "stream.heartbeat",
                            "data": {"server_time": isoformat_value(datetime.now(timezone.utc))},
                            "sent_at": isoformat_value(datetime.now(timezone.utc)),
                        },
                    )
                    continue
                _send_message(ws, message)
        except ConnectionClosed:
            app.logger.debug("WebSocket client disconnected from /ws/events")
        finally:
            subscription.close()


def _send_message(ws: Any, message: dict[str, object]) -> None:
    ws.send(json.dumps(message))
