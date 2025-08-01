import AnalysisHeader from "./Metrics/AnalysisHeader";
import SuggestionsCard from "./Metrics/SuggestionsCard";
import MetricsCard from "./Metrics/MetricsCard";
import ObservationsCarousel from "./Metrics/ObservationsCarousel";
import type { AnalysisResult } from "../types";

type SidebarDrcProps = {
  analysis: AnalysisResult;
};

export default function SidebarDrc({ analysis }: SidebarDrcProps) {
  return (
    <>
      <main className="flex-1">
        <AnalysisHeader />
        <div className="flex flex-row gap-6 mb-8">
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
