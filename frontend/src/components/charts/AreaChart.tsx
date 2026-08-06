import {
  AreaChart as RechartsArea,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Line,
  ComposedChart,
} from "recharts";
import { ChartPanel } from "./ChartPanel";

const GLOW_COLORS = ["#2563EB", "#64748B", "#38BDF8", "#1D4ED8"];
const TICK_FILL = "#38BDF8";

export function AreaChart({
  data,
  xKey,
  series,
  height = 280,
  title,
  subtitle,
}: {
  data: Record<string, unknown>[];
  xKey: string;
  series: { key: string; name: string; color?: string }[];
  height?: number;
  title?: string;
  subtitle?: string;
}) {
  return (
    <ChartPanel title={title} subtitle={subtitle}>
      <div className="w-full" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <RechartsArea data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
            <defs>
              {series.map((s, i) => {
                const c = s.color || GLOW_COLORS[i % GLOW_COLORS.length];
                return (
                  <linearGradient key={s.key} id={`areaFill-${s.key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={c} stopOpacity={0.35} />
                    <stop offset="100%" stopColor={c} stopOpacity={0} />
                  </linearGradient>
                );
              })}
              {series.map((s, i) => {
                const c = s.color || GLOW_COLORS[i % GLOW_COLORS.length];
                return (
                  <filter key={`glow-${s.key}`} id={`areaGlow-${s.key}`}>
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feMerge>
                      <feMergeNode in="blur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                );
              })}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
            <XAxis
              dataKey={xKey}
              tick={{ fontSize: 10, fill: TICK_FILL, fontFamily: "Consolas, monospace" }}
              tickLine={false}
              axisLine={{ stroke: "rgba(255,255,255,0.12)" }}
              minTickGap={20}
            />
            <YAxis
              tick={{ fontSize: 10, fill: TICK_FILL, fontFamily: "Consolas, monospace" }}
              tickLine={false}
              axisLine={false}
              width={50}
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
              cursor={{ stroke: "rgba(255,255,255,0.15)", strokeDasharray: "3 3" }}
            />
            {series.map((s, i) => {
              const c = s.color || GLOW_COLORS[i % GLOW_COLORS.length];
              return (
                <Area
                  key={s.key}
                  type="monotone"
                  dataKey={s.key}
                  name={s.name}
                  stroke={c}
                  strokeWidth={2.5}
                  fill={`url(#areaFill-${s.key})`}
                  animationBegin={i * 100}
                  animationDuration={1000}
                  animationEasing="ease-out"
                  dot={false}
                  activeDot={{ r: 4, strokeWidth: 2, stroke: c, fill: "#1A1D21" }}
                  filter={`url(#areaGlow-${s.key})`}
                />
              );
            })}
          </RechartsArea>
        </ResponsiveContainer>
      </div>
    </ChartPanel>
  );
}

export function AreaChartMulti({
  data,
  xKey,
  series,
  height = 280,
  title,
  subtitle,
}: {
  data: Record<string, unknown>[];
  xKey: string;
  series: { key: string; name: string; color?: string }[];
  height?: number;
  title?: string;
  subtitle?: string;
}) {
  return (
    <ChartPanel title={title} subtitle={subtitle}>
      <div className="w-full" style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
            <defs>
              {series.map((s, i) => {
                const c = s.color || GLOW_COLORS[i % GLOW_COLORS.length];
                return (
                  <filter key={`glow-${s.key}`} id={`multiGlow-${s.key}`}>
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feMerge>
                      <feMergeNode in="blur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                );
              })}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
            <XAxis
              dataKey={xKey}
              tick={{ fontSize: 10, fill: TICK_FILL, fontFamily: "Consolas, monospace" }}
              tickLine={false}
              axisLine={{ stroke: "rgba(255,255,255,0.12)" }}
              minTickGap={20}
            />
            <YAxis
              tick={{ fontSize: 10, fill: TICK_FILL, fontFamily: "Consolas, monospace" }}
              tickLine={false}
              axisLine={false}
              width={50}
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
              cursor={{ stroke: "rgba(255,255,255,0.15)", strokeDasharray: "3 3" }}
            />
            {series.map((s, i) => {
              const c = s.color || GLOW_COLORS[i % GLOW_COLORS.length];
              return (
                <Line
                  key={s.key}
                  type="monotone"
                  dataKey={s.key}
                  name={s.name}
                  stroke={c}
                  strokeWidth={2.5}
                  dot={false}
                  activeDot={{ r: 4, strokeWidth: 2, stroke: c, fill: "#1A1D21" }}
                  animationBegin={i * 100}
                  animationDuration={1000}
                  animationEasing="ease-out"
                  filter={`url(#multiGlow-${s.key})`}
                />
              );
            })}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </ChartPanel>
  );
}
