export function GanttChart({
  data,
  height = 260,
}: {
  data: Record<string, unknown>[];
  height?: number;
}) {
  if (!data || data.length === 0) {
    return <div className="text-center py-8 text-[var(--color-text-on-dark-secondary)] text-sm">No timeline data</div>;
  }

  const minTime = Math.min(...data.map((d) => new Date(d.date_debut as string).getTime()));
  const maxTime = Math.max(...data.map((d) => new Date(d.date_fin as string).getTime()));
  const range = maxTime - minTime || 1;

  const barHeight = 24;
  const gap = 8;
  const totalHeight = data.length * (barHeight + gap) + 20;

  return (
    <svg width="100%" height={Math.max(height, totalHeight)} style={{ minHeight: totalHeight }}>
      <defs>
        <filter id="ganttGlow">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      {data.map((item, i) => {
        const start = new Date(item.date_debut as string).getTime();
        const end = new Date(item.date_fin as string).getTime();
        const x = ((start - minTime) / range) * 100;
        const w = Math.max(1, ((end - start) / range) * 100);
        const y = i * (barHeight + gap) + 10;
        const status = (item.statut as string) || "";
        const color =
          status === "TERMINE" ? "#2563EB" :
          status === "EN_COURS" ? "#38BDF8" :
          status === "EN_ATTENTE" ? "#64748B" :
          "#1D4ED8";

        return (
          <g key={i}>
            <text
              x={0}
              y={y + barHeight / 2 + 4}
              fill="var(--color-text-on-dark)"
              fontSize="10"
              fontFamily="system-ui, sans-serif"
            >
              {(item.phase_name as string) || `Phase ${i + 1}`}
            </text>
            <rect
              x={`${x}%`}
              y={y}
              width={`${w}%`}
              height={barHeight}
              rx={4}
              fill={color}
              opacity={0.85}
              filter="url(#ganttGlow)"
            >
              <title>{`${item.phase_name} (${status}): ${Math.round(w)}%`}</title>
            </rect>
          </g>
        );
      })}
    </svg>
  );
}
