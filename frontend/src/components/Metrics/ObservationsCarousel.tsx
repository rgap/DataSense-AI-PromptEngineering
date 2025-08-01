import { useEffect, useState } from "react";
import type { Observacion } from "../../types/index";

type ObservationsProps = {
  observaciones: Observacion[];
};

export default function ObservationsCarousel({ observaciones }: ObservationsProps) {
  const [obsPage, setObsPage] = useState(0);
  const [obsPerPage, setObsPerPage] = useState(3);

  // Update items per page based on screen size
  useEffect(() => {
    const updateItemsPerPage = () => {
      setObsPerPage(window.innerWidth < 1024 ? 1 : 3);
      setObsPage(0); // Reset to first page when changing layout
    };

    updateItemsPerPage();
    window.addEventListener("resize", updateItemsPerPage);
    return () => window.removeEventListener("resize", updateItemsPerPage);
  }, []);

  const obsTotalPages = Math.ceil(observaciones.length / obsPerPage);
  const obsToShow = observaciones.slice(obsPage * obsPerPage, (obsPage + 1) * obsPerPage);

  return (
    <>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <h3 className="text-lg lg:text-2xl font-bold text-[#134CCA]">Observaciones del análisis de IA</h3>

        <div className="gap-2 flex">
          {/* Flecha izquierda */}
          <button
            className={`self-center p-2 rounded-lg transition ${obsPage === 0 ? "bg-gray-200 cursor-not-allowed" : "bg-blue-100 hover:bg-[#95B3F5]"}`}
            disabled={obsPage === 0}
            onClick={() => setObsPage(p => Math.max(0, p - 1))}
          >
            <img src="/img/iconos/svg/arrowLeft.svg" className="w-4 h-4 lg:w-5 lg:h-5" alt="Anterior" />
          </button>
          {/* Flecha derecha */}
          <button
            className={`self-center p-2 rounded-lg transition ${
              obsPage >= obsTotalPages - 1 ? "bg-gray-200 cursor-not-allowed" : "bg-blue-100 hover:bg-[#95B3F5]"
            }`}
            disabled={obsPage >= obsTotalPages - 1}
            onClick={() => setObsPage(p => Math.min(obsTotalPages - 1, p + 1))}
          >
            <img src="/img/iconos/svg/arrowRight.svg" className="w-4 h-4 lg:w-5 lg:h-5" alt="Siguiente" />
          </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-4 items-stretch">
        {/* Observaciones */}
        {obsToShow.map((obs, i) => (
          <div key={i} className={`flex-1 flex gap-2 rounded-xl shadow p-3 lg:p-4 border-[#C79425] border-2 bg-[#FEFCE8]`}>
            <img src="/img/iconos/svg/adviceIcon.svg" className="w-4 h-4 flex-shrink-0 mt-1" alt="Icono de alerta de advertencia" />
            <div className="flex flex-col gap-2">
              <p className="font-bold mb-1 text-sm lg:text-base">{obs.titulo}</p>
              <p className="text-xs lg:text-sm text-gray-700">{obs.mensaje}</p>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
