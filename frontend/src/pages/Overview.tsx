import { useNavigate } from "react-router-dom";
import PageContainer from "../components/layout/PageContainer";
import { KpiCard } from "../components/ui/KpiCard";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { ProgressBar } from "../components/ui/ProgressBar";
import { BarChart } from "../components/charts/BarChart";
import { AreaChart } from "../components/charts/AreaChart";
import { PieChart } from "../components/charts/PieChart";
import { AlertPanel } from "../components/alerts/AlertPanel";
import { useApi } from "../hooks/useApi";
import type { ExecutiveKPI, OEEByMachine, ProductionVsPlan, MachineStatus, ScrapByFamily, ProductionTrend, ActiveOrder, AlertItem } from "../types/api";

export default function Overview() {
  const navigate = useNavigate();

  const handleAlertClick = (alert: AlertItem) => {
    const msg = alert.message.toLowerCase();
    if (msg.includes("machine") && (msg.includes("panne") || msg.includes("maintenance"))) {
      navigate("/machines");
    } else if (msg.includes("stock")) {
      navigate("/inventory");
    }
  };
  const kpi = useApi<ExecutiveKPI>("/executive/kpi");
  const oeeByMachine = useApi<OEEByMachine[]>("/executive/oee-by-machine");
  const vsPlan = useApi<ProductionVsPlan[]>("/executive/production-vs-plan");
  const machines = useApi<MachineStatus[]>("/executive/machine-status");
  const scrap = useApi<ScrapByFamily[]>("/executive/scrap-by-family");
  const trend = useApi<ProductionTrend[]>("/executive/production-trend");
  const orders = useApi<ActiveOrder[]>("/executive/active-orders");
  const alerts = useApi<AlertItem[]>("/executive/alerts");

  const k = kpi.data;
  const oeeData = k?.oee;
  const machineCounts = k?.machines;
  const ofData = k?.ordres_fabrication;
  const retardsRaw = k?.retards;
  const retards = typeof retardsRaw === "number" ? retardsRaw : ((retardsRaw as Record<string, unknown> | undefined)?.retard as number) ?? 0;

  const alertCount = alerts.data ? alerts.data.filter((a) => a.type === "CRITICAL").length : undefined;

  return (
    <PageContainer
      title="Vue d'ensemble"
      description="Indicateurs cles de performance"
      alertCount={alertCount}
    >
      {/* KPI Cards */}
      <div className="grid grid-cols-6 gap-3">
        <KpiCard
          label="OEE Global"
          value={oeeData ? Math.round(oeeData.oee_global * 100) / 100 : 0}
          unit="%"
          icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="3" y="12" width="4" height="9" rx="1"/><rect x="10" y="7" width="4" height="14" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/></svg>}
        />
        <KpiCard
          label="Taux Rebut"
          value={oeeData ? Math.round(oeeData.taux_rebut * 100) / 100 : 0}
          unit="%"
          icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="12" cy="12" r="10"/><path d="M9 12l2 2 4-4"/></svg>}
        />
        <KpiCard
          label="Machines en marche"
          value={machineCounts?.running ?? 0}
          subtitle={`Arretees: ${machineCounts?.stopped ?? 0} | Maintenance: ${machineCounts?.maintenance ?? 0}`}
          icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42"/></svg>}
        />
        <KpiCard
          label="OF actifs"
          value={ofData?.en_cours ?? 0}
          subtitle={`En attente: ${ofData?.en_attente ?? 0} | Termines: ${ofData?.termine ?? 0}`}
          icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>}
        />
        <KpiCard
          label="Retards"
          value={retards}
          color={retards > 0 ? "#DC2626" : "#2563EB"}
          icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>}
        />
        <KpiCard
          label="Qualite"
          value={oeeData ? Math.round(oeeData.qualite * 100) / 100 : 0}
          unit="%"
          icon={<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>}
        />
      </div>

      {/* Alerts Panel */}
      {alerts.data && alerts.data.length > 0 && <AlertPanel alerts={alerts.data} onAlertClick={handleAlertClick} />}

      {/* Performance Section */}
      <div>
        <SectionHeader title="Performance Production" subtitle="OEE par machine et production vs plan" />
        <div className="grid grid-cols-5 gap-4">
          <div className="col-span-3">
            <Card>
              <CardHeader title="OEE par Machine" />
              <CardBody className="p-0">
                {oeeByMachine.data ? (
                  <BarChart
                    data={oeeByMachine.data.slice().sort((a, b) => a.oee - b.oee) as unknown as Record<string, unknown>[]}
                    xKey="code"
                    yKey="oee"
                    colorKey="oee"
                    height={320}
                  />
                ) : oeeByMachine.loading ? (
                  <div className="h-[320px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div>
                ) : null}
              </CardBody>
            </Card>
          </div>
          <div className="col-span-2">
            <Card>
              <CardHeader title="Production vs Plan" subtitle="30 derniers jours" />
              <CardBody className="p-0">
                {vsPlan.data ? (
                  <AreaChart
                    data={vsPlan.data.slice(-30) as unknown as Record<string, unknown>[]}
                    xKey="date"
                    series={[
                      { key: "planifie", name: "Planifie", color: "#2563EB" },
                      { key: "reel", name: "Reel", color: "#38BDF8" },
                    ]}
                    height={280}
                  />
                ) : vsPlan.loading ? (
                  <div className="h-[280px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div>
                ) : null}
              </CardBody>
            </Card>
          </div>
        </div>
      </div>

      {/* Machines & Quality */}
      <div>
        <SectionHeader title="Machines & Qualite" subtitle="Etat des machines et analyse des rebuts" />
        <div className="grid grid-cols-5 gap-4">
          <div className="col-span-3">
            <Card>
              <CardHeader title="Etat des Machines" />
              <CardBody className="space-y-1.5 max-h-[420px] overflow-y-auto">
                {machines.data?.map((m, i) => <MachineRow key={i} machine={m} onSelect={(code) => navigate(`/machines?machine=${code}`)} />)}
                {machines.loading && <div className="text-center py-8 text-[#8A95A0] text-sm">Loading...</div>}
              </CardBody>
            </Card>
          </div>
          <div className="col-span-2 space-y-4">
            <Card>
              <CardHeader title="Rebuts par Famille" />
              <CardBody className="p-0">
                {scrap.data ? (
                  <PieChart data={scrap.data as unknown as Record<string, unknown>[]} nameKey="famille" valueKey="nb_rebut" height={250} />
                ) : scrap.loading ? (
                  <div className="h-[250px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div>
                ) : null}
              </CardBody>
            </Card>
            <Card>
              <CardHeader title="Tendance Production" subtitle="30 derniers jours" />
              <CardBody className="p-0">
                {trend.data ? (
                  <AreaChart
                    data={trend.data.slice(-30) as unknown as Record<string, unknown>[]}
                    xKey="date"
                    series={[
                      { key: "produites", name: "Produites", color: "#2563EB" },
                      { key: "rebuts", name: "Rebuts", color: "#38BDF8" },
                    ]}
                    height={220}
                  />
                ) : trend.loading ? (
                  <div className="h-[220px] flex items-center justify-center text-[#8A95A0] text-sm">Loading...</div>
                ) : null}
              </CardBody>
            </Card>
          </div>
        </div>
      </div>

      {/* Active Orders */}
      <div>
        <SectionHeader title="Ordres de Fabrication Actifs" subtitle="Suivi des OF en cours" />
        {orders.data ? (
          <div className="space-y-2">
            {orders.data.slice(0, 10).map((of, i) => <OrderRow key={i} order={of} onSelect={(num) => navigate(`/production?of=${num}`)} />)}
          </div>
        ) : orders.loading ? (
          <div className="text-center py-8 text-[#8A95A0] text-sm">Loading...</div>
        ) : null}
      </div>
    </PageContainer>
  );
}

function SectionHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <div>
        <h2 className="text-[#1C1E21] font-bold text-base tracking-tight">{title}</h2>
        {subtitle && <p className="text-[#8A95A0] text-xs mt-0.5">{subtitle}</p>}
      </div>
      <div className="flex-1 h-px bg-gradient-to-r from-[var(--border-color)] to-transparent" />
    </div>
  );
}

function MachineRow({ machine, onSelect }: { machine: MachineStatus; onSelect?: (code: string) => void }) {
  return (
    <button onClick={() => onSelect?.(machine.code)} className="w-full flex items-center justify-between px-4 py-3 rounded-lg border border-[#E2E5E9] bg-white transition-all duration-150 hover:shadow-sm hover:-translate-y-0.5 cursor-pointer">
      <div className="flex items-center gap-3">
        <span className="font-mono font-bold text-xs text-[var(--color-copper)]">{machine.code}</span>
        <span className="text-xs text-[#5A6872]">{machine.nom}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-[10px] text-[#8A95A0]">{machine.type}</span>
        <Badge variant={machine.statut === "RUNNING" ? "success" : machine.statut === "STOPPED" ? "danger" : "warning"}>
          {machine.statut}
        </Badge>
      </div>
    </button>
  );
}

function OrderRow({ order, onSelect }: { order: ActiveOrder; onSelect?: (num: string) => void }) {
  const pct = order.avancement_pct || 0;
  const st = order.statut;
  return (
    <button onClick={() => onSelect?.(order.numero_of)} className="w-full flex items-center justify-between px-4 py-3 rounded-lg border border-[#E2E5E9] border-l-[3px] bg-white transition-all duration-150 hover:shadow-sm hover:-translate-y-0.5 cursor-pointer text-left"
      style={{ borderLeftColor: st === "EN_COURS" ? "#38BDF8" : st === "EN_RETARD" ? "#DC2626" : st === "TERMINE" ? "#2563EB" : "#94A3B8" }}
    >
      <div className="flex items-center gap-4">
        <span className="font-mono font-bold text-xs text-[var(--color-copper)]">{order.numero_of}</span>
        <span className="text-xs text-[#1C1E21]">{order.piece_ref} - {order.piece_nom?.slice(0, 40)}</span>
      </div>
      <div className="flex items-center gap-4">
        <span className="font-mono text-[11px] text-[#5A6872]">{order.quantite_produite}/{order.quantite_demandee}</span>
        <Badge variant={st === "EN_COURS" ? "warning" : st === "EN_RETARD" ? "danger" : st === "TERMINE" ? "success" : "info"}>{st}</Badge>
        {order.retard_jours ? <span className="text-[#DC2626] font-bold text-[11px]">+{order.retard_jours}j</span> : null}
        <div className="w-24">
          <ProgressBar value={pct} />
        </div>
      </div>
    </button>
  );
}

