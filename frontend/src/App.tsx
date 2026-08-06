import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";

const Overview = lazy(() => import("./pages/Overview"));
const Machine = lazy(() => import("./pages/Machine"));
const Production = lazy(() => import("./pages/Production"));
const Quality = lazy(() => import("./pages/Quality"));
const Inventory = lazy(() => import("./pages/Inventory"));
const Tool = lazy(() => import("./pages/Tool"));
const Maintenance = lazy(() => import("./pages/Maintenance"));

function isAuthenticated() {
  const token = localStorage.getItem("amip_token");
  if (!token) return false;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    if (payload.exp * 1000 < Date.now()) {
      localStorage.removeItem("amip_token");
      localStorage.removeItem("amip_user");
      return false;
    }
    return true;
  } catch {
    return false;
  }
}

function Logout() {
  localStorage.removeItem("amip_token");
  localStorage.removeItem("amip_user");
  window.location.href = "/";
  return null;
}

function Loading() {
  return (
    <div className="min-h-screen bg-[var(--color-bg-warm)] flex items-center justify-center">
      <div className="flex items-center gap-3 text-[var(--color-text-secondary)]">
        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <span className="text-sm">Loading...</span>
      </div>
    </div>
  );
}

export default function App() {
  const authed = isAuthenticated();

  if (!authed) {
    return (
      <Routes>
        <Route path="*" element={<Login />} />
      </Routes>
    );
  }

  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/machines" element={<Machine />} />
        <Route path="/production" element={<Production />} />
        <Route path="/quality" element={<Quality />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/tool" element={<Tool />} />
        <Route path="/maintenance" element={<Maintenance />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="*" element={<Overview />} />
      </Routes>
    </Suspense>
  );
}
