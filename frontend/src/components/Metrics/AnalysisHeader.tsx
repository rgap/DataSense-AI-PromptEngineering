export default function AnalysisHeader() {
  return (
    <>
      <div className="flex items-center gap-2 lg:gap-3 mb-2">
        <img src="/img/iconos/svg/robotIcon.svg" className="w-6 h-6 lg:w-8 lg:h-8" alt="Icono del robot subidor" />
        <h2 className="text-xl lg:text-3xl font-bold text-[#134CCA]">Análisis de Datos con IA</h2>
      </div>
      <div className="text-sm lg:text-base text-gray-600 mb-4 lg:mb-6">Revisión automática de calidad de datos y detección de anomalías</div>
    </>
  );
}
