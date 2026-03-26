import { Suspense, lazy } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "@/components/layout/AppShell";

const DashboardPage = lazy(() =>
  import("@/pages/Dashboard").then((module) => ({ default: module.DashboardPage })),
);
const DevicesPage = lazy(() =>
  import("@/pages/Devices").then((module) => ({ default: module.DevicesPage })),
);
const EventsPage = lazy(() =>
  import("@/pages/Events").then((module) => ({ default: module.EventsPage })),
);
const InspectionsPage = lazy(() =>
  import("@/pages/Inspections").then((module) => ({ default: module.InspectionsPage })),
);

function App() {
  return (
    <Suspense fallback={<div className="p-6 text-sm text-ink/65">Loading interface...</div>}>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/devices" element={<DevicesPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/inspections" element={<InspectionsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </Suspense>
  );
}

export default App;
