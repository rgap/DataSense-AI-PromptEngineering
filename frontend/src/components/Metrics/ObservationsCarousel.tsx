import { useState } from "react";
const mockObservations = [
  {
    type: "error",
    title: "220 columna name hay duplicados",
    description:
      "Se detectaron registros duplicados que podrían afectar la precisión del análisis",
  },
  {
    type: "warning",
    title: "Valores nulos esperados en Moves.csv",
    description:
      "Algunos campos contienen valores vacíos que son normales para este tipo de datos",
  },
  {
    type: "success",
    title: "Estructura de datos válida",
    description:
      "El esquema general del archivo cumple con los estándares esperados",
  },
  {
    type: "warning",
    title: "Formato inconsistente en columna #3",
    description:
      "La columna de fechas presenta diferentes formatos que requieren normalización",
  },
];

export default function ObservationsCarousel() {
  const [obsPage, setObsPage] = useState(0);

  // Observaciones
  const obsPerPage = 3;
  const obsTotalPages = Math.ceil(mockObservations.length / obsPerPage);
  const obsToShow = mockObservations.slice(
    obsPage * obsPerPage,
    (obsPage + 1) * obsPerPage
  );
  return (
    <>
      <div className="flex justify-between">
        <h3 className="text-2xl font-bold text-[#134CCA] mb-4">
          Observaciones del análisis de IA
        </h3>

        <div className="gap-2 flex">
          {/* Flecha izquierda */}
          <button
            className={`self-center p-2 rounded-lg transition ${
              obsPage === 0
                ? "bg-gray-200 cursor-not-allowed"
                : "bg-blue-100 hover:bg-[#95B3F5]"
            }`}
            disabled={obsPage === 0}
            onClick={() => setObsPage((p) => Math.max(0, p - 1))}
          >
            <img
              src="/img/iconos/svg/arrowLeft.svg"
              className="w-5 h-5"
              alt="Anterior"
            />
          </button>
          {/* Flecha derecha */}
          <button
            className={`self-center p-2 rounded-lg transition ${
              obsPage >= obsTotalPages - 1
                ? "bg-gray-200 cursor-not-allowed"
                : "bg-blue-100 hover:bg-[#95B3F5]"
            }`}
            disabled={obsPage >= obsTotalPages - 1}
            onClick={() =>
              setObsPage((p) => Math.min(obsTotalPages - 1, p + 1))
            }
          >
            <img
              src="/img/iconos/svg/arrowRight.svg"
              className="w-5 h-5"
              alt="Siguiente"
            />
          </button>
        </div>
      </div>

      <div className="flex flex-row gap-4 items-stretch">
        {/* Observaciones */}
        {obsToShow.map((obs, i) => (
          <div
            key={i}
            className={`flex-1 flex gap-2 rounded-xl shadow p-4 border-l-4 ${
              obs.type === "error"
                ? "border-red-400 bg-red-50"
                : obs.type === "warning"
                ? "border-yellow-400 bg-yellow-50"
                : "border-green-400 bg-green-50"
            }`}
          >
            {obs.type === "error" ? (
              <img
                src="/img/iconos/svg/warningIcon.svg"
                className="w-4 h-4"
                alt="Icono de alerta de peligro"
              />
            ) : obs.type === "warning" ? (
              <img
                src="/img/iconos/svg/adviceIcon.svg"
                className="w-4 h-4"
                alt="Icono de alerta de advertencia"
              />
            ) : (
              <img
                src="/img/iconos/svg/tortaIcon.svg"
                className="w-4 h-4"
                alt="Icono de alerta cumplido"
              />
            )}
            <div className="flex flex-col gap-2">
              <p className="font-bold mb-1 text-base">{obs.title}</p>
              <p className="text-sm text-gray-700">{obs.description}</p>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
