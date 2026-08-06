/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          50: "#f0f3f8",
          100: "#d9e0ed",
          200: "#b3c1db",
          300: "#8da2c9",
          400: "#6783b7",
          500: "#0B2545",
          600: "#091e3a",
          700: "#07172f",
          800: "#051024",
          900: "#030918",
        },
        steel: {
          50: "#f2f6f9",
          100: "#dee7ef",
          200: "#bdcfe0",
          300: "#9cb7d1",
          400: "#7b9fc2",
          500: "#5B7B9A",
          600: "#4a6580",
          700: "#3a4f66",
          800: "#2a394c",
          900: "#1a2432",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "'Segoe UI'",
          "Roboto",
          "'Helvetica Neue'",
          "Arial",
          "sans-serif",
        ],
        mono: ["'SF Mono'", "'Cascadia Code'", "'Consolas'", "'Courier New'", "monospace"],
      },
      animation: {
        "fade-in": "fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards",
        "slide-up": "slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards",
        "pulse-soft": "pulseSoft 2.5s ease-in-out infinite",
        "gradient-shift": "gradientShift 8s ease infinite",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        slideUp: {
          from: { opacity: "0", transform: "translateY(16px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        pulseSoft: {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(198,40,40,0.15)" },
          "50%": { boxShadow: "0 0 0 6px rgba(198,40,40,0.05)" },
        },
        gradientShift: {
          "0%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
          "100%": { backgroundPosition: "0% 50%" },
        },
      },
    },
  },
  plugins: [],
};
