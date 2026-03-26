import { describe, expect, it } from "vitest";

import { applyLiveEventToOverview, buildEventsWebSocketUrl } from "@/lib/live-stream";
import type { DashboardOverview, VisionEvent } from "@/types/models";


const baseOverview: DashboardOverview = {
  device_counts: { total: 2, online: 1, offline: 1, error: 0 },
  events_last_24h: [
    { timestamp: "2026-03-25T20:00:00.000Z", count: 1 },
    { timestamp: "2026-03-25T21:00:00.000Z", count: 3 },
  ],
  events_total: 4,
  inspection_pass_rate: 90.5,
  inspection_trend: [{ date: "2026-03-25", pass: 5, fail: 1, uncertain: 0 }],
  recent_events: [],
  devices: [
    {
      id: "device-1",
      name: "Jetson Cell 01",
      type: "jetson",
      location: "Line A",
      status: "offline",
      last_seen: "2026-03-25T20:15:00Z",
      created_at: "2026-03-24T20:15:00Z",
    },
  ],
  latest_inspections: [],
};

const liveEvent: VisionEvent = {
  id: "event-1",
  device_id: "device-1",
  device_name: "Jetson Cell 01",
  event_type: "detection",
  confidence: 0.98,
  label: "crate",
  frame_ts: "2026-03-25T21:18:00.000Z",
  metadata: { lane: 2 },
  created_at: "2026-03-25T21:18:00.000Z",
};


describe("live stream helpers", () => {
  it("builds the websocket url from the API base", () => {
    expect(buildEventsWebSocketUrl("http://localhost:5000/api/v1", undefined)).toBe("ws://localhost:5000/ws/events");
    expect(buildEventsWebSocketUrl("https://example.com/api/v1", undefined)).toBe("wss://example.com/ws/events");
  });

  it("applies a live event into the cached dashboard overview", () => {
    const next = applyLiveEventToOverview(baseOverview, liveEvent);

    expect(next.events_total).toBe(5);
    expect(next.events_last_24h[1].count).toBe(4);
    expect(next.recent_events[0].id).toBe("event-1");
    expect(next.devices[0].status).toBe("online");
    expect(next.devices[0].last_seen).toBe("2026-03-25T21:18:00.000Z");
  });
});
