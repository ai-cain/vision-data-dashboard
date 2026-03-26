import {
  Activity,
  ClipboardCheck,
  Cpu,
  LayoutDashboard,
  Router,
} from "lucide-react";
import { NavLink, Outlet, useLocation } from "react-router-dom";

import { cn } from "@/lib/utils";

const routeMeta: Record<string, { eyebrow: string; title: string; subtitle: string }> = {
  "/": {
    eyebrow: "Operations Cockpit",
    title: "Vision control plane",
    subtitle: "Real-time visibility into device health, model events, and inspection quality.",
  },
  "/devices": {
    eyebrow: "Fleet View",
    title: "Edge device fleet",
    subtitle: "Track status, last heartbeat, and recent event activity across your deployed hardware.",
  },
  "/events": {
    eyebrow: "Event Log",
    title: "Model event stream",
    subtitle: "Filter detections, anomalies, and count results while keeping export-ready records.",
  },
  "/inspections": {
    eyebrow: "Inspection QA",
    title: "Inspection outcomes",
    subtitle: "Monitor pass rate, defects, and the evidence trail for industrial inspection jobs.",
  },
};

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/devices", label: "Devices", icon: Cpu },
  { to: "/events", label: "Events", icon: Activity },
  { to: "/inspections", label: "Inspections", icon: ClipboardCheck },
];

export function AppShell() {
  const location = useLocation();
  const meta = routeMeta[location.pathname] ?? routeMeta["/"];

  return (
    <div className="industrial-shell min-h-screen">
      <div className="mx-auto flex min-h-screen max-w-[1600px] gap-6 px-4 py-4 lg:px-6">
        <aside className="hidden w-80 shrink-0 rounded-[32px] bg-panel px-6 py-7 text-white shadow-panel lg:flex lg:flex-col">
          <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-white/60">Industrial Edge</p>
            <h1 className="mt-3 text-3xl font-bold">Vision Data Dashboard</h1>
            <p className="mt-3 text-sm leading-6 text-white/70">
              Observability for CV pipelines, inspection jobs, and the devices that keep them online.
            </p>
          </div>

          <nav className="mt-8 flex flex-col gap-2">
            {links.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-2xl border border-transparent px-4 py-3 text-sm text-white/75 transition",
                    isActive
                      ? "border-white/15 bg-white/10 text-white"
                      : "hover:border-white/10 hover:bg-white/5 hover:text-white",
                  )
                }
              >
                <Icon className="h-4 w-4" />
                <span>{label}</span>
              </NavLink>
            ))}
          </nav>

          <div className="mt-auto rounded-[28px] border border-white/10 bg-gradient-to-br from-white/10 to-white/5 p-5">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-white/55">System routing</p>
            <div className="mt-4 flex items-start gap-3">
              <div className="rounded-2xl bg-white/10 p-3">
                <Router className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-semibold">Live data path</p>
                <p className="mt-2 text-sm leading-6 text-white/70">
                  Device heartbeat and event traffic land in the API and refresh every 20-30 seconds in the UI.
                </p>
              </div>
            </div>
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col gap-6">
          <header className="rounded-[32px] border border-ink/10 bg-paper/90 px-6 py-5 shadow-panel backdrop-blur">
            <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <p className="font-mono text-xs uppercase tracking-[0.22em] text-ink/45">{meta.eyebrow}</p>
                <h2 className="mt-3 text-4xl font-bold text-ink">{meta.title}</h2>
                <p className="mt-3 max-w-3xl text-sm leading-6 text-ink/65">{meta.subtitle}</p>
              </div>
              <div className="flex flex-wrap gap-2 lg:hidden">
                {links.map(({ to, label }) => (
                  <NavLink
                    key={to}
                    to={to}
                    className={({ isActive }) =>
                      cn(
                        "rounded-full border px-4 py-2 text-sm transition",
                        isActive
                          ? "border-ember bg-ember text-white"
                          : "border-ink/15 bg-white text-ink",
                      )
                    }
                  >
                    {label}
                  </NavLink>
                ))}
              </div>
            </div>
          </header>

          <main className="pb-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
