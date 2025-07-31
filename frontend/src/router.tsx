import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import DashboardView from "./views/DashboardView";
import MetricsView from "./views/MetricsView";
import LoadingView from "./views/LoadingView";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<DashboardView />} />
          <Route path="/analizando" element={<LoadingView />} />
          <Route path="/resultados" element={<MetricsView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
