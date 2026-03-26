import { describe, expect, it } from "vitest";

import { buildConfidenceHistogram, formatPercent } from "@/lib/utils";


describe("utils", () => {
  it("formats percentages with one decimal place", () => {
    expect(formatPercent(98.234)).toBe("98.2%");
  });

  it("builds a confidence histogram from events", () => {
    const histogram = buildConfidenceHistogram([
      {
        id: "1",
        device_id: "d1",
        device_name: "Device A",
        event_type: "detection",
        confidence: 0.12,
        label: "cap",
        frame_ts: "2026-03-25T20:00:00Z",
        metadata: {},
        created_at: "2026-03-25T20:00:00Z",
      },
      {
        id: "2",
        device_id: "d1",
        device_name: "Device A",
        event_type: "count",
        confidence: 0.84,
        label: "bottle",
        frame_ts: "2026-03-25T20:05:00Z",
        metadata: {},
        created_at: "2026-03-25T20:05:00Z",
      },
    ]);

    expect(histogram[0].count).toBe(1);
    expect(histogram[4].count).toBe(1);
  });
});
