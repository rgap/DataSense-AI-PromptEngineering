import SidebarDrc from "@/components/SidebarDrc";
import SidebarIzq from "@/components/SidebarIzq";
import { useLocation } from "react-router-dom";

export default function DashboardView() {
  const location = useLocation();
  const { analysis, file } = location.state || {};

  return (
    <>
      <div className="flex flex-row gap-8 max-w-7xl mx-auto py-10 px-4">
        <SidebarIzq file={file} />
        <SidebarDrc analysis={analysis} />
      </div>
    </>
  );
}
