import { useEffect, useState } from "react";

export function GaugeChart({
  value,
  max = 100,
  label,
  thresholds,
  size = 180,
}: {
  value: number;
  max?: number;
  label?: string;
  thresholds?: { green?: number; orange?: number };
  size?: number;
}) {
  const [animVal, setAnimVal] = useState(0);
  const gt = thresholds?.green ?? 70;
  const ot = thresholds?.orange ?? 40;
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  useEffect(() => {
    const start = performance.now();
    const from = animVal;
    const to = pct;
    const dur = 1000;
    function tick(now: number) {
      const t = Math.min((now - start) / dur, 1);
      const ease = 1 - Math.pow(1 - t, 3);
      setAnimVal(from + (to - from) * ease);
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }, [pct]);

  const color = animVal >= gt ? "#2563EB" : animVal >= ot ? "#F59E0B" : "#DC2626";
  const glowColor = animVal >= gt ? "rgba(37,99,235,0.5)" : animVal >= ot ? "rgba(245,158,11,0.5)" : "rgba(220,38,38,0.5)";

  const cx = 90;
  const cy = 90;
  const sphereR = 82;
  const arcStroke = 6;
  const arcR = sphereR - arcStroke / 2;
  const startAngle = -180;
  const sweepAngle = 180;
  const sa = (startAngle * Math.PI) / 180;
  const ea = ((startAngle + sweepAngle) * Math.PI) / 180;
  const x1 = cx + arcR * Math.cos(sa);
  const y1 = cy + arcR * Math.sin(sa);
  const x2 = cx + arcR * Math.cos(ea);
  const y2 = cy + arcR * Math.sin(ea);
  const bgArc = `M ${x1} ${y1} A ${arcR} ${arcR} 0 0 1 ${x2} ${y2}`;

  const activeAngle = startAngle + (sweepAngle * animVal) / 100;
  const aa = (activeAngle * Math.PI) / 180;
  const ax = cx + arcR * Math.cos(aa);
  const ay = cy + arcR * Math.sin(aa);
  const largeArc = 0;
  const activeArc = `M ${x1} ${y1} A ${arcR} ${arcR} 0 ${largeArc} 1 ${ax} ${ay}`;

  const angle = (animVal / 100) * 180;
  const rad = (angle - 180) * (Math.PI / 180);
  const needleLen = 60;
  const nx = cx + needleLen * Math.cos(rad);
  const ny = cy + needleLen * Math.sin(rad);

  return (
    <div className="relative flex items-center justify-center flex-shrink-0" style={{ width: size, height: size, overflow: 'hidden' }}>
      <svg width={size} height={size} viewBox="-12 -12 204 204" style={{ overflow: 'hidden' }}>
        <defs>
          <linearGradient id="gaugeGlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#DC2626" stopOpacity="0.9" />
            <stop offset={`${ot}%`} stopColor="#F59E0B" stopOpacity="0.9" />
            <stop offset={`${gt}%`} stopColor="#2563EB" stopOpacity="0.9" />
          </linearGradient>
          <filter id="gaugeGlow">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="gaugeBgGlow">
            <feGaussianBlur stdDeviation="1.5" />
          </filter>
          <radialGradient id="glassBg" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(255,255,255,0.04)" />
            <stop offset="80%" stopColor="rgba(0,0,0,0.2)" />
            <stop offset="100%" stopColor="rgba(0,0,0,0.4)" />
          </radialGradient>
        </defs>

        {/* Glass background circle */}
        <circle cx={cx} cy={cy} r={sphereR} fill="url(#glassBg)" stroke="rgba(255,255,255,0.06)" strokeWidth="1" />

        {/* Glow halo under arc */}
        <path d={bgArc} fill="none" stroke={glowColor} strokeWidth="12" strokeLinecap="round" filter="url(#gaugeBgGlow)" opacity="0.4" />

        {/* Background arc */}
        <path d={bgArc} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="6" strokeLinecap="round" />

        {/* Active arc glow */}
        <path d={activeArc} fill="none" stroke={glowColor} strokeWidth="10" strokeLinecap="round" filter="url(#gaugeGlow)" opacity="0.6" />

        {/* Active arc */}
        <path d={activeArc} fill="none" stroke={color} strokeWidth="6" strokeLinecap="round" filter="url(#gaugeGlow)" />

        {/* Needle glow */}
        <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={glowColor} strokeWidth="5" strokeLinecap="round" filter="url(#gaugeGlow)" opacity="0.4" />

        {/* Needle */}
        <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={color} strokeWidth="2.5" strokeLinecap="round" />

        {/* Center cap */}
        <circle cx={cx} cy={cy} r="5" fill={color} filter="url(#gaugeGlow)" />
        <circle cx={cx} cy={cy} r="2" fill="#1A1D21" />

        {/* Value */}
        <text x={cx} y={cy + 28} textAnchor="middle" fill="#D0C8C0" fontSize="22" fontWeight="700" fontFamily="'Consolas','Courier New',monospace">
          {Math.round(animVal)}%
        </text>

        {label && (
          <text x={cx} y={cy + 44} textAnchor="middle" fill="#38BDF8" fontSize="10" fontFamily="system-ui, sans-serif" letterSpacing="0.05em">
            {label}
          </text>
        )}
      </svg>
    </div>
  );
}
