import type { ReactNode } from "react";

export function ChartPanel({ children, title, subtitle }: { children: ReactNode; title?: string; subtitle?: string }) {
  return (
    <div className="rounded-lg bg-[var(--color-graphite)] border border-[var(--color-graphite-border)] shadow-[inset_0_0_30px_rgba(0,0,0,0.35)] p-4">
      {title && (
        <div className="flex items-center gap-2 mb-3">
          <span className="w-1.5 h-1.5 rounded-full bg-[var(--color-copper)] shadow-[0_0_6px_var(--color-copper-glow)]" />
          <span className="text-[var(--color-text-on-dark)] text-[10px] uppercase tracking-[0.12em] font-semibold">{title}</span>
          {subtitle && <span className="text-[var(--color-text-on-dark-secondary)] text-[10px] ml-auto">{subtitle}</span>}
        </div>
      )}
      {children}
    </div>
  );
}
