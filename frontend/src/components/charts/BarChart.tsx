import {
  BarChart as RechartsBar,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { ChartPanel } from "./ChartPanel";

const TICK_FILL = "#38BDF8";

export function BarChart({
  data,
  xKey,
  yKey,
  colorKey,
  height = 300,
  horizontal = false,
  barColors,
  title,
  subtitle,
}: {
  data: Record<string, unknown>[];
  xKey: string;
  yKey: string;
  colorKey?: string;
  height?: number;
  horizontal?: boolean;
  barColors?: string[];
  title?: string;
  subtitle?: string;
}) {
  const barId = `barGrad-${xKey}-${yKey}`;
  const getBarColor = (val: number) => {
    if (typeof val !== "number") return "#2563EB";
    return val >= 70 ? `url(#${barId}-high)` : val >= 50 ? `url(#${barId}-mid)` : `url(#${barId}-low)`;
  };
  return (
    <ChartPanel title={title} subtitle={subtitle}>
      <div className="w-full" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <RechartsBar
            data={data}
            layout={horizontal ? "vertical" : "horizontal"}
            margin={{ top: 8, right: 8, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id={`${barId}-high`} x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#1D4ED8" />
                <stop offset="100%" stopColor="#2563EB" />
              </linearGradient>
              <linearGradient id={`${barId}-mid`} x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#1E40AF" />
                <stop offset="100%" stopColor="#3B82F6" />
              </linearGradient>
              <linearGradient id={`${barId}-low`} x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#64748B" />
                <stop offset="100%" stopColor="#94A3B8" />
              </linearGradient>
              <filter id={`${barId}-glow`}>
                <feGaussianBlur stdDeviation="2.5" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
            <XAxis
              type={horizontal ? "number" : "category"}
              dataKey={horizontal ? undefined : xKey}
              tick={{ fontSize: 10, fill: TICK_FILL, fontFamily: "Consolas, monospace" }}
              tickLine={false}
              axisLine={{ stroke: "rgba(255,255,255,0.12)" }}
            />
            <YAxis
              type={horizontal ? "category" : "number"}
              dataKey={horizontal ? xKey : undefined}
              tick={{ fontSize: 10, fill: TICK_FILL, fontFamily: "Consolas, monospace" }}
              tickLine={false}
              axisLine={false}
              width={horizontal ? 80 : 50}
            />
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
              cursor={{ fill: "rgba(255,255,255,0.03)" }}
            />
            <Bar
              dataKey={yKey}
              radius={[4, 4, 0, 0]}
              animationBegin={0}
              animationDuration={800}
              animationEasing="ease-out"
              filter={`url(#${barId}-glow)`}
            >
              {data.map((entry, i) => {
                const colorVal = colorKey ? entry[colorKey] : undefined;
                let fill: string;
                if (typeof colorVal === "number") {
                  fill = getBarColor(colorVal);
                } else {
                  fill = (barColors || ["#2563EB"])[i % (barColors || ["#2563EB"]).length];
                }
                return <Cell key={i} fill={fill} />;
              })}
            </Bar>
          </RechartsBar>
        </ResponsiveContainer>
      </div>
    </ChartPanel>
  );
}
