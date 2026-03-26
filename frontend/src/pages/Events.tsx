import { useDeferredValue, useState } from "react";
import { Activity, Download, Gauge } from "lucide-react";

import { ConfidenceHistogram } from "@/components/charts/ConfidenceHistogram";
import { StatCard } from "@/components/layout/StatCard";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { useDevices } from "@/hooks/useDevices";
import { useEvents, useEventStats } from "@/hooks/useEvents";
import { buildConfidenceHistogram, downloadEventsCsv, formatDateTime } from "@/lib/utils";
import type { EventFilters } from "@/types/models";

const initialFilters: EventFilters = {
  page: 1,
  per_page: 50,
};

export function EventsPage() {
  const [filters, setFilters] = useState<EventFilters>(initialFilters);
  const deferredFilters = useDeferredValue(filters);
  const events = useEvents(deferredFilters);
  const eventStats = useEventStats();
  const devices = useDevices();

  if (events.isLoading && !events.data) {
    return <Card>Loading event stream...</Card>;
  }

  if (events.isError || !events.data) {
    return <Card>Unable to load event stream right now.</Card>;
  }

  const histogram = buildConfidenceHistogram(events.data.items);

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <StatCard
          label="Filtered Events"
          value={events.data.total.toString()}
          helper="Rows returned by the active filters in the event log."
          icon={<Activity className="h-5 w-5" />}
        />
        <StatCard
          label="Average Confidence"
          value={`${Math.round((eventStats.data?.average_confidence ?? 0) * 100)}%`}
          helper="Global average confidence across the stored event dataset."
          icon={<Gauge className="h-5 w-5" />}
        />
        <Card className="flex flex-col justify-between">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-ink/45">Export</p>
            <p className="mt-3 text-2xl font-bold text-ink">CSV snapshot</p>
            <p className="mt-3 text-sm text-ink/65">
              Export the currently filtered page for further QA or offline review.
            </p>
          </div>
          <Button className="mt-5 w-full" onClick={() => downloadEventsCsv(events.data.items)}>
            <Download className="mr-2 h-4 w-4" />
            Export CSV
          </Button>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.95fr,1.05fr]">
        <Card>
          <CardTitle>Filters</CardTitle>
          <CardDescription className="mb-4">
            Narrow the log by device, event type, and time window.
          </CardDescription>
          <div className="grid gap-3 md:grid-cols-2">
            <Select
              value={filters.device ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  page: 1,
                  device: event.target.value || undefined,
                }))
              }
            >
              <option value="">All devices</option>
              {devices.data?.items.map((device) => (
                <option key={device.id} value={device.id}>
                  {device.name}
                </option>
              ))}
            </Select>

            <Select
              value={filters.type ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  page: 1,
                  type: (event.target.value || undefined) as EventFilters["type"],
                }))
              }
            >
              <option value="">All event types</option>
              <option value="detection">Detection</option>
              <option value="anomaly">Anomaly</option>
              <option value="count">Count</option>
            </Select>

            <Input
              type="datetime-local"
              value={filters.start_date ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  page: 1,
                  start_date: event.target.value || undefined,
                }))
              }
            />
            <Input
              type="datetime-local"
              value={filters.end_date ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  page: 1,
                  end_date: event.target.value || undefined,
                }))
              }
            />
          </div>
        </Card>

        <Card>
          <CardTitle>Confidence distribution</CardTitle>
          <CardDescription className="mb-4">
            Histogram for the currently visible event subset.
          </CardDescription>
          <ConfidenceHistogram data={histogram} />
        </Card>
      </section>

      <section>
        <Card>
          <CardTitle>Event log</CardTitle>
          <CardDescription className="mb-4">
            Paginated stream of detections, anomalies, and count events.
          </CardDescription>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="border-b border-ink/10 text-ink/55">
                <tr>
                  <th className="pb-3 font-medium">Device</th>
                  <th className="pb-3 font-medium">Type</th>
                  <th className="pb-3 font-medium">Label</th>
                  <th className="pb-3 font-medium">Confidence</th>
                  <th className="pb-3 font-medium">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {events.data.items.map((event) => (
                  <tr key={event.id} className="border-b border-ink/8">
                    <td className="py-3">{event.device_name ?? "Unknown"}</td>
                    <td className="py-3">
                      <Badge className="border-ink/15 bg-ink/5 text-ink">{event.event_type}</Badge>
                    </td>
                    <td className="py-3">{event.label}</td>
                    <td className="py-3">{Math.round(event.confidence * 100)}%</td>
                    <td className="py-3 text-ink/60">{formatDateTime(event.frame_ts)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-5 flex items-center justify-between">
            <p className="text-sm text-ink/60">
              Page {events.data.page} · {events.data.total} total records
            </p>
            <div className="flex gap-2">
              <Button
                variant="secondary"
                disabled={events.data.page <= 1}
                onClick={() =>
                  setFilters((current) => ({
                    ...current,
                    page: Math.max(1, (current.page ?? 1) - 1),
                  }))
                }
              >
                Previous
              </Button>
              <Button
                variant="secondary"
                disabled={events.data.page * events.data.per_page >= events.data.total}
                onClick={() =>
                  setFilters((current) => ({
                    ...current,
                    page: (current.page ?? 1) + 1,
                  }))
                }
              >
                Next
              </Button>
            </div>
          </div>
        </Card>
      </section>
    </div>
  );
}
