import AnalysisHeader from "./Metrics/AnalysisHeader";
import SuggestionsCard from "./Metrics/SuggestionsCard";
import MetricsCard from "./Metrics/MetricsCard";
import ObservationsCarousel from "./Metrics/ObservationsCarousel";

export default function SidebarDrc() {
  return (
    <>
      <main className="flex-1">
        <AnalysisHeader />
        <div className="flex flex-row gap-6 mb-8">
          <SuggestionsCard />
          <MetricsCard />
        </div>
        <div>
          <ObservationsCarousel />
        </div>
      </main>
    </>
  );
}
