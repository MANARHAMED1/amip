import { useEffect, useState, useCallback, useRef } from "react";

export interface Notification {
  type: "machine_down" | "machine_restored" | "maintenance_due";
  machine_code: string;
  machine_name?: string;
  timestamp: string;
  message: string;
  date?: string;
  type_label?: string;
}

export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host;
    const ws = new WebSocket(`${protocol}//${host}/ws/notifications`);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => {
      setConnected(false);
      setTimeout(connect, 5000);
    };
    ws.onmessage = (event) => {
      try {
        const msg: Notification = JSON.parse(event.data);
        setNotifications((prev) => [msg, ...prev].slice(0, 50));
      } catch {
        // ignore malformed messages
      }
    };
  }, []);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  const dismiss = useCallback((index: number) => {
    setNotifications((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const clearAll = useCallback(() => setNotifications([]), []);

  return { notifications, connected, dismiss, clearAll };
}
