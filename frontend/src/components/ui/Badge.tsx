import { type ReactNode } from "react";
import clsx from "clsx";

type BadgeVariant = "success" | "warning" | "danger" | "info" | "neutral";

const colors: Record<BadgeVariant, { bg: string; text: string; dot: string }> = {
  success: { bg: "bg-[rgba(37,99,235,0.1)]", text: "text-[#2563EB]", dot: "bg-[#2563EB] shadow-[0_0_6px_rgba(37,99,235,0.5)]" },
  warning: { bg: "bg-[rgba(56,189,248,0.1)]", text: "text-[#38BDF8]", dot: "bg-[#38BDF8] shadow-[0_0_6px_rgba(56,189,248,0.5)]" },
  danger:  { bg: "bg-[rgba(220,38,38,0.08)]", text: "text-[#DC2626]", dot: "bg-[#DC2626] shadow-[0_0_6px_rgba(220,38,38,0.5)]" },
  info:    { bg: "bg-[rgba(148,163,184,0.1)]", text: "text-[#94A3B8]", dot: "bg-[#94A3B8] shadow-[0_0_6px_rgba(148,163,184,0.5)]" },
  neutral: { bg: "bg-[rgba(100,116,139,0.08)]", text: "text-[#64748B]", dot: "bg-[#64748B]" },
};

export function Badge({
  children,
  variant = "neutral",
  dot = true,
  className,
}: {
  children: ReactNode;
  variant?: BadgeVariant;
  dot?: boolean;
  className?: string;
}) {
  const c = colors[variant];
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border transition-all duration-150",
        c.bg,
        c.text,
        `border-[${c.dot}20]`,
        className
      )}
    >
      {dot && <span className={clsx("w-1.5 h-1.5 rounded-full", c.dot)} />}
      {children}
    </span>
  );
}

export function statusVariant(status: string): BadgeVariant {
  const s = status.toUpperCase();
  if (["TERMINE", "NORMAL", "OK", "OUI"].includes(s)) return "success";
  if (["EN_COURS", "RUNNING", "ACTIVE"].includes(s)) return "warning";
  if (["STOPPED", "MAINTENANCE", "EN_ATTENTE", "BAS"].includes(s)) return "info";
  if (["BROKEN", "CRITIQUE", "EN_RETARD", "CRITICAL", "ANNULE"].includes(s)) return "danger";
  if (["SURSTOCK", "WARNING"].includes(s)) return "neutral";
  return "neutral";
}
