import { startTransition, useState } from "react";
import { AlertTriangle, Image as ImageIcon, ShieldCheck } from "lucide-react";

import { InspectionTrendChart } from "@/components/charts/InspectionTrendChart";
import { StatCard } from "@/components/layout/StatCard";
import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Select } from "@/components/ui/select";
import { useDevices } from "@/hooks/useDevices";
import { useInspectionSummary, useInspections } from "@/hooks/useInspections";
import { formatDateTime, resultTone } from "@/lib/utils";
import type { InspectionFilters, InspectionResult } from "@/types/models";

const initialFilters: InspectionFilters = {
  page: 1,
  per_page: 25,
};

export function InspectionsPage() {
  const [filters, setFilters] = useState<InspectionFilters>(initialFilters);
  const [selectedInspection, setSelectedInspection] = useState<InspectionResult | null>(null);
  const inspections = useInspections(filters);
  const summary = useInspectionSummary();
  const devices = useDevices();

  if (inspections.isLoading && !inspections.data) {
    return <Card>Loading inspection records...</Card>;
  }

  if (inspections.isError || !inspections.data || !summary.data) {
    return <Card>Unable to load inspection records right now.</Card>;
  }

  const failCount = summary.data.count_by_result.fail ?? 0;

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <StatCard
          label="Total Inspections"
          value={summary.data.total_inspections.toString()}
          helper="Stored inspection jobs currently available through the API."
          icon={<ShieldCheck className="h-5 w-5" />}
        />
        <StatCard
          label="Pass Rate"
          value={`${summary.data.pass_rate.toFixed(1)}%`}
          helper="Share of jobs marked as pass across the full inspection dataset."
          icon={<ShieldCheck className="h-5 w-5" />}
        />
        <StatCard
          label="Failed Jobs"
          value={failCount.toString()}
          helper="Jobs with an explicit fail outcome and a likely defect classification."
          icon={<AlertTriangle className="h-5 w-5" />}
        />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.05fr,0.95fr]">
        <Card>
          <CardTitle>Inspection trend</CardTitle>
          <CardDescription className="mb-4">
            Pass and fail movement over the last seven daily buckets.
          </CardDescription>
          <InspectionTrendChart data={summary.data.trend} />
        </Card>

        <Card>
          <CardTitle>Filters and defect mix</CardTitle>
          <CardDescription className="mb-4">
            Narrow results and review the most common failure causes.
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
              value={filters.result ?? ""}
              onChange={(event) =>
                setFilters((current) => ({
                  ...current,
                  page: 1,
                  result: (event.target.value || undefined) as InspectionFilters["result"],
                }))
              }
            >
              <option value="">All outcomes</option>
              <option value="pass">Pass</option>
              <option value="fail">Fail</option>
              <option value="uncertain">Uncertain</option>
            </Select>
          </div>

          <div className="mt-5 space-y-3">
            {Object.entries(summary.data.defect_breakdown).length > 0 ? (
              Object.entries(summary.data.defect_breakdown).map(([defect, count]) => (
                <div
                  key={defect}
                  className="flex items-center justify-between rounded-2xl border border-ink/10 bg-white/70 px-4 py-3"
                >
                  <span className="capitalize text-ink">{defect.replace(/_/g, " ")}</span>
                  <span className="font-mono text-sm text-ink">{count}</span>
                </div>
              ))
            ) : (
              <div className="rounded-2xl border border-dashed border-ink/15 bg-white/40 p-5 text-sm text-ink/60">
                No defect records yet.
              </div>
            )}
          </div>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.15fr,0.85fr]">
        <Card>
          <CardTitle>Inspection table</CardTitle>
          <CardDescription className="mb-4">
            Click a row to inspect the image path placeholder and batch detail.
          </CardDescription>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="border-b border-ink/10 text-ink/55">
                <tr>
                  <th className="pb-3 font-medium">Job</th>
                  <th className="pb-3 font-medium">Device</th>
                  <th className="pb-3 font-medium">Result</th>
                  <th className="pb-3 font-medium">Defect</th>
                  <th className="pb-3 font-medium">Score</th>
                  <th className="pb-3 font-medium">Created</th>
                </tr>
              </thead>
              <tbody>
                {inspections.data.items.map((inspection) => (
                  <tr
                    key={inspection.id}
                    className="cursor-pointer border-b border-ink/8 transition hover:bg-ink/5"
                    onClick={() =>
                      startTransition(() => {
                        setSelectedInspection(inspection);
                      })
                    }
                  >
                    <td className="py-3 font-medium text-ink">{inspection.job_id}</td>
                    <td className="py-3">{inspection.device_name ?? "Unknown"}</td>
                    <td className="py-3">
                      <Badge className={resultTone(inspection.result)}>{inspection.result}</Badge>
                    </td>
                    <td className="py-3">{inspection.defect_type ?? "None"}</td>
                    <td className="py-3">{Math.round(inspection.score * 100)}%</td>
                    <td className="py-3 text-ink/60">{formatDateTime(inspection.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        <Card>
          <CardTitle>Image path viewer</CardTitle>
          <CardDescription className="mb-4">
            Placeholder view for the captured frame path associated with a selected inspection.
          </CardDescription>

          {selectedInspection ? (
            <div className="space-y-4">
              <div className="rounded-[28px] border border-dashed border-ink/15 bg-gradient-to-br from-white to-sand p-8 text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-ink/10 bg-white">
                  <ImageIcon className="h-8 w-8 text-ink/55" />
                </div>
                <p className="mt-4 text-sm text-ink/60">Frame placeholder</p>
                <p className="mt-2 font-mono text-xs text-ink/50">{selectedInspection.image_path}</p>
              </div>

              <div className="space-y-3 rounded-[24px] bg-panel px-5 py-4 text-white">
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.18em] text-white/55">Selected job</p>
                  <h3 className="mt-2 text-2xl font-bold">{selectedInspection.job_id}</h3>
                </div>
                <p className="text-sm text-white/70">{selectedInspection.device_name}</p>
                <Badge className="w-fit border-white/20 bg-white/10 text-white">{selectedInspection.result}</Badge>
              </div>
            </div>
          ) : (
            <div className="rounded-2xl border border-dashed border-ink/15 bg-white/40 p-5 text-sm text-ink/60">
              Select an inspection row to inspect its image path and metadata.
            </div>
          )}
        </Card>
      </section>
    </div>
  );
}
