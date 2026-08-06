export function ProgressBar({
  value,
  max = 100,
  color,
  height = 6,
  animate = true,
}: {
  value: number;
  max?: number;
  color?: string;
  height?: number;
  animate?: boolean;
}) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const barColor = color ?? "#2563EB";

  return (
    <div
      className="w-full rounded-full overflow-hidden"
      style={{ height, backgroundColor: "var(--surface-progress-track)" }}
    >
      <div
        className="h-full rounded-full transition-all"
        style={{
          width: `${pct}%`,
          backgroundColor: barColor,
          transition: animate ? "width 0.6s cubic-bezier(0.4,0,0.2,1)" : "none",
        }}
      />
    </div>
  );
}
