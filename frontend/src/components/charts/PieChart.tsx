import { PieChart as RechartsPie, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { ChartPanel } from "./ChartPanel";

const GLOW_COLORS = ["#2563EB", "#38BDF8", "#1D4ED8", "#60A5FA", "#3B82F6", "#64748B", "#94A3B8"];

export function PieChart({
  data,
  nameKey,
  valueKey,
  height = 280,
  donut = true,
  title,
  subtitle,
}: {
  data: Record<string, unknown>[];
  nameKey: string;
  valueKey: string;
  height?: number;
  donut?: boolean;
  title?: string;
  subtitle?: string;
}) {
  return (
    <ChartPanel title={title} subtitle={subtitle}>
      <div className="w-full" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <RechartsPie margin={{ top: 8, right: 8, left: 8, bottom: 8 }}>
            <defs>
              {data.map((_, i) => (
                <filter key={`segGlow-${i}`} id={`segGlow-${i}`}>
                  <feGaussianBlur stdDeviation="2" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              ))}
            </defs>
            <Pie
              data={data}
              dataKey={valueKey}
              nameKey={nameKey}
              cx="50%"
              cy="50%"
              innerRadius={donut ? 55 : 0}
              outerRadius={90}
              paddingAngle={2}
              animationBegin={0}
              animationDuration={1000}
              animationEasing="ease-out"
            >
              {data.map((_, i) => (
                <Cell
                  key={i}
                  fill={GLOW_COLORS[i % GLOW_COLORS.length]}
                  stroke="rgba(37,99,235,0.2)"
                  strokeWidth={2}
                  filter={`url(#segGlow-${i})`}
                />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                background: "#1A1D21",
                border: "1px solid rgba(37,99,235,0.35)",
                borderRadius: 8,
                boxShadow: "0 4px 24px rgba(0,0,0,0.6), 0 0 20px rgba(37,99,235,0.2)",
                fontSize: 12,
                color: "#FFFFFF",
              }}
              itemStyle={{ color: "#FFFFFF", fontFamily: "Consolas, monospace", fontSize: 12 }}
              labelStyle={{ color: "#38BDF8", fontWeight: 600, fontSize: 11 }}
            />
          </RechartsPie>
        </ResponsiveContainer>
      </div>
    </ChartPanel>
  );
}
