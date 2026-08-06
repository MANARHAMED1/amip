import { useState, useEffect, useCallback } from "react";
import { getJSON } from "../api/client";

export function useApi<T = unknown>(path: string | null, params?: Record<string, string | number | undefined>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    if (!path) { setLoading(false); return; }
    setLoading(true);
    setError(null);
    try {
      const result = await getJSON<T>(path, params);
      setData(result);
    } catch (err: unknown) {
      setError((err as { message?: string })?.message || "Failed to load data");
    } finally {
      setLoading(false);
    }
  }, [path, JSON.stringify(params)]);

  useEffect(() => { fetch(); }, [fetch]);

  return { data, loading, error, refetch: fetch };
}
