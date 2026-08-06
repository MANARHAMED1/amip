import { type ReactNode } from "react";
import clsx from "clsx";

export function Card({
  children,
  className,
  hover = true,
  borderLeft,
}: {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  borderLeft?: string;
}) {
  return (
    <div
      className={clsx(
        "bg-white border border-[#E2E5E9] rounded-lg shadow-sm transition-all duration-200",
        hover && "hover:shadow-md hover:-translate-y-0.5",
        className
      )}
      style={borderLeft ? { borderLeft: `4px solid ${borderLeft}` } : undefined}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  title,
  subtitle,
  icon,
  action,
}: {
  title: string;
  subtitle?: string;
  icon?: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="flex items-center justify-between px-5 py-4 border-b border-[#E2E5E9]">
      <div className="flex items-center gap-3">
        {icon && <span className="text-[var(--color-copper)]">{icon}</span>}
        <div>
          <div className="text-[#1C1E21] font-semibold text-sm">{title}</div>
          {subtitle && <div className="text-[#8A95A0] text-xs mt-0.5">{subtitle}</div>}
        </div>
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

export function CardBody({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={clsx("p-5", className)}>{children}</div>;
}
