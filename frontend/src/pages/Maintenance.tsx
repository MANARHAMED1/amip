import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge, statusVariant } from "../components/ui/Badge";
import { DataTable } from "../components/ui/DataTable";
import { AreaChart } from "../components/charts/AreaChart";
import { useApi } from "../hooks/useApi";
import { downloadReport } from "../api/download";
import type { MaintenanceRecord, MaintenanceKPI } from "../types/api";

export default function Maintenance() {
  const list = useApi<MaintenanceRecord[]>("/maintenance/list");
  const kpi = useApi<MaintenanceKPI>("/maintenance/kpi");
  const costEvo = useApi<Record<string, unknown>[]>("/maintenance/cost-evolution");

  return (
    <PageContainer title="Maintenance" description="Suivi des interventions">
      {/* KPI Cards */}
      <div className="grid grid-cols-6 gap-3">
        <KpiCard label="Interventions" value={kpi.data?.stats.nb_interventions ?? 0} icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>} />
        <KpiCard label="Cout total" value={kpi.data ? Math.round(kpi.data.stats.cout_total) : 0} unit="€" />
        <KpiCard label="Cout moyen" value={kpi.data ? Math.round(kpi.data.stats.cout_moyen) : 0} unit="€" />
        <KpiCard label="Preventives" value={kpi.data?.stats.nb_preventive ?? 0} />
        <KpiCard label="Correctives" value={kpi.data?.stats.nb_corrective ?? 0} color="#DC2626" />
        <KpiCard label="Duree moyenne" value={kpi.data ? Math.round(kpi.data.stats.duree_moyenne_min) : 0} unit="min" />
      </div>

      {/* Export */}
      <div className="flex justify-end gap-2">
        <button onClick={() => downloadReport("/api/reports/maintenance/excel", "rapport_maintenance.xlsx")}
           className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#16A34A]/10 text-[#16A34A] text-xs font-semibold hover:bg-[#16A34A]/20 transition-colors cursor-pointer">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Excel
        </button>
        <button onClick={() => downloadReport("/api/reports/maintenance/pdf", "rapport_maintenance.pdf")}
           className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#DC2626]/10 text-[#DC2626] text-xs font-semibold hover:bg-[#DC2626]/20 transition-colors cursor-pointer">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          PDF
        </button>
      </div>

      <div className="grid grid-cols-5 gap-4">
        {/* Cost Evolution */}
        <div className="col-span-2">
          <Card>
            <CardHeader title="Evolution des couts" />
            <CardBody className="p-0">
              {costEvo.data ? (
                <AreaChart
                  data={costEvo.data as unknown as Record<string, unknown>[]}
                  xKey="mois"
                  series={[{ key: "cout_mensuel", name: "Cout mensuel", color: "#2563EB" }]}
                  height={280}
                />
              ) : costEvo.loading ? <div className="h-[280px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
            </CardBody>
          </Card>
        </div>

        {/* By type */}
        <div className="col-span-3">
          <Card>
            <CardHeader title="Repartition par type" />
            <CardBody>
              {kpi.data?.by_type ? (
                <div className="space-y-3">
                  {kpi.data.by_type.map((t, i) => (
                    <div key={i} className="flex items-center justify-between text-sm py-2 border-b border-[#F0F2F5] last:border-0">
                      <span className="text-[var(--color-text-primary)] font-medium">{t.type_maintenance as string}</span>
                      <span className="text-[var(--color-text-secondary)]">{t.nb as number} interventions</span>
                    </div>
                  ))}
                </div>
              ) : kpi.loading ? <div className="h-[200px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
            </CardBody>
          </Card>
        </div>
      </div>

      {/* Records table */}
      <Card>
        <CardHeader title="Interventions" />
        <CardBody className="p-0">
          {list.data ? (
            <DataTable
              columns={[
                { key: "machine_code", header: "Machine", width: "100px", render: (r) => <span className="font-mono font-bold text-xs">{r.machine_code as string}</span> },
                { key: "type_maintenance", header: "Type" },
                { key: "description", header: "Description" },
                { key: "date_debut", header: "Debut" },
                { key: "date_fin", header: "Fin" },
                { key: "duree", header: "Duree (min)", align: "right" },
                { key: "cout", header: "Cout", align: "right", render: (r) => `${(r.cout as number || 0).toFixed(0)}€` },
                { key: "statut", header: "Statut", render: (r) => <Badge variant={statusVariant(r.statut as string)}>{r.statut as string}</Badge> },
              ]}
              data={list.data as unknown as Record<string, unknown>[]}
              pageSize={20}
            />
          ) : list.loading ? (
            <div className="text-center py-12 text-[#8A95A0] text-sm">Loading...</div>
          ) : null}
        </CardBody>
      </Card>
    </PageContainer>
  );
}
