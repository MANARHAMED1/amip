import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge, statusVariant } from "../components/ui/Badge";
import { ProgressBar } from "../components/ui/ProgressBar";
import { DataTable } from "../components/ui/DataTable";
import { useApi } from "../hooks/useApi";
import { getJSON } from "../api/client";
import { downloadReport } from "../api/download";
import type { ProductionKPI, ProductionOrder, ProductionOrderDetail } from "../types/api";
import clsx from "clsx";

export default function Production() {
  const [urlParams, setUrlParams] = useSearchParams();
  const [statutFilter, setStatutFilter] = useState("");

  const kpi = useApi<ProductionKPI>("/production/kpi");
  const list = useApi<ProductionOrder[]>(`/production/list?limit=200${statutFilter ? `&statut=${statutFilter}` : ""}`);
  const machines = useApi<Record<string, unknown>[]>("/machine/list");

  const [selectedOF, setSelectedOF] = useState<string | null>(urlParams.get("of") || null);
  const durPred = useApi<Record<string, unknown>>(selectedOF ? `/production/prediction/duration?numero_of=${selectedOF}` : null);
  const [ofDetail, setOfDetail] = useState<ProductionOrderDetail | null>(null);
  const [ofLoading, setOfLoading] = useState(false);

  const openOF = async (num: string) => {
    setSelectedOF(num);
    setUrlParams({ of: num });
    setOfLoading(true);
    try {
      const data = await getJSON<ProductionOrderDetail>(`/production/${num}`);
      setOfDetail(data);
    } catch {
      setOfDetail(null);
    } finally {
      setOfLoading(false);
    }
  };

  const closeOF = () => { setSelectedOF(null); setOfDetail(null); setUrlParams({}); };

  useEffect(() => {
    const ofParam = urlParams.get("of");
    if (ofParam && ofParam !== selectedOF) openOF(ofParam);
  }, []);

  return (
    <PageContainer title="Production" description="Gestion des ordres de fabrication">
      {/* KPI Cards */}
      <div className="grid grid-cols-6 gap-3">
        <KpiCard label="Total OF" value={kpi.data?.total ?? 0} />
        <KpiCard label="En cours" value={kpi.data?.en_cours ?? 0} color="#38BDF8" />
        <KpiCard label="Termines" value={kpi.data?.termine ?? 0} color="var(--color-copper)" />
        <KpiCard label="En attente" value={kpi.data?.en_attente ?? 0} color="#94A3B8" />
        <KpiCard label="En retard" value={kpi.data?.en_retard ?? 0} color="#DC2626" />
        <KpiCard label="Annules" value={kpi.data?.annule ?? 0} color="#64748B" />
      </div>

      {/* Export */}
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <label className="label mb-0">Statut</label>
          <select value={statutFilter} onChange={(e) => setStatutFilter(e.target.value)} className="input-field max-w-[180px] text-xs">
            <option value="">Tous</option>
            <option value="EN_COURS">En cours</option>
            <option value="EN_ATTENTE">En attente</option>
            <option value="TERMINE">Termine</option>
            <option value="ANNULE">Annule</option>
          </select>
          <span className="text-[#8A95A0] text-xs">Click OF number to view detail (phases, rejects per phase, operators)</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => downloadReport("/api/reports/production/excel", "rapport_production.xlsx")}
             className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#16A34A]/10 text-[#16A34A] text-xs font-semibold hover:bg-[#16A34A]/20 transition-colors cursor-pointer">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Excel
          </button>
          <button onClick={() => downloadReport("/api/reports/production/pdf", "rapport_production.pdf")}
             className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#DC2626]/10 text-[#DC2626] text-xs font-semibold hover:bg-[#DC2626]/20 transition-colors cursor-pointer">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            PDF
          </button>
        </div>
      </div>

      <div className={clsx("grid gap-4", selectedOF ? "grid-cols-5" : "grid-cols-1")}>
        {/* OF List */}
        <div className={selectedOF ? "col-span-2" : ""}>
          <Card>
            <CardHeader title="Ordres de Fabrication" subtitle={selectedOF ? "Select another OF or click close" : undefined} />
            <CardBody className="p-0">
              {list.data ? (
                <DataTable
                  columns={[
                    { key: "numero_of", header: "OF", width: "110px", render: (r) => (
                      <button onClick={() => openOF(r.numero_of as string)} className="font-mono font-bold text-xs text-[var(--color-copper)] hover:text-[var(--color-copper-light)] transition-colors underline underline-offset-2 decoration-dotted">
                        {r.numero_of as string}
                      </button>
                    )},
                    { key: "piece_ref", header: "Ref" },
                    { key: "piece_nom", header: "Piece" },
                    { key: "quantite_demandee", header: "Plan", align: "right" },
                    { key: "quantite_produite", header: "Fabriqué", align: "right" },
                    { key: "quantite_rebut", header: "Rebut", align: "right", render: (r) => <span className="text-[#DC2626]">{(r.quantite_rebut as number || 0)}</span> },
                    { key: "bonnes", header: "Bon", align: "right", render: (r) => { const f = r.quantite_produite as number || 0; const b = r.quantite_rebut as number || 0; return <span className="text-[#2563EB] font-semibold">{f - b}</span> } },
                    { key: "taux_rendement", header: "Rend.", align: "right", render: (r) => `${(r.taux_rendement as number || 0).toFixed(1)}%` },
                    { key: "statut", header: "Statut", render: (r) => <Badge variant={statusVariant(r.statut as string)}>{(r.statut as string).replace("_", " ")}</Badge> },
                    { key: "priorite", header: "Prio", render: (r) => <Badge variant={r.priorite === "HAUTE" ? "warning" : "neutral"}>{(r.priorite as string)}</Badge> },
                  ]}
                  data={(list.data || []) as unknown as Record<string, unknown>[]}
                  pageSize={selectedOF ? 10 : 25}
                />
              ) : list.loading ? <div className="text-center py-12 text-[#8A95A0] text-sm">Loading...</div> : null}
            </CardBody>
          </Card>
        </div>

        {/* OF Detail */}
        {selectedOF && (
          <div className="col-span-3">
            <Card>
              <CardHeader
                title={`OF ${selectedOF}`}
                subtitle={ofDetail ? `${ofDetail.of.piece_nom} - ${ofDetail.of.piece_ref}` : undefined}
                action={
                  <button onClick={closeOF} className="text-xs text-[#8A95A0] hover:text-[#C62828] transition-colors px-2 py-1 rounded hover:bg-[#FDF6F6]">
                    Close
                  </button>
                }
              />
              <CardBody>
                {ofLoading ? (
                  <div className="text-center py-12 text-[#8A95A0] text-sm">Loading OF detail...</div>
                ) : ofDetail ? (
                  <>
                    {/* OF Info Grid */}
                    <div className="grid grid-cols-4 gap-3 mb-4">
                      <KpiCard label="Planifie" value={ofDetail.of.quantite_demandee} unit="pcs" color="var(--color-copper)" />
                      <KpiCard label="Fabriqué (total)" value={ofDetail.of.quantite_produite} unit="pcs" color="var(--color-copper)" />
                      <KpiCard label="Bon" value={ofDetail.of.quantite_produite - ofDetail.of.quantite_rebut} unit="pcs" color="#2563EB" />
                      <KpiCard label="Rebut" value={ofDetail.of.quantite_rebut} unit={`pcs (${ofDetail.of.quantite_demandee > 0 ? ((ofDetail.of.quantite_rebut / ofDetail.of.quantite_produite) * 100).toFixed(1) : 0}%)`} color="#DC2626" />
                    </div>
                    <div className="grid grid-cols-3 gap-3 mb-4">
                      <KpiCard label="Rendement" value={ofDetail.of.quantite_demandee > 0 ? Math.round((1 - ofDetail.of.quantite_rebut / ofDetail.of.quantite_produite) * 1000) / 10 : 0} unit="%" color="#2563EB" />
                      <KpiCard
                        label="Retard"
                        value={ofDetail.retard_jours ?? 0}
                        unit="jours"
                        color={ofDetail.retard_jours ? "#DC2626" : "#2563EB"}
                      />
                      <KpiCard label="Taux rendement" value={ofDetail.of.taux_rendement || 0} unit="%" color="var(--color-copper)" />
                    </div>

                    {/* Phases table with rejects per phase */}
                    {/* Delay prediction placeholder */}
                    {ofDetail.retard_jours ? (
                      <div className="px-4 py-2.5 rounded-lg border border-[rgba(198,40,40,0.15)] bg-[#FDF6F6] border-l-[4px] border-l-[#C62828] flex items-center gap-2 text-xs mb-3">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#C62828" strokeWidth="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                        <span className="font-bold text-[#C62828]">Prediction retard: {ofDetail.retard_jours} jours de retard detecte</span>
                        <span className="text-[#8A95A0]">— Replanifier les phases critiques pour recuperer le retard.</span>
                      </div>
                    ) : durPred.data && !durPred.data.error ? (
                      <div className="px-4 py-2.5 rounded-lg border border-[rgba(37,99,235,0.15)] bg-[rgba(37,99,235,0.04)] border-l-[4px] border-l-[#2563EB] flex items-center gap-2 text-xs mb-3">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>
                        <span className="font-bold text-[#1C1E21]">Duree estimee</span>
                        <span className="text-[#8A95A0]">— {durPred.data.estimated_duration_min as number} min ({(durPred.data.estimated_duration_hours as number).toFixed(1)}h) selon historique des OF similaires</span>
                      </div>
                    ) : (
                      <div className="px-4 py-2.5 rounded-lg border border-[rgba(37,99,235,0.15)] bg-[rgba(37,99,235,0.04)] border-l-[4px] border-l-[#2563EB] flex items-center gap-2 text-xs mb-3">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>
                        <span className="font-bold text-[#1C1E21]">Prediction duree</span>
                        <span className="text-[#8A95A0]">— Chargement...</span>
                      </div>
                    )}
                    <div className="text-[13px] font-semibold text-[#1C1E21] mb-2">Phases de fabrication</div>
                    <DataTable
                      columns={[
                        { key: "numero_phase", header: "Phase", width: "70px", render: (r) => <span className="font-mono font-bold text-[11px]">{r.numero_phase as string}</span> },
                        { key: "designation", header: "Designation" },
                        { key: "machine_code", header: "Machine", render: (r) => <span className="font-mono text-[11px]">{r.machine_code as string}</span> },
                        { key: "nb_pieces_produites", header: "Produites", align: "right" },
                        { key: "nb_pieces_rebut", header: "Rebut", align: "right", render: (r) => <span className="text-[#C62828] font-semibold">{(r.nb_pieces_rebut as number || 0)}</span> },
                        { key: "operateur_nom", header: "Operateur", render: (r) => `${(r.operateur_prenom as string || "")} ${(r.operateur_nom as string || "").charAt(0)}.` },
                        { key: "statut", header: "Statut", render: (r) => <Badge variant={statusVariant((r.exec_statut as string) || (r.statut as string))}>{(r.exec_statut as string || r.statut as string || "").replace("_", " ")}</Badge> },
                      ]}
                      data={ofDetail.phases as unknown as Record<string, unknown>[]}
                      pageSize={10}
                      searchable={false}
                    />
                  </>
                ) : (
                  <div className="text-center py-8 text-[#C62828] text-sm">Failed to load OF detail</div>
                )}
              </CardBody>
            </Card>
          </div>
        )}
      </div>
    </PageContainer>
  );
}
