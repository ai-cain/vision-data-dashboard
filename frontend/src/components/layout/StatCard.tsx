import type { ReactNode } from "react";

import { Card, CardDescription } from "@/components/ui/card";

interface StatCardProps {
  label: string;
  value: string;
  helper: string;
  icon: ReactNode;
}

export function StatCard({ label, value, helper, icon }: StatCardProps) {
  return (
    <Card className="overflow-hidden bg-paper">
      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-ink/45">{label}</p>
          <p className="mt-3 text-3xl font-bold text-ink">{value}</p>
        </div>
        <div className="rounded-2xl border border-ink/10 bg-ink/5 p-3 text-ink">{icon}</div>
      </div>
      <CardDescription>{helper}</CardDescription>
    </Card>
  );
}
