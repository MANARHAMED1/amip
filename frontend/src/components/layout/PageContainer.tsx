import { useState, type ReactNode } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

export default function PageContainer({
  title,
  description,
  alertCount,
  headerContent,
  children,
}: {
  title: string;
  description?: string;
  alertCount?: number;
  headerContent?: ReactNode;
  children: ReactNode;
}) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--color-bg-warm)]">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5">
          <Header title={title} description={description} alertCount={alertCount} />
          {headerContent}
          {children}
        </div>
      </div>
    </div>
  );
}
