import { startTransition, useEffect, useState } from "react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { useDevice, useDevices } from "@/hooks/useDevices";
import { formatDateTime, statusTone } from "@/lib/utils";

export function DevicesPage() {
  const devices = useDevices();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selectedDevice = useDevice(selectedId);

  useEffect(() => {
    if (!selectedId && devices.data?.items[0]) {
      setSelectedId(devices.data.items[0].id);
    }
  }, [devices.data, selectedId]);

  if (devices.isLoading) {
    return <Card>Loading device fleet...</Card>;
  }

  if (devices.isError || !devices.data) {
    return <Card>Unable to load device fleet right now.</Card>;
  }

  const recentConfidence =
    selectedDevice.data?.recent_events
      .slice()
      .reverse()
      .map((event) => ({
        timestamp: event.frame_ts,
        confidence: Math.round(event.confidence * 100),
      })) ?? [];

  return (
    <div className="grid gap-6 xl:grid-cols-[1.2fr,0.8fr]">
      <Card>
        <CardTitle>Fleet table</CardTitle>
        <CardDescription className="mb-4">
          Click a device to inspect its latest heartbeat and recent event activity.
        </CardDescription>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-ink/10 text-ink/55">
              <tr>
                <th className="pb-3 font-medium">Name</th>
                <th className="pb-3 font-medium">Type</th>
                <th className="pb-3 font-medium">Location</th>
                <th className="pb-3 font-medium">Status</th>
                <th className="pb-3 font-medium">Last seen</th>
              </tr>
            </thead>
            <tbody>
              {devices.data.items.map((device) => {
                const isActive = device.id === selectedId;
                return (
                  <tr
                    key={device.id}
                    className={`cursor-pointer border-b border-ink/8 transition ${isActive ? "bg-ember/10" : "hover:bg-ink/5"}`}
                    onClick={() => {
                      startTransition(() => {
                        setSelectedId(device.id);
                      });
                    }}
                  >
                    <td className="py-3 font-medium text-ink">{device.name}</td>
                    <td className="py-3 capitalize">{device.type}</td>
                    <td className="py-3">{device.location}</td>
                    <td className="py-3">
                      <Badge className={statusTone(device.status)}>{device.status}</Badge>
                    </td>
                    <td className="py-3 text-ink/60">{formatDateTime(device.last_seen)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      <Card>
        <CardTitle>Device detail</CardTitle>
        <CardDescription className="mb-4">
          Recent event confidence and metadata for the selected edge node.
        </CardDescription>

        {selectedDevice.isLoading || !selectedDevice.data ? (
          <div className="rounded-2xl border border-dashed border-ink/15 bg-white/40 p-5 text-sm text-ink/60">
            Select a device to inspect recent telemetry.
          </div>
        ) : (
          <div className="space-y-5">
            <div className="rounded-[24px] bg-panel px-5 py-4 text-white">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.18em] text-white/55">Selected node</p>
                  <h3 className="mt-2 text-2xl font-bold">{selectedDevice.data.name}</h3>
                  <p className="mt-2 text-sm text-white/70">
                    {selectedDevice.data.location} · {selectedDevice.data.type}
                  </p>
                </div>
                <Badge className="border-white/20 bg-white/10 text-white">{selectedDevice.data.status}</Badge>
              </div>
            </div>

            <div className="h-64 rounded-[24px] border border-ink/10 bg-white/65 p-3">
              <ResponsiveContainer>
                <AreaChart data={recentConfidence}>
                  <defs>
                    <linearGradient id="confidenceFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#127c73" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#127c73" stopOpacity={0.05} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(17, 35, 40, 0.08)" strokeDasharray="4 4" />
                  <XAxis dataKey="timestamp" tickFormatter={(value) => formatDateTime(value)} hide />
                  <YAxis stroke="rgba(17, 35, 40, 0.45)" tickLine={false} axisLine={false} />
                  <Tooltip
                    formatter={(value) => [`${value}%`, "Confidence"]}
                    labelFormatter={(label) => formatDateTime(label)}
                    contentStyle={{
                      borderRadius: "18px",
                      border: "1px solid rgba(17, 35, 40, 0.1)",
                      background: "#fffaf3",
                    }}
                  />
                  <Area type="monotone" dataKey="confidence" stroke="#127c73" fill="url(#confidenceFill)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-3">
              {selectedDevice.data.recent_events.slice(0, 6).map((event) => (
                <div key={event.id} className="rounded-2xl border border-ink/10 bg-white/70 px-4 py-3">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="font-semibold capitalize text-ink">
                        {event.label} · {event.event_type}
                      </p>
                      <p className="text-sm text-ink/60">{formatDateTime(event.frame_ts)}</p>
                    </div>
                    <p className="font-mono text-sm text-ink">{Math.round(event.confidence * 100)}%</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
