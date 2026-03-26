import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatShortDate } from "@/lib/utils";

interface InspectionTrendChartProps {
  data: Array<{ date: string; pass: number; fail: number; uncertain: number }>;
}

export function InspectionTrendChart({ data }: InspectionTrendChartProps) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="passFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#127c73" stopOpacity={0.35} />
              <stop offset="95%" stopColor="#127c73" stopOpacity={0.05} />
            </linearGradient>
            <linearGradient id="failFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#b53f2f" stopOpacity={0.28} />
              <stop offset="95%" stopColor="#b53f2f" stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="rgba(17, 35, 40, 0.08)" strokeDasharray="4 4" />
          <XAxis
            dataKey="date"
            stroke="rgba(17, 35, 40, 0.45)"
            tickFormatter={formatShortDate}
            tickLine={false}
            axisLine={false}
          />
          <YAxis allowDecimals={false} stroke="rgba(17, 35, 40, 0.45)" tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{
              borderRadius: "18px",
              border: "1px solid rgba(17, 35, 40, 0.1)",
              background: "#fffaf3",
            }}
          />
          <Area type="monotone" dataKey="pass" stroke="#127c73" fill="url(#passFill)" strokeWidth={2.5} />
          <Area type="monotone" dataKey="fail" stroke="#b53f2f" fill="url(#failFill)" strokeWidth={2.5} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
