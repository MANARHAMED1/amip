import { useState } from "react";
import clsx from "clsx";
import type { AlertItem } from "../../types/api";

export function AlertPanel({ alerts, onAlertClick }: { alerts: AlertItem[]; onAlertClick?: (alert: AlertItem) => void }) {
  const [expanded, setExpanded] = useState(false);
  const critical = alerts.filter((a) => a.type === "CRITICAL");
  const warning = alerts.filter((a) => a.type === "WARNING");
  const displayLimit = expanded ? alerts.length : 5;
  const display = [...critical, ...warning].slice(0, displayLimit);

  return (
    <div className="bg-white border border-[#E2E5E9] rounded-xl shadow-sm">
      <div className="flex items-center justify-between px-5 py-4 border-b border-[#E2E5E9]">
        <div className="flex items-center gap-3">
          <h3 className="text-[#1C1E21] font-bold text-sm">Alerts</h3>
          {critical.length > 0 && (
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[rgba(198,40,40,0.1)] text-[#C62828] border border-[rgba(198,40,40,0.2)]">
              {critical.length} Critical
            </span>
          )}
          {warning.length > 0 && (
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[rgba(237,108,2,0.1)] text-[#ED6C02] border border-[rgba(237,108,2,0.2)]">
              {warning.length} Warning
            </span>
          )}
        </div>
      </div>

      <div className="max-h-[420px] overflow-y-auto px-4 py-3 space-y-2">
        {display.length === 0 && (
          <div className="text-center py-6 text-[#8A95A0] text-sm">No active alerts</div>
        )}
        {display.map((alert, i) => {
          const isCritical = alert.type === "CRITICAL";
          return (
            <div
              key={i}
              onClick={() => onAlertClick?.(alert)}
              className={clsx(
                "flex items-start gap-3 px-4 py-3 rounded-lg border-l-[3px] transition-all cursor-pointer",
                isCritical
                  ? "bg-[#FDF6F6] border-l-[#C62828] hover:bg-[#FBEFEF]"
                  : "bg-[#FFFBF5] border-l-[#ED6C02] hover:bg-[#FEF6EA]"
              )}
            >
              <div
                className={clsx(
                  "shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold",
                  isCritical ? "bg-[#C62828] text-white" : "bg-[#ED6C02] text-white"
                )}
              >
                !
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-[#1C1E21] text-xs font-semibold">{alert.message}</div>
                {alert.detail && (
                  <div className="text-[#5A6872] text-[11px] mt-0.5">{alert.detail}</div>
                )}
              </div>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="shrink-0 text-[#8A95A0] mt-1">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </div>
          );
        })}
      </div>

      {alerts.length > 5 && (
        <div className="border-t border-[#E2E5E9] px-5 py-3">
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-[var(--color-copper)] hover:text-[var(--color-copper-dark)] font-semibold transition-colors"
          >
            {expanded ? "Show less" : `View all (${alerts.length})`}
          </button>
        </div>
      )}
    </div>
  );
}
