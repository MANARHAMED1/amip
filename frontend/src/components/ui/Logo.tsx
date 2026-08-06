interface LogoFullProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizes = { sm: 120, md: 160, lg: 200 };
const heights = { sm: 42, md: 56, lg: 70 };

export function LogoFull({ size = "md", className }: LogoFullProps) {
  const w = sizes[size];
  const h = heights[size];
  const s = w;
  const svgH = h;
  return (
    <svg
      width={w}
      height={h}
      viewBox={`0 0 ${w} ${h}`}
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#2563EB" />
          <stop offset="100%" stopColor="#38BDF8" />
        </linearGradient>
      </defs>
      <g transform={`translate(0,${Math.round(svgH * 0.08)})`}>
        <path
          d={`M${Math.round(s * 0.045)} ${Math.round(svgH * 0.82)} L${Math.round(s * 0.115)} ${Math.round(svgH * 0.12)} L${Math.round(s * 0.185)} ${Math.round(svgH * 0.82)}`}
          stroke="url(#logoGrad)"
          strokeWidth={2.5}
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <line
          x1={Math.round(s * 0.065)}
          y1={Math.round(svgH * 0.55)}
          x2={Math.round(s * 0.155)}
          y2={Math.round(svgH * 0.55)}
          stroke="url(#logoGrad)"
          strokeWidth={2}
          strokeLinecap="round"
        />
          <circle
          cx={Math.round(s * 0.115)}
          cy={Math.round(svgH * 0.55)}
          r={Math.max(2, Math.round(s * 0.012))}
              fill="#38BDF8"
        />
        <path
          d={`M${Math.round(s * 0.185)} ${Math.round(svgH * 0.2)} L${Math.round(s * 0.205)} ${Math.round(svgH * 0.15)} L${Math.round(s * 0.205)} ${Math.round(svgH * 0.25)} Z`}
              fill="#38BDF8"
          opacity={0.6}
        />
        <path
          d={`M${Math.round(s * 0.185)} ${Math.round(svgH * 0.35)} L${Math.round(s * 0.21)} ${Math.round(svgH * 0.28)} L${Math.round(s * 0.21)} ${Math.round(svgH * 0.42)} Z`}
              fill="#38BDF8"
          opacity={0.4}
        />
        <path
          d={`M${Math.round(s * 0.185)} ${Math.round(svgH * 0.55)} L${Math.round(s * 0.215)} ${Math.round(svgH * 0.46)} L${Math.round(s * 0.215)} ${Math.round(svgH * 0.64)} Z`}
              fill="#38BDF8"
          opacity={0.25}
        />
      </g>
      <text
        x={Math.round(s * 0.25)}
        y={Math.round(svgH * 0.52)}
        fontFamily="system-ui, -apple-system, sans-serif"
        fontSize={Math.round(s * 0.145)}
        fontWeight={800}
        fill="#2563EB"
        letterSpacing="-0.03em"
      >
        {size === "sm" ? "A" : "AMIP"}
      </text>
      {size !== "sm" && (
        <text
          x={Math.round(s * 0.25)}
          y={Math.round(svgH * 0.78)}
          fontFamily="system-ui, -apple-system, sans-serif"
          fontSize={Math.round(s * 0.045)}
          fontWeight={600}
          fill="var(--color-text-secondary)"
          letterSpacing="0.12em"
        >
          ADVANCED MANUFACTURING INTELLIGENCE
        </text>
      )}
    </svg>
  );
}

interface LogoIconProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

const iconSizes = { sm: 28, md: 36, lg: 48, xl: 64 };

export function LogoIcon({ size = "md", className }: LogoIconProps) {
  const sz = iconSizes[size];
  return (
    <svg
      width={sz}
      height={sz}
      viewBox={`0 0 ${sz} ${sz}`}
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <linearGradient id="logoIconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#2563EB" />
          <stop offset="100%" stopColor="#38BDF8" />
        </linearGradient>
      </defs>
      <rect
        width={sz}
        height={sz}
        rx={Math.round(sz * 0.22)}
        fill="url(#logoIconGrad)"
      />
      <path
        d={`M${Math.round(sz * 0.3)} ${Math.round(sz * 0.78)} L${Math.round(sz * 0.5)} ${Math.round(sz * 0.22)} L${Math.round(sz * 0.7)} ${Math.round(sz * 0.78)}`}
        stroke="white"
        strokeWidth={Math.max(1.5, sz * 0.05)}
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <line
        x1={Math.round(sz * 0.37)}
        y1={Math.round(sz * 0.56)}
        x2={Math.round(sz * 0.63)}
        y2={Math.round(sz * 0.56)}
        stroke="white"
        strokeWidth={Math.max(1.2, sz * 0.04)}
        strokeLinecap="round"
      />
      <circle
        cx={Math.round(sz * 0.5)}
        cy={Math.round(sz * 0.56)}
        r={Math.max(1.2, sz * 0.035)}
        fill="white"
      />
      <path
        d={`M${Math.round(sz * 0.7)} ${Math.round(sz * 0.3)} L${Math.round(sz * 0.76)} ${Math.round(sz * 0.22)} L${Math.round(sz * 0.76)} ${Math.round(sz * 0.38)} Z`}
        fill="white"
        opacity={0.5}
      />
      <path
        d={`M${Math.round(sz * 0.7)} ${Math.round(sz * 0.46)} L${Math.round(sz * 0.78)} ${Math.round(sz * 0.36)} L${Math.round(sz * 0.78)} ${Math.round(sz * 0.56)} Z`}
        fill="white"
        opacity={0.3}
      />
    </svg>
  );
}
