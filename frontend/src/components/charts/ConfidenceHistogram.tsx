import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface ConfidenceHistogramProps {
  data: Array<{ range: string; count: number }>;
}

export function ConfidenceHistogram({ data }: ConfidenceHistogramProps) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid stroke="rgba(17, 35, 40, 0.08)" strokeDasharray="4 4" />
          <XAxis dataKey="range" stroke="rgba(17, 35, 40, 0.45)" tickLine={false} axisLine={false} />
          <YAxis allowDecimals={false} stroke="rgba(17, 35, 40, 0.45)" tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{
              borderRadius: "18px",
              border: "1px solid rgba(17, 35, 40, 0.1)",
              background: "#fffaf3",
            }}
          />
          <Bar dataKey="count" fill="#db6d34" radius={[12, 12, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
