import { useState } from "react";
import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge, statusVariant } from "../components/ui/Badge";
import { BarChart } from "../components/charts/BarChart";
import { AreaChart } from "../components/charts/AreaChart";
import { DataTable } from "../components/ui/DataTable";
import { useApi } from "../hooks/useApi";
import { downloadReport } from "../api/download";
import type { QualityKPI, QualityCause, QualityByMachine } from "../types/api";

function ExportButtons() {
  return (
    <div className="flex items-center gap-2 ml-auto">
      <button onClick={() => downloadReport("/api/reports/quality/excel", "rapport_qualite.xlsx")}
         className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#16A34A]/10 text-[#16A34A] text-xs font-semibold hover:bg-[#16A34A]/20 transition-colors cursor-pointer">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Excel
      </button>
      <button onClick={() => downloadReport("/api/reports/quality/pdf", "rapport_qualite.pdf")}
         className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#DC2626]/10 text-[#DC2626] text-xs font-semibold hover:bg-[#DC2626]/20 transition-colors cursor-pointer">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        PDF
      </button>
    </div>
  );
}

export default function Quality() {
  const [dateStart, setDateStart] = useState("");
  const [dateEnd, setDateEnd] = useState("");
  const [machineFilter, setMachineFilter] = useState("");
  const [partFilter, setPartFilter] = useState("");
  const params = { date_start: dateStart || undefined, date_end: dateEnd || undefined };

  const kpi = useApi<QualityKPI>("/quality/kpi", { ...params, machine_code: machineFilter || undefined, piece_ref: partFilter || undefined });
  const causes = useApi<QualityCause[]>("/quality/causes", params);
  const byMachine = useApi<Record<string, unknown>[]>("/quality/by-machine", params);
  const byOperator = useApi<Record<string, unknown>[]>("/quality/by-operator", params);
  const byPart = useApi<Record<string, unknown>[]>("/quality/by-part", params);
  const byMaterial = useApi<Record<string, unknown>[]>("/quality/by-material", params);
  const evolution = useApi<Record<string, unknown>[]>("/quality/evolution", params);
  const scrapPred = useApi<Record<string, unknown>>(machineFilter ? `/quality/scrap-prediction?machine_code=${machineFilter}` : null);

  const machines = (byMachine.data || []) as unknown as Record<string, unknown>[];
  const machineOptions = machines.map((m) => ({ value: m.code as string, label: `${m.code as string} - ${m.nom as string}` }));

  // Compute scrap rate threshold from data (mean of all observed rates) instead of hardcoded 10%
  const scrapRatesPart = (byPart.data || []).map((r) => r.taux_rebut as number || 0);
  const scrapRatesMaterial = (byMaterial.data || []).map((r) => r.taux_rebut as number || 0);
  const allScrapRates = [...scrapRatesPart, ...scrapRatesMaterial];
  const scrapThreshold = allScrapRates.length > 0 ? allScrapRates.reduce((a, b) => a + b, 0) / allScrapRates.length : 0;

  return (
    <PageContainer title="Qualite" description="Analyse des rebuts par machine, operateur, piece et matiere">
      {/* Filters + Export */}
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <label className="label mb-0 text-xs">Du</label>
          <input type="date" value={dateStart} onChange={(e) => setDateStart(e.target.value)} className="input-field max-w-[160px] text-xs" />
          <label className="label mb-0 text-xs">au</label>
          <input type="date" value={dateEnd} onChange={(e) => setDateEnd(e.target.value)} className="input-field max-w-[160px] text-xs" />
        </div>
        <select value={machineFilter} onChange={(e) => setMachineFilter(e.target.value)} className="input-field max-w-[220px] text-xs">
          <option value="">Toutes machines</option>
          {machineOptions.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
        <input
          type="text" placeholder="Filter piece ref..." value={partFilter}
          onChange={(e) => setPartFilter(e.target.value)}
          className="input-field max-w-[180px] text-xs"
        />
        <ExportButtons />
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-6 gap-3">
        <KpiCard label="Inspections" value={kpi.data?.nb_inspections ?? 0} />
        <KpiCard label="Taux conformite" value={kpi.data ? Math.round(kpi.data.taux_conformite * 100) / 100 : 0} unit="%" color="#2563EB" />
        <KpiCard label="Non conformes" value={kpi.data?.total_non_conformes ?? 0} color="#DC2626" />
        <KpiCard label="Ecart dimension" value={kpi.data ? Math.round(kpi.data.ecart_dimension_moyen * 100) / 100 : 0} unit="mm" />
        <KpiCard label="Rugosite moyenne" value={kpi.data ? Math.round(kpi.data.rugosite_moyenne * 100) / 100 : 0} />
        <KpiCard label="Controles" value={kpi.data?.total_controles ?? 0} />
      </div>

      {/* Row 1: By Machine & By Operator */}
      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardHeader title="Taux rebut par machine" />
          <CardBody className="p-0">
            {byMachine.data ? (
              <BarChart data={byMachine.data as unknown as Record<string, unknown>[]} xKey="code" yKey="taux_rebut" colorKey="taux_rebut" height={280} />
            ) : byMachine.loading ? <div className="h-[280px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Taux rebut par operateur" />
          <CardBody className="p-0">
            {byOperator.data ? (
              <BarChart
                data={byOperator.data.map((r) => ({ ...r, operateur_label: `${r.prenom as string} ${r.nom as string}` }))}
                xKey="operateur_label" yKey="taux_rebut" colorKey="taux_rebut" height={280}
              />
            ) : byOperator.loading ? <div className="h-[280px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
          </CardBody>
        </Card>
      </div>

      {/* Row 2: By Part & By Material */}
      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardHeader title="Taux rebut par piece" />
          <CardBody className="p-0">
            {byPart.data ? (
              <DataTable
                columns={[
                  { key: "reference", header: "Reference", width: "120px", render: (r) => <span className="font-mono font-bold text-[11px]">{r.reference as string}</span> },
                  { key: "designation", header: "Piece" },
                  { key: "controles", header: "Controles", align: "right" },
                  { key: "non_conformes", header: "Non conformes", align: "right" },
                  { key: "taux_rebut", header: "Taux rebut", align: "right", render: (r) => { const tr = ((r.taux_rebut as number) || 0); return <span className={tr > scrapThreshold ? "text-[#DC2626]" : "text-[#2563EB]"}>{tr.toFixed(1)}%</span> } },
                ]}
                data={byPart.data as unknown as Record<string, unknown>[]}
                pageSize={10}
              />
            ) : byPart.loading ? <div className="h-[200px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Taux rebut par matiere" />
          <CardBody className="p-0">
            {byMaterial.data ? (
              <DataTable
                columns={[
                  { key: "type_matiere", header: "Type matiere", render: (r) => <span className="font-semibold text-xs">{r.type_matiere as string}</span> },
                  { key: "total_controles", header: "Controles", align: "right" },
                  { key: "total_non_conformes", header: "Non conformes", align: "right" },
                  { key: "taux_rebut", header: "Taux rebut", align: "right", render: (r) => { const tr = ((r.taux_rebut as number) || 0); return <span className={tr > scrapThreshold ? "text-[#DC2626]" : "text-[#2563EB]"}>{tr.toFixed(1)}%</span> } },
                ]}
                data={byMaterial.data as unknown as Record<string, unknown>[]}
                pageSize={10}
              />
            ) : byMaterial.loading ? <div className="h-[200px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
          </CardBody>
        </Card>
      </div>

      {/* Row 3: Causes, Prediction & Evolution */}
      <div className="grid grid-cols-5 gap-4">
        <div className="col-span-2">
          <Card>
            <CardHeader title="Causes de rebut" />
            <CardBody className="p-0">
              {causes.data ? (
                <BarChart data={causes.data as unknown as Record<string, unknown>[]} xKey="description" yKey="nb" colorKey={undefined} height={280} horizontal />
              ) : causes.loading ? <div className="h-[280px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
            </CardBody>
          </Card>
        </div>
        <div className="col-span-3 space-y-3">
          {/* Scrap Prediction */}
          {machineFilter && scrapPred.data && !scrapPred.data.error ? (
            <div className={`px-4 py-3 rounded-lg border text-xs ${scrapPred.data.risk_level === 'HIGH' ? 'border-[rgba(220,38,38,0.3)] bg-[rgba(220,38,38,0.04)] border-l-[#DC2626] border-l-[4px]' : scrapPred.data.risk_level === 'MODERATE' ? 'border-[rgba(56,189,248,0.3)] bg-[rgba(56,189,248,0.04)] border-l-[#38BDF8] border-l-[4px]' : 'border-[rgba(37,99,235,0.2)] bg-[rgba(37,99,235,0.04)] border-l-[#2563EB] border-l-[4px]'}`}>
              <div className="flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>
                <span className="font-bold text-[#1C1E21]">Prediction rebut — {machineFilter}</span>
                <span className={`font-bold ml-auto ${scrapPred.data.risk_level === 'HIGH' ? 'text-[#DC2626]' : scrapPred.data.risk_level === 'MODERATE' ? 'text-[#38BDF8]' : 'text-[#2563EB]'}`}>
                  {(scrapPred.data.avg_scrap_probability as number * 100).toFixed(1)}% risque
                </span>
              </div>
              <div className="mt-1 text-[#8A95A0] ml-6">Niveau: <strong>{scrapPred.data.risk_level as string}</strong> — base sur {scrapPred.data.samples_analyzed as number} phases d'execution.</div>
            </div>
          ) : scrapPred.loading ? (
            <div className="px-4 py-3 rounded-lg border border-[rgba(37,99,235,0.2)] bg-[rgba(37,99,235,0.04)] text-xs text-[#8A95A0]">Chargement prediction rebut...</div>
          ) : (
            <div className="px-4 py-3 rounded-lg border border-[rgba(37,99,235,0.2)] bg-[rgba(37,99,235,0.04)] border-l-[4px] border-l-[#2563EB] text-xs">
              <div className="flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/></svg>
                <span className="font-bold text-[#1C1E21]">Prediction rebut</span>
                <span className="text-[#8A95A0]">— Selectionnez une machine pour voir la prediction</span>
              </div>
            </div>
          )}
          <Card>
            <CardHeader title="Evolution taux rebut" />
            <CardBody className="p-0">
              {evolution.data ? (
                <AreaChart
                  data={evolution.data as unknown as Record<string, unknown>[]}
                  xKey="date"
                  series={[{ key: "taux_rebut", name: "Taux rebut", color: "#2563EB" }]}
                  height={220}
                />
              ) : evolution.loading ? <div className="h-[220px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
            </CardBody>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
}
