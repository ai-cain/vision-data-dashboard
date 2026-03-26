import axios from "axios";

import type {
  DashboardOverview,
  Device,
  DeviceDetail,
  EventFilters,
  EventStats,
  InspectionFilters,
  InspectionResult,
  InspectionSummary,
  PaginatedResponse,
  VisionEvent,
} from "@/types/models";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:5000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function fetchOverview() {
  const response = await api.get<DashboardOverview>("/stats/overview");
  return response.data;
}

export async function fetchDevices() {
  const response = await api.get<{ items: Device[]; total: number }>("/devices");
  return response.data;
}

export async function fetchDevice(deviceId: string) {
  const response = await api.get<DeviceDetail>(`/devices/${deviceId}`);
  return response.data;
}

export async function fetchEvents(filters: EventFilters) {
  const response = await api.get<PaginatedResponse<VisionEvent>>("/events", {
    params: filters,
  });
  return response.data;
}

export async function fetchEventStats() {
  const response = await api.get<EventStats>("/events/stats");
  return response.data;
}

export async function fetchInspections(filters: InspectionFilters) {
  const response = await api.get<PaginatedResponse<InspectionResult>>("/inspections", {
    params: filters,
  });
  return response.data;
}

export async function fetchInspectionSummary() {
  const response = await api.get<InspectionSummary>("/inspections/summary");
  return response.data;
}
