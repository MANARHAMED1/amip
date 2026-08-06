import { useState } from "react";
import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge, statusVariant } from "../components/ui/Badge";
import { ProgressBar } from "../components/ui/ProgressBar";
import { DataTable } from "../components/ui/DataTable";
import { useApi } from "../hooks/useApi";
import { getJSON } from "../api/client";
import type { Tool } from "../types/api";
import clsx from "clsx";

export default function ToolPage() {
  const list = useApi<Tool[]>("/tool/list");
  const [selected, setSelected] = useState("");
  const wearPred = useApi<Record<string, unknown>>(selected ? `/tool/${selected}/wear-prediction` : null);
  const [detailData, setDetailData] = useState<Record<string, unknown> | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const openDetail = async (code: string) => {
    setSelected(code);
    setDetailLoading(true);
    setDetailData(null);
    try {
      const data = await getJSON<Record<string, unknown>>(`/tool/${code}`);
      setDetailData(data);
    } catch {
      setDetailData(null);
    } finally {
      setDetailLoading(false);
    }
  };

  const closeDetail = () => { setSelected(""); setDetailData(null); };

  const toolsData = list.data || [];

  const replacable = toolsData.filter(
    (t) => t.pct_usure >= 80 || t.indicateur_remplacement !== "OK"
  ).length;

  return (
    <PageContainer title="Outillage" description="Gestion des outils et suivi d'usure">
      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-3">
        <KpiCard label="Total outils" value={toolsData.length} icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>} />
        <KpiCard label="Disponibles" value={toolsData.filter(t => t.disponible).length} color="#2563EB" />
        <KpiCard label="Usure > 80%" value={toolsData.filter(t => t.pct_usure >= 80).length} color="#C62828" subtitle="necessite remplacement" />
        <KpiCard label="En alerte" value={replacable} color="#ED6C02" subtitle="usure elevee ou indisponible" />
      </div>

      <div className={clsx("grid gap-4", selected ? "grid-cols-5" : "grid-cols-1")}>
        {/* Tool Table */}
        <div className={selected ? "col-span-3" : ""}>
          <Card>
            <CardHeader title="Outils" subtitle={selected ? "Click code to view detail" : undefined} />
            <CardBody className="p-0">
              {list.loading ? (
                <div className="h-[300px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div>
              ) : toolsData.length > 0 ? (
                <DataTable
                  columns={[
                    { key: "code", header: "Code", width: "100px", render: (r) => (
                      <button onClick={() => openDetail(r.code as string)} className="font-mono font-bold text-xs text-[var(--color-copper)] hover:text-[var(--color-copper-light)] transition-colors underline underline-offset-2 decoration-dotted">
                        {r.code as string}
                      </button>
                    )},
                    { key: "designation", header: "Designation" },
                    { key: "type_outil", header: "Type" },
                    { key: "pct_usure", header: "Usure", align: "right", render: (r) => {
                      const p = r.pct_usure as number;
                      return (
                        <div className="flex items-center gap-2 justify-end">
                          <div className="w-16"><ProgressBar value={p} /></div>
                          <span className="font-mono text-xs font-semibold text-[var(--color-text-secondary)]">{p.toFixed(0)}%</span>
                        </div>
                      );
                    }},
                    { key: "duree_vie_restante", header: "Vie restante", align: "right", render: (r) => <span className="font-mono text-xs">{r.duree_vie_restante as number} cycles</span> },
                    { key: "disponible", header: "Dispo", render: (r) => <Badge variant={r.disponible ? "success" : "info"}>{r.disponible ? "Oui" : "Non"}</Badge> },
                    { key: "indicateur_remplacement", header: "Statut", render: (r) => <Badge variant={r.indicateur_remplacement === "OK" ? "success" : r.indicateur_remplacement === "SURVEILLANCE" ? "warning" : "danger"}>{(r.indicateur_remplacement as string)?.replace(/_/g, " ")}</Badge> },
                  ]}
                  data={toolsData as unknown as Record<string, unknown>[]}
                  pageSize={20}
                />
              ) : list.error ? (
                <div className="h-[200px] flex items-center justify-center text-[#DC2626] text-sm">{list.error}</div>
              ) : null}
            </CardBody>
          </Card>
        </div>

        {/* Tool Detail Panel */}
        {selected && (
          <div className="col-span-2 space-y-3">
            {detailLoading ? (
              <Card><CardBody><div className="text-center py-8 text-[#8A95A0] text-sm">Loading detail...</div></CardBody></Card>
            ) : detailData ? (
              <>
                <Card>
                  <CardHeader
                    title="Details outil"
                    subtitle={selected}
                    action={<button onClick={closeDetail} className="text-xs text-[#8A95A0] hover:text-[#C62828] transition-colors px-2 py-1 rounded hover:bg-[#FDF6F6]">Close</button>}
                  />
                  <CardBody className="space-y-3 text-sm">
                    <div className="grid grid-cols-2 gap-x-4 gap-y-2">
                      {[
                        ["Code", (detailData.tool as Record<string, unknown>)?.code as string],
                        ["Designation", (detailData.tool as Record<string, unknown>)?.designation as string],
                        ["Type", (detailData.tool as Record<string, unknown>)?.type_outil as string],
                        ["Diametre", `${(detailData.tool as Record<string, unknown>)?.diametre} mm`],
                        ["Matiere", (detailData.tool as Record<string, unknown>)?.matiere_outil as string],
                        ["Emplacement", (detailData.tool as Record<string, unknown>)?.emplacement as string],
                        ["Duree vie totale", `${(detailData.tool as Record<string, unknown>)?.duree_vie_totale} cycles`],
                        ["Usure actuelle", `${(detailData.tool as Record<string, unknown>)?.usure_actuelle} cycles`],
                        ["Vie restante", `${(detailData.tool as Record<string, unknown>)?.duree_vie_restante} cycles`],
                        ["Usure %", `${(detailData.tool as Record<string, unknown>)?.pct_usure}%`],
                        ["Cout achat", `${(detailData.tool as Record<string, unknown>)?.cout_achat}€`],
                        ["Cout remplacement", `${(detailData.tool as Record<string, unknown>)?.cout_remplacement}€`],
                        ["Stock", `${(detailData.tool as Record<string, unknown>)?.quantite_stock}`],
                        ["Seuil alerte", `${(detailData.tool as Record<string, unknown>)?.seuil_alerte}`],
                        ["Disponible", (detailData.tool as Record<string, unknown>)?.disponible ? "Oui" : "Non"],
                        ["Indicateur", ((detailData.tool as Record<string, unknown>)?.indicateur_remplacement as string || "")?.replace(/_/g, " ")],
                      ].map(([l, v]) => (
                        <div key={l} className="flex justify-between py-1 border-b border-[#F0F2F5] last:border-0">
                          <span className="text-[#5A6872] text-[11px]">{l}</span>
                          <span className="font-semibold text-[#1C1E21] text-[11px]">{String(v ?? "")}</span>
                        </div>
                      ))}
                    </div>
                    {/* Usure progress bar */}
                    <div className="mt-2">
                      <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-[#5A6872]">Usure</span>
                        <span className="font-mono font-semibold">{String((detailData.tool as Record<string, unknown>)?.pct_usure ?? "")}%</span>
                      </div>
                      <ProgressBar value={(detailData.tool as Record<string, unknown>)?.pct_usure as number || 0} />
                    </div>
                    {/* Vie restante predite */}
                    <div className={clsx("px-4 py-3 rounded-lg border-l-[4px] text-xs", (detailData.tool as Record<string, unknown>)?.indicateur_remplacement === "CRITICAL" ? "bg-[rgba(220,38,38,0.06)] border-l-[#DC2626]" : (detailData.tool as Record<string, unknown>)?.indicateur_remplacement === "WARNING" ? "bg-[rgba(245,158,11,0.06)] border-l-[#F59E0B]" : "bg-[rgba(37,99,235,0.06)] border-l-[#2563EB]")}>
                      <div className="flex items-center gap-2">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={clsx((detailData.tool as Record<string, unknown>)?.indicateur_remplacement === "CRITICAL" ? "text-[#DC2626]" : (detailData.tool as Record<string, unknown>)?.indicateur_remplacement === "WARNING" ? "text-[#F59E0B]" : "text-[#2563EB]")}><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>
                        <span className="font-bold text-[#1C1E21]">Vie restante predite</span>
                      </div>
                      <p className="text-[#5A6872] mt-1 ml-6">
                        {(detailData.tool as Record<string, unknown>)?.indicateur_remplacement === "CRITICAL"
                          ? "Remplacer immediatement — risque de casse en production."
                          : (detailData.tool as Record<string, unknown>)?.indicateur_remplacement === "WARNING"
                          ? "Planifier remplacement dans les prochains cycles."
                          : "OK — suivi normal."}
                        {" "}Vie restante: {String((detailData.tool as Record<string, unknown>)?.duree_vie_restante ?? "")} cycles ({String(((detailData.tool as Record<string, unknown>)?.nb_executions || (detailData.stats as Record<string, unknown>)?.nb_executions) ?? "")} utilisations cumulees).
                      </p>
                    </div>
                    {/* ML Wear Prediction */}
                    {wearPred.data && !wearPred.data.error && (
                      <div className={clsx("px-4 py-3 rounded-lg border-l-[4px] text-xs", wearPred.data.status === "CRITICAL" ? "bg-[rgba(220,38,38,0.06)] border-l-[#DC2626]" : wearPred.data.status === "WARNING" ? "bg-[rgba(245,158,11,0.06)] border-l-[#F59E0B]" : "bg-[rgba(37,99,235,0.06)] border-l-[#2563EB]")}>
                        <div className="flex items-center gap-2">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={wearPred.data.status === "CRITICAL" ? "text-[#DC2626]" : wearPred.data.status === "WARNING" ? "text-[#F59E0B]" : "text-[#2563EB]"}><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
                          <span className="font-bold text-[#1C1E21]">Usure predite (XGBoost)</span>
                        </div>
                        <p className="text-[#5A6872] mt-1 ml-6">
                          Increment estime: <strong>{(wearPred.data.predicted_wear_increment as number).toFixed(1)}</strong> cycles — Usure projetee: <strong>{(wearPred.data.wear_percentage_after_use as number).toFixed(0)}%</strong> apres prochaine utilisation.
                        </p>
                      </div>
                    )}
                  </CardBody>
                </Card>
                {/* Execution history summary */}
                {(detailData.executions as Record<string, unknown>[] || []).length > 0 && (
                  <Card>
                    <CardHeader title="Historique utilisations" subtitle={`${(detailData.executions as Record<string, unknown>[]).length} dernieres executions`} />
                    <CardBody className="p-0">
                      <div className="divide-y divide-[#F0F2F5] max-h-[300px] overflow-y-auto">
                        {(detailData.executions as Record<string, unknown>[]).slice(0, 15).map((ex, i) => (
                          <div key={i} className="px-4 py-2 text-[11px] flex items-center justify-between">
                            <span className="text-[#5A6872]">{(ex.date_debut as string)?.slice(0, 10)}</span>
                            <span className="font-mono text-[#1C1E21]">{ex.machine_code as string}</span>
                            <span className="text-[#5A6872]">{ex.piece_ref as string}</span>
                            <span className="font-mono text-[#1C1E21]">{ex.duree_utilisation as number} min</span>
                          </div>
                        ))}
                      </div>
                    </CardBody>
                  </Card>
                )}
              </>
            ) : (
              <Card><CardBody><div className="text-center py-8 text-[#C62828] text-sm">Failed to load tool detail</div></CardBody></Card>
            )}
          </div>
        )}
      </div>
    </PageContainer>
  );
}
