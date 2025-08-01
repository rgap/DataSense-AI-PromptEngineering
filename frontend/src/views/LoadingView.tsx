import { analyzeDataset } from "@/api/datasetAnalysisApi";
import Characteristics from "@/components/Characteristics";
import Title from "@/components/Title";
import { useMutation } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

const steps = [
  {
    icon: "/img/iconos/png/checkBlue.png",
    label: "Cargando",
  },
  {
    icon: "/img/iconos/png/LoadIcon.png",
    label: "Analizando",
  },
  {
    icon: "/img/iconos/png/metricsIcon.png",
    label: "Terminado",
  },
];

export default function LoadingView() {
  const [progress, setProgress] = useState(0);
  const location = useLocation();
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const { file } = location.state || {};

  const mutation = useMutation({
    mutationFn: analyzeDataset,
    onError: () => {
      toast.error("Error al analizar el archivo.");
      navigate("/"); // Redirect back to home on error
    },
    onSuccess: data => {
      setStep(2);
      setProgress(100);
      setTimeout(() => {
        navigate("/resultados", { state: { analysis: data, file } });
      }, 1200);
    },
  });

  // Trigger the analysis when component mounts if file exists
  useEffect(() => {
    if (file && !mutation.isPending && !mutation.isSuccess) {
      mutation.mutate(file);
    }
  }, [file, mutation]);

  // Handle progress simulation while API call is in progress
  useEffect(() => {
    if (mutation.isPending && progress < 90) {
      const interval = setInterval(() => {
        setProgress(prev => {
          const next = prev + Math.random() * 8 + 3;
          if (next >= 90) return 90; // Cap at 90% until API completes
          return next;
        });
      }, 500);
      return () => clearInterval(interval);
    }
  }, [mutation.isPending, progress]);

  // Update steps based on mutation state and progress
  useEffect(() => {
    if (mutation.isPending) {
      if (progress < 30) setStep(0);
      else setStep(1);
    } else if (mutation.isSuccess) {
      setStep(2);
    }
  }, [mutation.isPending, mutation.isSuccess, progress]);

  // Redirect to home if no file is provided
  useEffect(() => {
    if (!file) {
      toast.error("No se encontró el archivo. Por favor, selecciona un archivo.");
      navigate("/");
    }
  }, [file, navigate]);

  // Colores y opacidad según el paso
  const getStepStyle = (idx: number) =>
    idx < step
      ? "border-blue-600 text-blue-600 bg-white"
      : idx === step
      ? "border-blue-600 text-blue-600 bg-white opacity-100"
      : "border-gray-300 text-gray-300 bg-white opacity-40";

  return (
    <div className="flex flex-col items-center px-4 py-10 max-w-5xl mx-auto">
      <Title />
      <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg p-10 mb-10 flex flex-col items-center">
        {/* Barra de pasos */}
        <div className="flex items-center w-full justify-between mb-6">
          {/* Paso 1 */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 transition-all duration-300 ${getStepStyle(0)}`}>
              <img src={steps[0].icon} alt="" className="w-10 h-10" />
            </div>
          </div>
          {/* Línea */}
          <div
            className={`h-1 flex-1 mx-2 transition-all duration-300 ${step > 0 ? "bg-blue-600" : "bg-gray-200"}`}
            style={{
              opacity: step > 0 ? 1 : 0.4,
              height: "4px",
              marginTop: "38px",
            }}
          />
          {/* Paso 2 */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 transition-all duration-300 ${getStepStyle(1)}`}>
              <img src={steps[1].icon} alt="" className="w-10 h-10" />
            </div>
          </div>
          {/* Línea */}
          <div
            className={`h-1 flex-1 mx-2 transition-all duration-300 ${step > 1 ? "bg-blue-600" : "bg-gray-200"}`}
            style={{
              opacity: step > 1 ? 1 : 0.4,
              height: "4px",
              marginTop: "38px",
            }}
          />
          {/* Paso 3 */}
          <div className="flex flex-col items-center flex-1">
            <div className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 transition-all duration-300 ${getStepStyle(2)}`}>
              <img src={steps[2].icon} alt="" className="w-10 h-10" />
            </div>
          </div>
        </div>
        {/* Texto de estado */}
        <div className="text-center mt-4">
          <span className="text-2xl font-bold text-gray-700">
            {mutation.isPending && step === 0 && "Cargando archivo..."}
            {mutation.isPending && step === 1 && "Analizando con IA..."}
            {mutation.isSuccess && step === 2 && "¡Análisis completado!"}
            {mutation.isError && "Error en el análisis"}
          </span>
          {mutation.isPending && <p className="text-sm text-gray-500 mt-2">Esto puede tomar unos momentos...</p>}
        </div>
      </div>
      <Characteristics />
    </div>
  );
}
