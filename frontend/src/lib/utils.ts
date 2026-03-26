import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

import type { DeviceStatus, InspectionOutcome, VisionEvent } from "@/types/models";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDateTime(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function formatShortDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
  }).format(new Date(value));
}

export function formatPercent(value: number) {
  return `${value.toFixed(1)}%`;
}

export function statusTone(status: DeviceStatus) {
  switch (status) {
    case "online":
      return "bg-teal/15 text-teal border-teal/30";
    case "offline":
      return "bg-ink/10 text-ink/70 border-ink/20";
    case "error":
      return "bg-danger/10 text-danger border-danger/30";
  }
}

export function resultTone(result: InspectionOutcome) {
  switch (result) {
    case "pass":
      return "bg-teal/15 text-teal border-teal/30";
    case "fail":
      return "bg-danger/10 text-danger border-danger/30";
    case "uncertain":
      return "bg-lemon/20 text-ink border-lemon/40";
  }
}

export function downloadEventsCsv(events: VisionEvent[]) {
  const header = ["id", "device_name", "event_type", "confidence", "label", "frame_ts"];
  const rows = events.map((event) => [
    event.id,
    event.device_name ?? "",
    event.event_type,
    event.confidence.toString(),
    event.label,
    event.frame_ts,
  ]);
  const csv = [header, ...rows]
    .map((row) => row.map((column) => `"${column.replace(/"/g, '""')}"`).join(","))
    .join("\n");

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const href = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = href;
  link.download = "vision-events.csv";
  link.click();
  URL.revokeObjectURL(href);
}

export function buildConfidenceHistogram(events: VisionEvent[]) {
  const buckets = [
    { range: "0.0-0.2", count: 0 },
    { range: "0.2-0.4", count: 0 },
    { range: "0.4-0.6", count: 0 },
    { range: "0.6-0.8", count: 0 },
    { range: "0.8-1.0", count: 0 },
  ];

  for (const event of events) {
    if (event.confidence < 0.2) buckets[0].count += 1;
    else if (event.confidence < 0.4) buckets[1].count += 1;
    else if (event.confidence < 0.6) buckets[2].count += 1;
    else if (event.confidence < 0.8) buckets[3].count += 1;
    else buckets[4].count += 1;
  }

  return buckets;
}
