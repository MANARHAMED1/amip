import { useState, useMemo } from "react";
import clsx from "clsx";

interface Column<T> {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
  sortable?: boolean;
  width?: string;
  align?: "left" | "right" | "center";
}

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  pageSize = 20,
  searchable = true,
  searchKeys,
  stickyHeader = true,
}: {
  columns: Column<T>[];
  data: T[];
  pageSize?: number;
  searchable?: boolean;
  searchKeys?: string[];
  stickyHeader?: boolean;
}) {
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");
  const [page, setPage] = useState(0);

  const safeData = data || [];
  const filtered = useMemo(() => {
    if (!search) return safeData;
    const keys = searchKeys || columns.map((c) => c.key);
    const q = search.toLowerCase();
    return safeData.filter((row) =>
      keys.some((k) => String(row[k] ?? "").toLowerCase().includes(q))
    );
  }, [safeData, search, searchKeys, columns]);

  const sorted = useMemo(() => {
    if (!sortKey) return filtered;
    return [...filtered].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      const cmp =
        typeof av === "number" && typeof bv === "number"
          ? av - bv
          : String(av ?? "").localeCompare(String(bv ?? ""));
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [filtered, sortKey, sortDir]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const paged = sorted.slice(page * pageSize, (page + 1) * pageSize);

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  return (
    <div className="bg-white border border-[var(--color-card-border)] rounded-lg overflow-hidden shadow-sm">
      {searchable && (
        <div className="px-4 py-3 border-b border-[var(--color-card-border)]">
          <input
            type="text"
            placeholder="Search..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(0); }}
            className="input-field max-w-xs text-sm"
          />
        </div>
      )}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr
              className={clsx(
                "bg-[var(--surface-row-alt)] border-b border-[var(--color-card-border)]",
                stickyHeader && "sticky top-0 z-10"
              )}
            >
              {columns.map((col) => (
                <th
                  key={col.key}
                  className={clsx(
                    "px-4 py-3 text-[var(--color-text-secondary)] text-xs font-semibold uppercase tracking-[0.04em]",
                    col.sortable !== false && "cursor-pointer select-none hover:text-[var(--color-text-primary)] transition-colors",
                    col.align === "right" && "text-right",
                    col.align === "center" && "text-center"
                  )}
                  style={col.width ? { width: col.width } : undefined}
                  onClick={() => col.sortable !== false && handleSort(col.key)}
                >
                  <span className="inline-flex items-center gap-1">
                    {col.header}
                    {sortKey === col.key && (
                      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                        {sortDir === "asc" ? <polyline points="18 15 12 9 6 15" /> : <polyline points="6 9 12 15 18 9" />}
                      </svg>
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map((row, i) => (
              <tr
                key={i}
                className={clsx(
                  "border-b border-[var(--color-card-border)] transition-colors duration-100 hover:bg-[rgba(37,99,235,0.04)]",
                  i % 2 === 1 && "bg-[var(--surface-row-alt)]"
                )}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={clsx(
                      "px-4 py-3 text-[var(--color-text-primary)]",
                      col.align === "right" && "text-right",
                      col.align === "center" && "text-center"
                    )}
                  >
                    {col.render ? col.render(row) : String(row[col.key] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
            {paged.length === 0 && (
              <tr>
                <td colSpan={columns.length} className="px-4 py-8 text-center text-[var(--color-text-muted)]">
                  No results found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 border-t border-[var(--color-card-border)] text-xs text-[var(--color-text-secondary)]">
          <span>
            {sorted.length} result{sorted.length !== 1 ? "s" : ""}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
              className="px-2.5 py-1 rounded hover:bg-[var(--surface-hover)] disabled:opacity-30 transition-colors"
            >
              Prev
            </button>
            {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
              const start = Math.max(0, Math.min(page - 3, totalPages - 7));
              const p = start + i;
              if (p >= totalPages) return null;
              return (
                <button
                  key={p}
                  onClick={() => setPage(p)}
                  className={clsx(
                    "px-2.5 py-1 rounded transition-colors",
                          p === page ? "bg-[var(--color-copper)] text-white" : "hover:bg-[var(--surface-hover)]"
                  )}
                >
                  {p + 1}
                </button>
              );
            })}
            <button
              onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
              disabled={page >= totalPages - 1}
              className="px-2.5 py-1 rounded hover:bg-[var(--surface-hover)] disabled:opacity-30 transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
