import SidebarDrc from "@/components/SidebarDrc";
import SidebarIzq from "@/components/SidebarIzq";

export default function MetricsView() {
  return (
    <>
      <div className="flex flex-row gap-8 max-w-7xl mx-auto py-10 px-4">
        <SidebarIzq />
        <SidebarDrc />
      </div>
    </>
  );
}
