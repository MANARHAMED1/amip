import { useEffect, useState, useRef } from "react";
import clsx from "clsx";
import { useNotifications } from "../../hooks/useNotifications";

export default function Header({
  title,
  description,
  alertCount,
  onAlertClick,
}: {
  title: string;
  description?: string;
  alertCount?: number;
  onAlertClick?: () => void;
}) {
  const [now, setNow] = useState(new Date());
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const notifRef = useRef<HTMLDivElement>(null);
  const { notifications, connected, dismiss, clearAll } = useNotifications();

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 30000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const user = (() => {
    try {
      return JSON.parse(localStorage.getItem("amip_user") || "{}");
    } catch {
      return {};
    }
  })();

  const dateStr = now.toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" });
  const timeStr = now.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });

  const handleSignOut = () => {
    localStorage.removeItem("amip_token");
    localStorage.removeItem("amip_user");
    window.location.href = "/login";
  };

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setNotifOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const unreadCount = notifications.length;

  const notifIcon = (type: string) => {
    switch (type) {
      case "machine_down": return <span className="text-[#DC2626]">&#9888;</span>;
      case "machine_restored": return <span className="text-[#16A34A]">&#10003;</span>;
      case "maintenance_due": return <span className="text-[#2563EB]">&#128197;</span>;
      default: return <span>&#128276;</span>;
    }
  };

  return (
    <header className="bg-[var(--color-graphite)] bg-[length:200%_200%] rounded-xl px-6 py-4 flex items-center justify-between shadow-sm" style={{ backgroundImage: "var(--gradient-header)" }}>
      <div className="flex items-center gap-4">
        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-[rgba(255,255,255,0.12)]">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 21h18" /><path d="M5 21V7l5 3V5l5 3V5l3 3v10" /><path d="M9 21v-4h2v4" /><path d="M15 21v-4h2v4" />
          </svg>
        </div>
        <div>
          <h1 className="text-white text-lg font-extrabold tracking-tight">{title}</h1>
          {description && <p className="text-white/70 text-xs mt-0.5">{description}</p>}
        </div>
      </div>
      <div className="flex items-center gap-4">
        {alertCount !== undefined && alertCount > 0 && (
          <button
            onClick={onAlertClick}
            className="relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[rgba(198,40,40,0.15)] text-[#FFCDD2] text-xs font-semibold hover:bg-[rgba(198,40,40,0.25)] transition-colors"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
              <path d="M13.73 21a2 2 0 0 1-3.46 0" />
            </svg>
            <span>{alertCount}</span>
          </button>
        )}
        <div className="relative" ref={notifRef}>
          <button onClick={() => setNotifOpen(!notifOpen)} className="relative flex items-center justify-center w-9 h-9 rounded-lg bg-[rgba(255,255,255,0.1)] text-white hover:bg-[rgba(255,255,255,0.18)] transition-colors">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
              <path d="M13.73 21a2 2 0 0 1-3.46 0" />
            </svg>
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 flex items-center justify-center bg-[#DC2626] text-white text-[9px] font-bold rounded-full">{unreadCount > 9 ? "9+" : unreadCount}</span>
            )}
          </button>
          {notifOpen && (
            <div className="absolute right-0 top-full mt-2 w-80 bg-white border border-[var(--color-card-border)] rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
              <div className="flex items-center justify-between px-4 py-3 border-b border-[var(--color-card-border)]">
                <span className="text-xs font-bold text-[var(--color-text-primary)]">Notifications</span>
                  {notifications.length > 0 && (
                  <button onClick={clearAll} className="text-[10px] text-[#2563EB] hover:underline">Tout effacer</button>
                )}
              </div>
              {notifications.length === 0 ? (
                <div className="px-4 py-6 text-center text-xs text-[#8A95A0]">
                  {connected ? "Aucune notification" : "Connexion perdue..."}
                </div>
              ) : (
                notifications.map((n, i) => (
                  <div key={i} className="flex items-start gap-3 px-4 py-3 border-b border-[var(--color-card-border)] last:border-b-0 hover:bg-[#F4F6F9] transition-colors">
                    <div className="mt-0.5">{notifIcon(n.type)}</div>
                    <div className="flex-1 min-w-0">
                      <div className="text-xs text-[var(--color-text-primary)] leading-tight whitespace-pre-wrap">{n.message}</div>
                      <div className="text-[10px] text-[#8A95A0] mt-1">{new Date(n.timestamp).toLocaleString("fr-FR")}</div>
                    </div>
                    <button onClick={() => dismiss(i)} className="text-[#8A95A0] hover:text-[#DC2626] transition-colors text-xs leading-none">&times;</button>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
        <div className="text-right">
          <div className="text-white text-xs font-semibold">{dateStr}</div>
          <div className="text-white/60 text-[11px]">{timeStr}</div>
        </div>
        <div className="relative" ref={menuRef}>
          <button onClick={() => setMenuOpen(!menuOpen)} className="flex items-center justify-center w-9 h-9 rounded-lg bg-[rgba(255,255,255,0.1)] text-white text-xs font-bold hover:bg-[rgba(255,255,255,0.18)] transition-colors cursor-pointer">
            {(user.full_name || user.username || "A")[0].toUpperCase()}
          </button>
          {menuOpen && (
            <div className="absolute right-0 top-full mt-2 w-48 bg-white border border-[var(--color-card-border)] rounded-lg shadow-lg z-50 overflow-hidden">
              <div className="px-4 py-3 border-b border-[var(--color-card-border)]">
                <div className="text-xs font-semibold text-[var(--color-text-primary)]">{user.full_name || user.username || "User"}</div>
                <div className="text-[11px] text-[var(--color-text-muted)]">{user.role || ""}</div>
              </div>
              <button onClick={handleSignOut} className="flex items-center gap-2 w-full px-4 py-2.5 text-xs text-[#C62828] hover:bg-[#FDF6F6] transition-colors">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                  <polyline points="16 17 21 12 16 7" />
                  <line x1="21" y1="12" x2="9" y2="12" />
                </svg>
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
