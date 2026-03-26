import type { DashboardOverview, Device, EventVolumePoint, VisionEvent } from "@/types/models";

export type LiveConnectionState = "connecting" | "open" | "closed" | "error";

export function buildEventsWebSocketUrl(
  apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:5000/api/v1",
  explicitUrl = import.meta.env.VITE_WS_EVENTS_URL,
) {
  const baseUrl = explicitUrl ?? apiBaseUrl;
  const url = new URL(baseUrl, window.location.origin);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  url.pathname = "/ws/events";
  url.search = "";

  return url.toString();
}

export function isVisionEventPayload(payload: unknown): payload is VisionEvent {
  if (!payload || typeof payload !== "object") {
    return false;
  }

  const candidate = payload as Partial<VisionEvent>;
  return (
    typeof candidate.id === "string" &&
    typeof candidate.device_id === "string" &&
    typeof candidate.event_type === "string" &&
    typeof candidate.confidence === "number" &&
    typeof candidate.label === "string" &&
    typeof candidate.frame_ts === "string" &&
    typeof candidate.created_at === "string"
  );
}

export function applyLiveEventToOverview(current: DashboardOverview, event: VisionEvent): DashboardOverview {
  return {
    ...current,
    events_total: current.events_total + 1,
    events_last_24h: incrementHourlySeries(current.events_last_24h, event.frame_ts),
    recent_events: [event, ...current.recent_events.filter((item) => item.id !== event.id)].slice(0, 10),
    devices: touchDeviceLastSeen(current.devices, event),
  };
}

function incrementHourlySeries(series: EventVolumePoint[], frameTimestamp: string) {
  const eventHour = normalizeHourKey(frameTimestamp);
  return series.map((point) =>
    normalizeHourKey(point.timestamp) === eventHour ? { ...point, count: point.count + 1 } : point,
  );
}

function normalizeHourKey(value: string) {
  const date = new Date(value);
  date.setMinutes(0, 0, 0);
  return date.toISOString();
}

function touchDeviceLastSeen(devices: Device[], event: VisionEvent) {
  return devices.map((device) => {
    if (device.id !== event.device_id) {
      return device;
    }

    return {
      ...device,
      last_seen: event.frame_ts,
      status: device.status === "offline" ? "online" : device.status,
    };
  });
}
