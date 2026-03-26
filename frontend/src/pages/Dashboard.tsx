import { Activity, AlertTriangle, Cpu, ShieldCheck } from "lucide-react";

import { EventsLineChart } from "@/components/charts/EventsLineChart";
import { InspectionTrendChart } from "@/components/charts/InspectionTrendChart";
import { PassRateDonut } from "@/components/charts/PassRateDonut";
import { StatCard } from "@/components/layout/StatCard";
import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { useDashboard } from "@/hooks/useDashboard";
import { formatDateTime, statusTone } from "@/lib/utils";

export function DashboardPage() {
  const overview = useDashboard();

  if (overview.isLoading) {
    return <Card>Loading dashboard metrics...</Card>;
  }

  if (overview.isError || !overview.data) {
    return <Card>Unable to load dashboard data right now.</Card>;
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Devices Online"
          value={overview.data.device_counts.online.toString()}
          helper={`${overview.data.device_counts.total} total devices reporting into the system.`}
          icon={<Cpu className="h-5 w-5" />}
        />
        <StatCard
          label="Devices in Error"
          value={overview.data.device_counts.error.toString()}
          helper="Units that need inspection or recent heartbeat verification."
          icon={<AlertTriangle className="h-5 w-5" />}
        />
        <StatCard
          label="Events Total"
          value={overview.data.events_total.toString()}
          helper="Historical detections, anomalies, and count records in storage."
          icon={<Activity className="h-5 w-5" />}
        />
        <StatCard
          label="Inspection Pass Rate"
          value={`${overview.data.inspection_pass_rate.toFixed(1)}%`}
          helper="Blended pass rate across the latest inspection dataset."
          icon={<ShieldCheck className="h-5 w-5" />}
        />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.5fr,1fr]">
        <Card>
          <CardTitle>Events in the last 24 hours</CardTitle>
          <CardDescription className="mb-4">
            Rolling event activity coming from edge devices and inspection jobs.
          </CardDescription>
          <EventsLineChart data={overview.data.events_last_24h} />
        </Card>

        <Card className="flex flex-col">
          <CardTitle>Inspection quality pulse</CardTitle>
          <CardDescription>Quick view of the current pass rate across all recorded jobs.</CardDescription>
          <div className="mt-4 flex-1">
            <PassRateDonut passRate={overview.data.inspection_pass_rate} />
          </div>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.2fr,0.8fr]">
        <Card>
          <CardTitle>Recent events</CardTitle>
          <CardDescription className="mb-4">
            The latest detections and anomalies arriving from the field.
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
                {overview.data.recent_events.map((event) => (
                  <tr key={event.id} className="border-b border-ink/8">
                    <td className="py-3">{event.device_name ?? "Unknown"}</td>
                    <td className="py-3 capitalize">{event.event_type}</td>
                    <td className="py-3">{event.label}</td>
                    <td className="py-3">{Math.round(event.confidence * 100)}%</td>
                    <td className="py-3 text-ink/60">{formatDateTime(event.frame_ts)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        <Card>
          <CardTitle>Fleet snapshot</CardTitle>
          <CardDescription className="mb-4">
            Status and most recent heartbeat of every registered edge device.
          </CardDescription>
          <div className="space-y-3">
            {overview.data.devices.map((device) => (
              <div
                key={device.id}
                className="flex items-center justify-between rounded-2xl border border-ink/10 bg-white/70 px-4 py-3"
              >
                <div>
                  <p className="font-semibold text-ink">{device.name}</p>
                  <p className="text-sm text-ink/60">
                    {device.location} · {device.type}
                  </p>
                </div>
                <div className="text-right">
                  <Badge className={statusTone(device.status)}>{device.status}</Badge>
                  <p className="mt-2 text-xs text-ink/45">{formatDateTime(device.last_seen)}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </section>

      <section>
        <Card>
          <CardTitle>Inspection trend</CardTitle>
          <CardDescription className="mb-4">
            Daily movement of pass and fail results over the latest week.
          </CardDescription>
          <InspectionTrendChart data={overview.data.inspection_trend} />
        </Card>
      </section>
    </div>
  );
}
