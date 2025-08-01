import type { AnalysisResult } from "../types";
import AnalysisHeader from "./Metrics/AnalysisHeader";
import MetricsCard from "./Metrics/MetricsCard";
import ObservationsCarousel from "./Metrics/ObservationsCarousel";
import SuggestionsCard from "./Metrics/SuggestionsCard";

type SidebarDrcProps = {
  analysis: AnalysisResult;
};

export default function SidebarDrc({ analysis }: SidebarDrcProps) {
  return (
    <>
      <main className="flex-1">
        <AnalysisHeader />
        <div className="flex flex-col lg:flex-row gap-4 lg:gap-6 mb-6 lg:mb-8">
          <SuggestionsCard sugerencias={analysis.sugerencias} />
          <MetricsCard metricas={analysis.metricas} />
        </div>
        <div>
          <ObservationsCarousel observaciones={analysis.observaciones} />
        </div>
      </main>
    </>
  );
}
