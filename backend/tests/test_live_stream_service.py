from __future__ import annotations

from app.services.live_stream_service import EventStreamBroker


def test_stream_broker_delivers_messages_to_subscribers() -> None:
    broker = EventStreamBroker()
    subscription = broker.subscribe()

    try:
        broker.publish("event.created", {"id": "evt-1", "label": "crate"})
        message = subscription.next_message(timeout=0.1)
    finally:
        subscription.close()

    assert message is not None
    assert message["event"] == "event.created"
    assert message["data"] == {"id": "evt-1", "label": "crate"}
    assert "sent_at" in message
