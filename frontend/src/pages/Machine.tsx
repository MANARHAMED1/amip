import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge, statusVariant } from "../components/ui/Badge";
import { ProgressBar } from "../components/ui/ProgressBar";
import { GaugeChart } from "../components/charts/GaugeChart";
import { AreaChart } from "../components/charts/AreaChart";
import { useApi } from "../hooks/useApi";
import { getJSON } from "../api/client";
import type { Machine } from "../types/api";
import clsx from "clsx";

export default function Machine() {
  const [urlParams, setUrlParams] = useSearchParams();
  const machines = useApi<Machine[]>("/machine/list");
  const [selected, setSelected] = useState(urlParams.get("machine") || "");
  const allSensors = useApi<Record<string, unknown>[]>("/sensors/all-machines");

  useEffect(() => {
    const m = urlParams.get("machine");
    if (m && m !== selected) setSelected(m);
  }, [urlParams]);

  const handleSelect = (code: string) => {
    setSelected(code);
    setUrlParams({ machine: code });
  };

  const info = useApi<Record<string, unknown>>(selected ? `/machine/${selected}` : null);
  const perf = useApi<Record<string, unknown>>(selected ? `/machine/${selected}/performance` : null);
  const oeeHist = useApi<Record<string, unknown>[]>(selected ? `/machine/${selected}/oee-history` : null);
  const sensors = useApi<Record<string, unknown>>(selected ? `/machine/${selected}/sensors` : null);
  const sensorHistory = useApi<Record<string, unknown>[]>(selected ? `/sensors/history/${selected}` : null);
  const timeline = useApi<Record<string, unknown>[]>(selected ? `/machine/${selected}/phases-timeline` : null);
  const maint = useApi<Record<string, unknown>[]>(selected ? `/machine/${selected}/maintenance` : null);
  const maintKpi = useApi<Record<string, unknown>>(selected ? `/machine/${selected}/maintenance-kpi` : null);
  const anomaly = useApi<Record<string, unknown>>(selected ? `/machine/${selected}/anomaly` : null);
  const nextMaint = useApi<Record<string, unknown>>(selected ? `/maintenance/${selected}/next-maintenance` : null);

  const rawInfo = info.data as Record<string, unknown> | undefined;
  const machineInfo = rawInfo?.machine as Machine | undefined;
  const operateur = rawInfo?.operateur as Record<string, unknown> | undefined;
  const outil = rawInfo?.outil_actuel as Record<string, unknown> | undefined;
  const ofActuel = rawInfo?.of_actuel as Record<string, unknown> | undefined;
  const statut = (machineInfo?.statut as string) || "UNKNOWN";
  const statColor = statut === "RUNNING" ? "#2563EB" : statut === "BROKEN" ? "#DC2626" : "#94A3B8";

  const sensorCurrent = sensors.data?.current as Record<string, unknown> | undefined;
  const sensorStats = sensors.data?.stats as Record<string, unknown> | undefined;

  // Health score: composite from sensors (scaled to observed max), OEE, and tool wear
  const healthScore = (() => {
    if (!sensorStats || !perf.data || !outil) return null;
    const tempMaxObserved = sensorStats.temp_max as number || 1;
    const vibMaxObserved = sensorStats.vib_max as number || 1;
    const tempOk = Math.max(0, 100 - ((sensorStats.temp_max as number || 0) / tempMaxObserved) * 100);
    const vibOk = Math.max(0, 100 - ((sensorStats.vib_max as number || 0) / vibMaxObserved) * 100);
    const oeeScore = (perf.data.oee as number || 0);
    const toolWear = 100 - (outil.pct_usure as number || 0);
    return Math.round((tempOk * 0.25 + vibOk * 0.25 + oeeScore * 0.3 + toolWear * 0.2));
  })();

  // Machines needing attention: broken machines from actual data
  const needsAttention = (allSensors.data || []).filter((m) => m.statut_machine === "BROKEN");

  return (
    <PageContainer title="Machines" description="Analyse et suivi des machines avec donnees capteurs">
      {/* Machines needing attention banner */}
      {needsAttention.length > 0 && (
        <div className="bg-[#FDF6F6] border border-[rgba(198,40,40,0.2)] border-l-[4px] border-l-[#C62828] rounded-lg px-5 py-3">
          <div className="text-xs font-bold text-[#C62828] uppercase tracking-wider">
            {needsAttention.length} machine{needsAttention.length > 1 ? "s" : ""} necessite(nt) attention
          </div>
          <div className="flex flex-wrap gap-2 mt-2">
            {needsAttention.map((m, i) => (
              <button key={i} onClick={() => handleSelect(m.code as string)}
                className="flex items-center gap-2 px-3 py-1.5 bg-white rounded-lg border border-[rgba(198,40,40,0.15)] text-xs hover:bg-[#FBEFEF] transition-colors cursor-pointer"
              >
                <span className="font-mono font-bold">{m.code as string}</span>
                <Badge variant="danger">
                  PANNE
                </Badge>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Machine Selector */}
      <div className="flex items-center gap-3 mb-2">
        <label className="label mb-0">Machine</label>
        <select value={selected} onChange={(e) => handleSelect(e.target.value)} className="input-field max-w-xs text-xs">
          <option value="">Select a machine</option>
          {(machines.data || []).map((m) => (
            <option key={m.code} value={m.code}>{m.code} - {m.nom}</option>
          ))}
        </select>
        {machines.loading && <span className="text-xs text-[#8A95A0]">Loading...</span>}
      </div>

      {selected && machineInfo && (
        <>
          {/* Machine Header with Health Score */}
          <div className="flex items-center gap-4 px-5 py-4 bg-white border border-[#E2E5E9] rounded-xl shadow-sm border-l-4"
            style={{ borderLeftColor: statColor }}
          >
            <div className="flex items-center justify-center w-11 h-11 rounded-xl" style={{ backgroundColor: `${statColor}10`, color: statColor }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72 1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
            </div>
            <div>
              <div className="font-mono font-extrabold text-lg text-[#1E293B]">{machineInfo.code}</div>
              <div className="text-[#64748B] text-xs mt-0.5">{machineInfo.nom as string}</div>
            </div>
            <Badge variant={statusVariant(statut)}>{statut}</Badge>
            {healthScore !== null && (
              <div className="flex items-center gap-2 ml-2 px-3 py-1.5 rounded-lg text-xs font-bold"
                style={{
                  backgroundColor: `hsla(${healthScore * 1.2}, 70%, 45%, 0.1)`,
                  color: `hsl(${healthScore * 1.2}, 70%, 45%)`,
                }}
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                </svg>
                Health: {healthScore}%
              </div>
            )}
            <div className="ml-auto flex gap-4 text-[#94A3B8] text-[11px]">
              <span>{machineInfo.type}</span>
              <span>{machineInfo.marque} {machineInfo.modele}</span>
            </div>
          </div>

          {/* Operator + prediction placeholder */}
          <div className="flex items-center gap-2 flex-wrap">
            {operateur && (
              <div className="flex items-center gap-2 px-4 py-2 bg-[#F1F5F9] rounded-lg text-xs text-[#64748B]">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Operateur: <strong>{operateur.prenom as string} {operateur.nom as string}</strong>
              </div>
            )}
            {statut !== "RUNNING" && (
              <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#FDF6F6] text-[#C62828] text-xs font-semibold">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                Action requise: machine {statut === "BROKEN" ? "en panne" : statut === "MAINTENANCE" ? "en maintenance" : "arretee"}
              </div>
            )}
          </div>

          {/* Performance KPIs */}
          <SectionHeader title="Performance" subtitle="Indicateurs de performance machine" />
          <div className="grid grid-cols-5 gap-3">
            <KpiCard label="Disponibilite" value={perf.data ? +(perf.data.disponibilite as number || 0).toFixed(1) : 0} unit="%" />
            <KpiCard label="Performance" value={perf.data ? +(perf.data.performance as number || 0).toFixed(1) : 0} unit="%" />
            <KpiCard label="Qualite" value={perf.data ? +(perf.data.qualite as number || 0).toFixed(1) : 0} unit="%" />
            <KpiCard label="OEE" value={perf.data ? +(perf.data.oee as number || 0).toFixed(1) : 0} unit="%" />
            <KpiCard label="Pieces produites" value={perf.data?.total_produites as number || 0} />
          </div>

          {/* OEE History + Sensor Gauges */}
          <SectionHeader title="Capteurs & OEE" subtitle="Donnees temps reel et historique performance" />
          <div className="grid grid-cols-5 gap-4">
            {/* Sensor Gauges */}
            <div className="col-span-2">
                  {sensorCurrent && sensorStats ? (
                <div className="grid grid-cols-2 gap-3">
                  <Card><CardBody className="flex flex-col items-center py-3">
                    <GaugeChart value={sensorCurrent.temperature as number || 0} max={sensorStats.temp_max as number || 100} label="Temperature (°C)" size={140} />
                    <div className="text-[10px] text-[#8A95A0] mt-1">Max observe: {(sensorStats.temp_max as number).toFixed(0)}°C</div>
                  </CardBody></Card>
                  <Card><CardBody className="flex flex-col items-center py-3">
                    <GaugeChart value={sensorCurrent.vibration as number || 0} max={sensorStats.vib_max as number || 5} label="Vibration (mm/s)" size={140} />
                    <div className="text-[10px] text-[#8A95A0] mt-1">Max observe: {(sensorStats.vib_max as number).toFixed(1)} mm/s</div>
                  </CardBody></Card>
                  <Card><CardBody className="flex flex-col items-center py-3">
                    <GaugeChart value={sensorCurrent.rpm as number || 0} max={machineInfo?.rpm_max ?? (sensorStats.rpm_max as number || 6000)} label="RPM" size={140} />
                  </CardBody></Card>
                  <Card><CardBody className="flex flex-col items-center py-3">
                    <GaugeChart value={sensorCurrent.puissance as number || 0} max={sensorStats.puissance_max as number || 50} label="Puissance (kW)" size={140} />
                  </CardBody></Card>
                </div>
              ) : sensors.loading ? <div className="h-[320px] flex items-center justify-center text-[#8A95A0] text-sm">Loading capteurs...</div> : null}
              {/* Sensor current values compact */}
              {sensorCurrent && (
                <div className="grid grid-cols-4 gap-2 mt-2">
                  <div className="px-2 py-1.5 rounded bg-[#F8FAFB] text-center">
                    <div className="text-[9px] text-[#8A95A0] uppercase tracking-wider">Avance</div>
                    <div className="font-mono text-xs">{(sensorCurrent.vitesse_avance as number || 0).toFixed(1)} mm/min</div>
                  </div>
                  <div className="px-2 py-1.5 rounded bg-[#F8FAFB] text-center">
                    <div className="text-[9px] text-[#8A95A0] uppercase tracking-wider">Cycle</div>
                    <div className="font-mono text-xs">{(sensorCurrent.temps_cycle as number || 0).toFixed(1)}s</div>
                  </div>
                  <div className="px-2 py-1.5 rounded bg-[#F8FAFB] text-center">
                    <div className="text-[9px] text-[#8A95A0] uppercase tracking-wider">Charge</div>
                    <div className="font-mono text-xs">{(sensorCurrent.charge_frappe as number || 0).toFixed(1)}%</div>
                  </div>
                  <div className="px-2 py-1.5 rounded bg-[#F8FAFB] text-center">
                    <div className="text-[9px] text-[#8A95A0] uppercase tracking-wider">Etat</div>
                    <Badge variant={statusVariant(sensorCurrent.statut_machine as string || statut)}>{(sensorCurrent.statut_machine as string || statut)}</Badge>
                  </div>
                </div>
              )}
            </div>

            {/* OEE History */}
            <div className="col-span-3">
              <Card>
                <CardHeader title="OEE History (90 jours)" />
                <CardBody className="p-0">
                  {oeeHist.data ? (
                    <AreaChart
                      data={oeeHist.data.slice(-90) as Record<string, unknown>[]}
                      xKey="date"
                      series={[
                        { key: "oee", name: "OEE", color: "#2563EB" },
                        { key: "disponibilite", name: "Disponibilite", color: "#38BDF8" },
                        { key: "performance", name: "Performance", color: "#2563EB" },
                        { key: "qualite", name: "Qualite", color: "#38BDF8" },
                      ]}
                      height={300}
                    />
                  ) : oeeHist.loading ? <div className="h-[300px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div> : null}
                </CardBody>
              </Card>
            </div>
          </div>

          {/* Sensor History Curves */}
          {sensorHistory.data && sensorHistory.data.length > 0 && (
            <>
              <SectionHeader title="Historique Capteurs" subtitle="Courbes temperature, vibration et RPM (200 dernieres lectures)" />
              <div className="grid grid-cols-2 gap-4">
                <Card>
                  <CardHeader title="Temperature" subtitle={`Max: ${(sensorStats?.temp_max as number || 0).toFixed(0)}°C`} />
                  <CardBody className="p-0">
                    <AreaChart
                      data={sensorHistory.data.slice(-200).reverse() as Record<string, unknown>[]}
                      xKey="timestamp"
                      series={[{ key: "temperature", name: "Temperature", color: "#2563EB" }]}
                      height={200}
                    />
                  </CardBody>
                </Card>
                <Card>
                  <CardHeader title="Vibration" subtitle={`Max: ${(sensorStats?.vib_max as number || 0).toFixed(1)} mm/s`} />
                  <CardBody className="p-0">
                    <AreaChart
                      data={sensorHistory.data.slice(-200).reverse() as Record<string, unknown>[]}
                      xKey="timestamp"
                      series={[{ key: "vibration", name: "Vibration", color: "#2563EB" }]}
                      height={200}
                    />
                  </CardBody>
                </Card>
              </div>
            </>
          )}

          {/* Failure Risk Prediction — score computed from live sensor/OEE/wear data */}
          {healthScore !== null && (
            <div
              className="px-4 py-3 rounded-lg border-l-[4px] text-xs"
              style={{
                backgroundColor: `rgba(${255 * (1 - healthScore / 100)}, ${Math.min(255, 255 * (healthScore / 100) * 2)}, 50, 0.06)`,
                borderLeftColor: `hsl(${healthScore * 1.2}, 70%, 45%)`,
              }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-bold text-[#1C1E21]">Sante machine (composite capteurs + OEE + outil)</span>
                  <span className="text-[#5A6872] ml-2">
                    — Score composite: temperature, vibration, OEE et usure outil.
                  </span>
                </div>
                <span
                  className="font-bold font-mono"
                  style={{ color: `hsl(${healthScore * 1.2}, 70%, 45%)` }}
                >
                  {healthScore}%
                </span>
              </div>
            </div>
          )}

          {/* ML Predictions */}
          <SectionHeader title="Analyse predictive" subtitle="Anomalies et maintenance preventive" />
          <div className="grid grid-cols-2 gap-4">
            {anomaly.data && !anomaly.data.error && (
              <Card>
                <CardHeader title="Detection d'anomalie" subtitle="IsolationForest sur capteurs temps reel" />
                <CardBody>
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold ${anomaly.data.is_anomaly ? 'bg-[#DC2626]' : 'bg-[#2563EB]'}`}>
                      {anomaly.data.is_anomaly ? '!' : '✓'}
                    </div>
                    <div>
                      <div className={`font-bold text-sm ${anomaly.data.is_anomaly ? 'text-[#DC2626]' : 'text-[#1E293B]'}`}>
                        {anomaly.data.status as string}
                      </div>
                      <div className="text-[11px] text-[#64748B]">Score: {(anomaly.data.anomaly_score as number).toFixed(3)}</div>
                    </div>
                  </div>
                  <div className="mt-2 text-[10px] text-[#8A95A0]">{anomaly.data.samples_analyzed as number} lectures analysees</div>
                </CardBody>
              </Card>
            )}
            {nextMaint.data && !nextMaint.data.error && (
              <Card>
                <CardHeader title="Prochaine maintenance" subtitle="Prediction XGBoost basee sur historique" />
                <CardBody>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#38BDF8]/10 flex items-center justify-center text-[#38BDF8]">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    </div>
                    <div>
                      <div className="font-bold text-sm text-[#1E293B]">{(nextMaint.data.estimated_days_until_maintenance as number).toFixed(0)} jours</div>
                      <div className="text-[11px] text-[#64748B]">Estimee au {nextMaint.data.estimated_date as string}</div>
                    </div>
                  </div>
                  <div className="mt-2 text-[10px] text-[#8A95A0]">Confiance: {nextMaint.data.confidence as string}</div>
                </CardBody>
              </Card>
            )}
            {anomaly.loading && nextMaint.loading && <div className="text-[#8A95A0] text-xs p-4">Chargement predictions...</div>}
          </div>

          {/* Planning & Tooling */}
          <SectionHeader title="Planning & Outillage" subtitle="Phases planning, outil et maintenance" />
          {/* Compact Phases Timeline */}
          {timeline.data && timeline.data.length > 0 && (
            <div className="px-3 py-2.5 rounded-lg border border-[#E2E5E9] bg-white mb-3 overflow-x-auto">
              <div className="flex items-center gap-1 min-w-max">
                {timeline.data.map((phase, i) => {
                  const statut = (phase.statut as string) || "";
                  const color = statut === "TERMINE" ? "#2563EB" : statut === "EN_COURS" ? "#38BDF8" : "#CBD5E1";
                  return (
                    <div key={i} className="flex items-center">
                      {i > 0 && <div className="w-6 h-px bg-[#E2E5E9]" />}
                      <div className="flex flex-col items-center gap-1 px-2 py-1 rounded-md text-[10px] min-w-[80px]"
                        style={{ backgroundColor: `${color}10` }}
                      >
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
                        <span className="font-semibold text-[#1C1E21] truncate max-w-[70px] text-center">
                          {phase.phase_name as string}
                        </span>
                        <span className="text-[#8A95A0] text-[9px]">
                          {statut === "TERMINE" ? "Termine" : statut === "EN_COURS" ? "En cours" : "Planifie"}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          <div className="grid grid-cols-5 gap-3">
            <div className="col-span-2 space-y-3">
              {outil && (
                <div className="px-3 py-2.5 rounded-lg border border-[#E2E5E9] bg-white text-xs">
                  <div className="flex items-center gap-2 mb-1.5">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="1.8"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
                    <span className="font-semibold text-[#1C1E21]">{outil.code as string}</span>
                    <span className="text-[#8A95A0] text-[10px]">{outil.type_outil as string}</span>
                    <Badge variant={(outil.indicateur_remplacement as string) === "CRITICAL" ? "danger" : (outil.indicateur_remplacement as string) === "WARNING" ? "warning" : "success"}>
                      {(outil.indicateur_remplacement as string || "OK").replace(/_/g, " ")}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-3 text-[10px] text-[#64748B]">
                    <span>Usure: {(outil.pct_usure as number).toFixed(0)}%</span>
                    <ProgressBar value={outil.pct_usure as number} height={6} />
                  </div>
                </div>
              )}
              {ofActuel && (
                <div className="px-3 py-2.5 rounded-lg border border-[#E2E5E9] bg-white text-xs">
                  <div className="flex items-center gap-2 mb-1">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" strokeWidth="1.8"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
                    <span className="font-semibold text-[#1C1E21]">OF en cours</span>
                    <span className="font-mono text-[#8A95A0]">{ofActuel.numero_of as string}</span>
                    <span className="ml-auto text-[#64748B]">{ofActuel.piece_nom as string}</span>
                  </div>
                  <div className="text-[10px] text-[#64748B]">Produit: {ofActuel.nb_pieces_produites as number} pcs</div>
                </div>
              )}
            </div>

            <div className="col-span-3 space-y-3">
              {maintKpi.data && (
                <div className="grid grid-cols-3 gap-3">
                  {["mtbf_heures","mttr_heures","nb_interventions"].map((k, i) => (
                    <div key={k} className="px-3 py-2.5 rounded-lg bg-[#F8FAFB] border border-[#E2E5E9]">
                      <div className="text-[9px] font-semibold uppercase tracking-wider text-[#5A6872]">{k === "mtbf_heures" ? "MTBF" : k === "mttr_heures" ? "MTTR" : "Interventions"}</div>
                      <div className="font-mono font-bold text-sm text-[#1C1E21] mt-0.5">
                        {k === "nb_interventions" ? (maintKpi.data?.nb_total as number || 0) : ((maintKpi.data?.mtbf_mttr as Record<string, unknown>)?.[k] as number || 0).toFixed(1)}
                        {k !== "nb_interventions" ? "h" : ""}
                      </div>
                    </div>
                  ))}
                </div>
              )}
              <div className="px-3 py-2 rounded-lg border border-[#E2E5E9] bg-white text-xs">
                <div className="flex items-center gap-2 mb-1">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#64748B" strokeWidth="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span className="font-semibold text-[#64748B] text-[10px] uppercase tracking-wider">Maintenance recente</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {(maint.data as Record<string, unknown>[] || []).slice(0, 4).map((m, i) => (
                    <Badge key={i} variant={m.statut === "TERMINE" ? "success" : "warning"}>
                      {(m.description as string || "").slice(0, 25)}
                    </Badge>
                  ))}
                  {maint.loading && <span className="text-[#8A95A0] text-[10px]">Loading...</span>}
                  {(!maint.data || (maint.data as Record<string, unknown>[]).length === 0) && !maint.loading && <span className="text-[#8A95A0] text-[10px]">Aucune maintenance recente</span>}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </PageContainer>
  );
}

function SectionHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="flex items-center gap-3 mt-6 mb-3">
      <div>
        <h2 className="text-[#1C1E21] font-bold text-sm tracking-tight">{title}</h2>
        {subtitle && <p className="text-[#8A95A0] text-[11px] mt-0.5">{subtitle}</p>}
      </div>
      <div className="flex-1 h-px bg-gradient-to-r from-[var(--border-color)] to-transparent" />
    </div>
  );
}


