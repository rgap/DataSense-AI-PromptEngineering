import { BrowserRouter, Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import DashboardView from "./views/DashboardView";
import HomeView from "./views/HomeView";
import LoadingView from "./views/LoadingView";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<HomeView />} />
          <Route path="/analizando" element={<LoadingView />} />
          <Route path="/resultados" element={<DashboardView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
