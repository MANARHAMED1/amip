import { useEffect, useRef, useState } from "react";
import clsx from "clsx";

function useCountUp(end: number, duration = 800, enabled = true) {
  const [value, setValue] = useState(0);
  const raf = useRef<number>(0);

  useEffect(() => {
    if (!enabled) { setValue(end); return; }
    const start = performance.now();
    const from = 0;
    function tick(now: number) {
      const t = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - t, 3);
      setValue(from + (end - from) * ease);
      if (t < 1) raf.current = requestAnimationFrame(tick);
    }
    raf.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf.current);
  }, [end, duration, enabled]);

  return end >= 1000 ? Math.round(value).toLocaleString() : value.toFixed(1);
}

export function KpiCard({
  label,
  value,
  unit = "",
  delta,
  subtitle,
  icon,
  sparkline,
  color = "#1C1E21",
  className,
}: {
  label: string;
  value: number;
  unit?: string;
  delta?: number;
  subtitle?: string;
  icon?: React.ReactNode;
  sparkline?: number[];
  color?: string;
  className?: string;
}) {
  const displayVal = useCountUp(value);

  return (
    <div
        className={clsx(
        "card-lift bg-white border border-[var(--color-card-border)] rounded-lg px-5 py-4 shadow-sm",
        "transition-all duration-200 hover:shadow-md hover:-translate-y-0.5",
        "flex flex-col",
        className
      )}
    >
      <div className="flex items-center justify-between mb-1">
        <span className="text-[var(--color-text-secondary)] text-[10px] font-semibold uppercase tracking-[0.06em]">
          {label}
        </span>
        {icon && <span className="text-[var(--color-copper)]">{icon}</span>}
      </div>
      <div className="flex items-baseline gap-1.5">
        <span
          className="text-2xl font-bold leading-tight tabular-nums"
          style={{ fontFamily: "'Consolas','Courier New',monospace", color }}
        >
          {displayVal}
          {unit && <span className="text-sm font-semibold text-[var(--color-text-secondary)] ml-0.5">{unit}</span>}
        </span>
        {subtitle && <span className="text-[var(--color-text-muted)] text-[10px] ml-auto">{subtitle}</span>}
        {delta !== undefined && (
          <span
            className={clsx(
              "text-xs font-semibold font-mono flex items-center gap-0.5",
              delta >= 0 ? "text-[#2563EB]" : "text-[#DC2626]"
            )}
          >
            <svg
              width="10"
              height="10"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              {delta >= 0 ? (
                <>
                  <line x1="12" y1="19" x2="12" y2="5" />
                  <polyline points="5 12 12 5 19 12" />
                </>
              ) : (
                <>
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <polyline points="19 12 12 19 5 12" />
                </>
              )}
            </svg>
            {Math.abs(delta).toFixed(1)}%
          </span>
        )}
      </div>
        {sparkline && sparkline.length > 1 && (
        <svg className="w-full h-6 mt-2" viewBox={`0 0 ${sparkline.length - 1} 100`} preserveAspectRatio="none" style={{ filter: "drop-shadow(0 0 3px rgba(37,99,235,0.4))" }}>
          <defs>
            <linearGradient id={`spark-${label.replace(/\s/g, "")}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#2563EB" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#2563EB" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            d={sparkline
              .map((v, i) => `${i === 0 ? "M" : "L"} ${i} ${100 - v}`)
              .join(" ")}
            fill="none"
            stroke="#2563EB"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            filter="url(#sparkGlow)"
          />
          <path
            d={`${sparkline.map((v, i) => `${i === 0 ? "M" : "L"} ${i} ${100 - v}`).join(" ")} L ${sparkline.length - 1} 100 L 0 100 Z`}
            fill={`url(#spark-${label.replace(/\s/g, "")})`}
          />
        </svg>
      )}
    </div>
  );
}
