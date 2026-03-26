import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatShortDate } from "@/lib/utils";

interface EventsLineChartProps {
  data: Array<{ timestamp: string; count: number }>;
}

export function EventsLineChart({ data }: EventsLineChartProps) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid stroke="rgba(17, 35, 40, 0.08)" strokeDasharray="4 4" />
          <XAxis
            dataKey="timestamp"
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
          <Line
            type="monotone"
            dataKey="count"
            stroke="#db6d34"
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6, fill: "#127c73" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
