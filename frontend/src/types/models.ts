export type DeviceType = "jetson" | "esp32" | "raspi";
export type DeviceStatus = "online" | "offline" | "error";
export type EventType = "detection" | "anomaly" | "count";
export type InspectionOutcome = "pass" | "fail" | "uncertain";

export interface Device {
  id: string;
  name: string;
  type: DeviceType;
  location: string;
  status: DeviceStatus;
  last_seen: string;
  created_at: string;
}

export interface DeviceEventSnapshot {
  id: string;
  event_type: EventType;
  confidence: number;
  label: string;
  frame_ts: string;
  metadata: Record<string, unknown>;
}

export interface DeviceDetail extends Device {
  recent_events: DeviceEventSnapshot[];
}

export interface VisionEvent {
  id: string;
  device_id: string;
  device_name: string | null;
  event_type: EventType;
  confidence: number;
  label: string;
  frame_ts: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface InspectionResult {
  id: string;
  device_id: string;
  device_name: string | null;
  job_id: string;
  result: InspectionOutcome;
  defect_type: string | null;
  score: number;
  image_path: string;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  per_page: number;
  total: number;
}

export interface EventVolumePoint {
  timestamp: string;
  count: number;
}

export interface InspectionTrendPoint {
  date: string;
  pass: number;
  fail: number;
  uncertain: number;
}

export interface EventStats {
  total_events: number;
  average_confidence: number;
  count_by_type: Record<string, number>;
  count_by_device: Record<string, number>;
  recent_volume: EventVolumePoint[];
}

export interface InspectionSummary {
  total_inspections: number;
  pass_rate: number;
  count_by_result: Record<string, number>;
  defect_breakdown: Record<string, number>;
  trend: InspectionTrendPoint[];
}

export interface DashboardOverview {
  device_counts: {
    total: number;
    online: number;
    offline: number;
    error: number;
  };
  events_last_24h: EventVolumePoint[];
  events_total: number;
  inspection_pass_rate: number;
  inspection_trend: InspectionTrendPoint[];
  recent_events: VisionEvent[];
  devices: Device[];
  latest_inspections: InspectionResult[];
}

export interface LiveStreamEnvelope {
  event: string;
  data: unknown;
  sent_at?: string;
}

export interface EventFilters {
  device?: string;
  type?: EventType | "";
  start_date?: string;
  end_date?: string;
  page?: number;
  per_page?: number;
}

export interface InspectionFilters {
  device?: string;
  result?: InspectionOutcome | "";
  page?: number;
  per_page?: number;
}
