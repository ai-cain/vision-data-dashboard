import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";

interface PassRateDonutProps {
  passRate: number;
}

export function PassRateDonut({ passRate }: PassRateDonutProps) {
  const data = [
    { name: "Pass", value: passRate },
    { name: "Other", value: Math.max(0, 100 - passRate) },
  ];

  return (
    <div className="relative h-72 w-full">
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            innerRadius={68}
            outerRadius={96}
            paddingAngle={4}
            startAngle={90}
            endAngle={-270}
          >
            <Cell fill="#127c73" />
            <Cell fill="rgba(17, 35, 40, 0.12)" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
        <p className="font-mono text-xs uppercase tracking-[0.18em] text-ink/45">Pass Rate</p>
        <p className="mt-2 text-4xl font-bold text-ink">{passRate.toFixed(1)}%</p>
      </div>
    </div>
  );
}
