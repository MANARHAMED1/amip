import { useState } from "react";
import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge, statusVariant } from "../components/ui/Badge";
import { ProgressBar } from "../components/ui/ProgressBar";
import { BarChart } from "../components/charts/BarChart";
import { DataTable } from "../components/ui/DataTable";
import { useApi } from "../hooks/useApi";
import type { InventoryOverview, InventoryAlert } from "../types/api";
import clsx from "clsx";

type Tab = "matieres" | "outils" | "pieces";

export default function Inventory() {
  const [tab, setTab] = useState<Tab>("matieres");
  const [selectedItem, setSelectedItem] = useState<Record<string, unknown> | null>(null);

  const overview = useApi<InventoryOverview>("/inventory/overview");
  const alerts = useApi<InventoryAlert[]>("/inventory/alerts");
  const matieres = useApi<Record<string, unknown>[]>("/inventory/matieres");
  const outils = useApi<Record<string, unknown>[]>("/inventory/outils");
  const pieces = useApi<Record<string, unknown>[]>("/inventory/pieces");
  const consumption = useApi<Record<string, unknown>[]>("/inventory/consumption-trend");
  const stockout = useApi<Record<string, unknown>>("/inventory/stockout-forecast");

  const tabs: { key: Tab; label: string; count: number }[] = [
    { key: "matieres", label: "Matieres premieres", count: overview.data?.matieres.total ?? 0 },
    { key: "outils", label: "Outils", count: overview.data?.outils.total ?? 0 },
    { key: "pieces", label: "Pieces", count: overview.data?.pieces.total ?? 0 },
  ];

  const criticalAlerts = (alerts.data || []).filter((a) => a.statut === "CRITIQUE");

  const stockColor = (statut: string) => {
    switch (statut) {
      case "CRITIQUE": return "#DC2626";
      case "BAS": return "#F59E0B";
      case "SURSTOCK": return "#64748B";
      default: return "#2563EB";
    }
  };

  const currentData = tab === "matieres" ? matieres : tab === "outils" ? outils : pieces;

  const closeDetail = () => setSelectedItem(null);

  return (
    <PageContainer title="Inventaire" description="Etat des stocks par categorie">
      {/* Overview KPIs */}
      <div className="grid grid-cols-6 gap-3">
        <KpiCard label="Matieres" value={overview.data?.matieres.total ?? 0} />
        <KpiCard label="Dont critiques" value={overview.data?.matieres.critiques ?? 0} color="#C62828" />
        <KpiCard label="Valeur stock" value={overview.data ? Math.round(overview.data.matieres.valeur_totale) : 0} unit="€" />
        <KpiCard label="Outils" value={overview.data?.outils.total ?? 0} />
        <KpiCard label="Outils critiques" value={overview.data?.outils.critiques ?? 0} color="#C62828" />
        <KpiCard label="Pieces stock" value={overview.data?.pieces.stock_total ?? 0} />
      </div>

      {/* Critical alerts */}
      {criticalAlerts.length > 0 && (
        <div className="space-y-1.5">
          <div className="text-[11px] font-semibold uppercase tracking-[0.05em] text-[#C62828]">Alertes stock critique ({criticalAlerts.length})</div>
          <div className="grid grid-cols-2 gap-2">
            {criticalAlerts.slice(0, 6).map((a, i) => (
              <button key={i} onClick={() => { setTab((a.type === "OUTIL" ? "outils" : "matieres") as Tab); setSelectedItem(null); }} className="flex items-center justify-between px-3 py-2 rounded-lg bg-[#FDF6F6] border border-[rgba(198,40,40,0.15)] border-l-[3px] border-l-[#C62828] hover:bg-[#FBEFEF] transition-colors text-left">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="font-mono font-bold text-[11px] text-[var(--color-copper)]">{a.code}</span>
                  <span className="text-[11px] text-[#5A6872] truncate">{a.designation}</span>
                </div>
                <span className="text-[11px] text-[#C62828] font-semibold whitespace-nowrap ml-2">{a.quantite_stock} / {a.seuil_alerte}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 border-b border-[#E2E5E9]">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => { setTab(t.key); setSelectedItem(null); }}
            className={clsx(
              "px-4 py-2.5 text-xs font-semibold border-b-2 transition-colors",
              tab === t.key ? "border-[var(--color-copper)] text-[var(--color-copper)]" : "border-transparent text-[#8A95A0] hover:text-[#5A6872]"
            )}
          >
            {t.label} <span className="text-[11px] opacity-60">({t.count})</span>
          </button>
        ))}
      </div>

      {/* Data table */}
      <div className={clsx("grid gap-4", selectedItem ? "grid-cols-5" : "grid-cols-1")}>
        <div className={selectedItem ? "col-span-3" : ""}>
          <Card>
            <CardHeader title={tabs.find((t) => t.key === tab)?.label || ""} />
            <CardBody className="p-0">
              <DataTable
                columns={
                  tab === "matieres"
                    ? [
                        { key: "code", header: "Code", width: "100px", render: (r) => <span className="font-mono font-bold text-[11px]">{r.code as string}</span> },
                        { key: "designation", header: "Designation" },
                        { key: "type_matiere", header: "Type" },
                        { key: "quantite_stock", header: "Stock", align: "right", render: (r) => <span style={{ color: stockColor(r.statut as string) }} className="font-semibold">{(r.quantite_stock as number || 0).toFixed(0)}</span> },
                        { key: "seuil_alerte", header: "Seuil", align: "right" },
                        { key: "emplacement", header: "Emp." },
                        { key: "statut", header: "Statut", render: (r) => <Badge variant={statusVariant(r.statut as string)}>{r.statut as string}</Badge> },
                        { key: "_actions", header: "", width: "50px", sortable: false, render: (r) => (
                          <button onClick={() => setSelectedItem(r)} className="text-[var(--color-copper)] hover:text-[var(--color-copper-dark)] text-[11px] underline underline-offset-2 decoration-dotted">
                            Detail
                          </button>
                        )},
                      ]
                    : tab === "outils"
                    ? [
                        { key: "code", header: "Code", width: "100px", render: (r) => <span className="font-mono font-bold text-[11px]">{r.code as string}</span> },
                        { key: "designation", header: "Designation" },
                        { key: "type_outil", header: "Type" },
                        { key: "diametre", header: "Diam.", align: "right", render: (r) => `${(r.diametre as number || 0).toFixed(1)}mm` },
                        { key: "quantite_stock", header: "Stock", align: "right", render: (r) => <span style={{ color: stockColor(r.statut as string) }} className="font-semibold">{(r.quantite_stock as number || 0).toFixed(0)}</span> },
                        { key: "seuil_alerte", header: "Seuil", align: "right" },
                        { key: "statut", header: "Statut", render: (r) => <Badge variant={statusVariant(r.statut as string)}>{r.statut as string}</Badge> },
                        { key: "_actions", header: "", width: "50px", sortable: false, render: (r) => (
                          <button onClick={() => setSelectedItem(r)} className="text-[var(--color-copper)] hover:text-[var(--color-copper-dark)] text-[11px] underline underline-offset-2 decoration-dotted">
                            Detail
                          </button>
                        )},
                      ]
                    : [
                        { key: "reference", header: "Ref", width: "110px", render: (r) => <span className="font-mono font-bold text-[11px]">{r.reference as string}</span> },
                        { key: "designation", header: "Designation" },
                        { key: "famille", header: "Famille" },
                        { key: "quantite_stock", header: "Stock", align: "right", render: (r) => <span className="font-semibold">{(r.quantite_stock as number || 0).toFixed(0)}</span> },
                        { key: "valeur_stock", header: "Valeur", align: "right", render: (r) => `${(r.valeur_stock as number || 0).toFixed(0)}€` },
                        { key: "emplacement", header: "Emp." },
                        { key: "_actions", header: "", width: "50px", sortable: false, render: (r) => (
                          <button onClick={() => setSelectedItem(r)} className="text-[var(--color-copper)] hover:text-[var(--color-copper-dark)] text-[11px] underline underline-offset-2 decoration-dotted">
                            Detail
                          </button>
                        )},
                      ]
                }
                data={currentData.data || []}
                pageSize={15}
              />
            </CardBody>
          </Card>
        </div>

        {/* Item detail panel */}
        {selectedItem && (
          <div className="col-span-2">
            <Card>
              <CardHeader
                title={(selectedItem.code as string) || (selectedItem.reference as string) || ""}
                subtitle={(selectedItem.designation as string) || ""}
                action={<button onClick={closeDetail} className="text-xs text-[#8A95A0] hover:text-[#C62828] transition-colors">Close</button>}
              />
              <CardBody className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div className="px-3 py-2 rounded-lg bg-[#F8FAFB]">
                    <div className="text-[11px] text-[#8A95A0]">Stock actuel</div>
                    <div className="text-lg font-bold font-mono" style={{ color: stockColor(selectedItem.statut as string) }}>
                      {(selectedItem.quantite_stock as number || 0).toFixed(0)}
                    </div>
                  </div>
                  <div className="px-3 py-2 rounded-lg bg-[#F8FAFB]">
                    <div className="text-[11px] text-[#8A95A0]">Seuil d'alerte</div>
                    <div className="text-lg font-bold font-mono">{(selectedItem.seuil_alerte as number || 0).toFixed(0)}</div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-[#64748B]">Niveau stock</span>
                    <span className={clsx("font-semibold", selectedItem.statut === "CRITIQUE" && "text-[#C62828]", selectedItem.statut === "BAS" && "text-[#ED6C02]", selectedItem.statut === "SURSTOCK" && "text-[#A8A296]")}>
                      {selectedItem.statut as string}
                    </span>
                  </div>
                  <ProgressBar
                    value={(selectedItem.quantite_stock as number) || 0}
                    max={Math.max((selectedItem.seuil_alerte as number || 1) * 3, (selectedItem.quantite_stock as number || 0))}
                    color={stockColor(selectedItem.statut as string)}
                  />
                </div>

                {(selectedItem.type_matiere as string) && (
                  <div className="text-xs text-[#5A6872] grid grid-cols-2 gap-y-1">
                    <span>Type: {selectedItem.type_matiere as string}</span>
                    {(selectedItem.nuance as string) && <span>Nuance: {selectedItem.nuance as string}</span>}
                    {(selectedItem.prix_kg as number) != null && <span>Prix/kg: {(selectedItem.prix_kg as number).toFixed(2)}€</span>}
                    {(selectedItem.prix_revient as number) != null && <span>Prix revient: {(selectedItem.prix_revient as number).toFixed(2)}€</span>}
                  </div>
                )}

                {(selectedItem.emplacement as string) && (
                  <div className="text-xs text-[#5A6872]">Emplacement: {selectedItem.emplacement as string}</div>
                )}
              </CardBody>
            </Card>
          </div>
        )}
      </div>

      {/* Stockout forecast */}
      {stockout.data && stockout.data.items && (stockout.data.items as Record<string, unknown>[]).length > 0 ? (
        <div className="px-4 py-3 rounded-lg border border-[rgba(220,38,38,0.15)] bg-[rgba(220,38,38,0.04)] border-l-[4px] border-l-[#DC2626] text-xs">
          <div className="flex items-center gap-2 mb-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" strokeWidth="2" className="shrink-0"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>
            <span className="font-bold text-[#1C1E21]">Prevision rupture de stock — {new Date().toLocaleDateString('fr-FR')}</span>
          </div>
          <div className="grid grid-cols-3 gap-2">
            {(stockout.data.items as Record<string, unknown>[]).slice(0, 6).map((item, i) => {
              const months = item.months_to_depletion as number;
              const critical = months < 0.5;
              return (
                <div key={i} className={`flex items-center justify-between px-2 py-1.5 rounded ${critical ? 'bg-white border border-[rgba(220,38,38,0.2)]' : 'bg-white/60'}`}>
                  <div>
                    <div className="font-mono font-bold text-[10px]">{item.code as string}</div>
                    <div className="text-[9px] text-[#8A95A0] truncate max-w-[100px]">{item.designation as string}</div>
                  </div>
                  <span className={`font-mono font-bold text-[10px] ${critical ? 'text-[#DC2626]' : 'text-[#F59E0B]'}`}>
                    {item.depletion_date_est as string}
                  </span>
                </div>
              );
            })}
          </div>
          <div className="mt-1 text-[#8A95A0]">Projection lineaire basee sur consommation moyenne des 6 derniers mois.</div>
        </div>
      ) : stockout.data && stockout.data.items ? (
        <div className="px-4 py-3 rounded-lg border border-[rgba(37,99,235,0.2)] bg-[rgba(37,99,235,0.04)] text-xs text-[#8A95A0]">Aucune prevision de rupture disponible.</div>
      ) : null}

      {/* Consumption trend */}
      <Card>
        <CardHeader title="Tendance consommation mensuelle" />
        <CardBody className="p-0">
          {consumption.data ? (
            <BarChart data={consumption.data as unknown as Record<string, unknown>[]} xKey="mois" yKey="consommation" height={250} />
          ) : consumption.loading ? <div className="h-[250px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
        </CardBody>
      </Card>
    </PageContainer>
  );
}
