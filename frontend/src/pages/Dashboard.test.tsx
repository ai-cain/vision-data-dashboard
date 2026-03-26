import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";


const useDashboardMock = vi.fn();
const useDashboardLiveStreamMock = vi.fn();

vi.mock("@/hooks/useDashboard", () => ({
  useDashboard: () => useDashboardMock(),
}));
vi.mock("@/hooks/useDashboardLiveStream", () => ({
  useDashboardLiveStream: () => useDashboardLiveStreamMock(),
}));
vi.mock("@/components/charts/EventsLineChart", () => ({
  EventsLineChart: () => <div>events-line-chart</div>,
}));
vi.mock("@/components/charts/InspectionTrendChart", () => ({
  InspectionTrendChart: () => <div>inspection-trend-chart</div>,
}));
vi.mock("@/components/charts/PassRateDonut", () => ({
  PassRateDonut: ({ passRate }: { passRate: number }) => <div>{passRate.toFixed(1)}%</div>,
}));

import { DashboardPage } from "@/pages/Dashboard";


describe("DashboardPage", () => {
  it("renders dashboard metrics from query data", () => {
    useDashboardLiveStreamMock.mockReturnValue("open");
    useDashboardMock.mockReturnValue({
      isLoading: false,
      isError: false,
      data: {
        device_counts: { total: 5, online: 3, offline: 1, error: 1 },
        events_last_24h: [{ timestamp: "2026-03-25T20:00:00Z", count: 2 }],
        events_total: 42,
        inspection_pass_rate: 91.4,
        inspection_trend: [{ date: "2026-03-25", pass: 4, fail: 1, uncertain: 0 }],
        recent_events: [],
        devices: [],
        latest_inspections: [],
      },
    });

    render(<DashboardPage />);

    expect(screen.getByText("Events Total")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
    expect(screen.getAllByText("91.4%")).toHaveLength(2);
    expect(screen.getByText("Live Connected")).toBeInTheDocument();
  });
});
