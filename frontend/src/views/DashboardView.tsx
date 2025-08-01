import SidebarDrc from "@/components/SidebarDrc";
import SidebarIzq from "@/components/SidebarIzq";
import { useLocation } from "react-router-dom";

export default function DashboardView() {
  const location = useLocation();
  const { analysis, file } = location.state || {};

  return (
    <>
      <div className="flex flex-col lg:flex-row gap-4 lg:gap-8 max-w-7xl mx-auto py-4 lg:py-10 px-2 lg:px-4">
        <SidebarIzq file={file} />
        <SidebarDrc analysis={analysis} />
      </div>
    </>
  );
}
