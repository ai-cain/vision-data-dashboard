from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from queue import Empty, Full, Queue
from threading import Lock
from typing import Any
from uuid import uuid4

from app.schemas.common import isoformat_value


StreamPayload = dict[str, object]


@dataclass(slots=True)
class StreamSubscription:
    subscriber_id: str
    queue: Queue[StreamPayload]
    broker: "EventStreamBroker"

    def next_message(self, timeout: float = 15.0) -> StreamPayload | None:
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None

    def close(self) -> None:
        self.broker.unsubscribe(self.subscriber_id)


class EventStreamBroker:
    def __init__(self, max_queue_size: int = 100) -> None:
        self._lock = Lock()
        self._max_queue_size = max_queue_size
        self._subscribers: dict[str, Queue[StreamPayload]] = {}

    def subscribe(self) -> StreamSubscription:
        subscriber_id = str(uuid4())
        queue: Queue[StreamPayload] = Queue(maxsize=self._max_queue_size)
        with self._lock:
            self._subscribers[subscriber_id] = queue
        return StreamSubscription(subscriber_id=subscriber_id, queue=queue, broker=self)

    def unsubscribe(self, subscriber_id: str) -> None:
        with self._lock:
            self._subscribers.pop(subscriber_id, None)

    def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        message: StreamPayload = {
            "event": event_name,
            "data": payload,
            "sent_at": isoformat_value(datetime.now(timezone.utc)),
        }
        with self._lock:
            subscriber_queues = list(self._subscribers.values())

        for queue in subscriber_queues:
            self._push_message(queue, message)

    def subscriber_count(self) -> int:
        with self._lock:
            return len(self._subscribers)

    @staticmethod
    def _push_message(queue: Queue[StreamPayload], message: StreamPayload) -> None:
        try:
            queue.put_nowait(message)
        except Full:
            try:
                queue.get_nowait()
            except Empty:
                return
            queue.put_nowait(message)


live_event_stream = EventStreamBroker()
