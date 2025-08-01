import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Title from "@/components/Title";
import Characteristics from "@/components/Characteristics";

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
  const { analysis, file } = location.state || {};

  useEffect(() => {
    if (progress < 100) {
      const interval = setInterval(() => {
        setProgress((prev) => {
          const next = prev + Math.random() * 10 + 5;
          if (next >= 100) return 100;
          return next;
        });
      }, 400);
      return () => clearInterval(interval);
    } else {
      setStep(2);
      setTimeout(() => {
        navigate("/resultados", { state: { analysis: analysis, file } });
      }, 1200); // Espera un poco antes de redirigir
    }
  }, [progress, navigate, analysis, file]);

  useEffect(() => {
    if (progress < 40) setStep(0);
    else if (progress < 100) setStep(1);
    else setStep(2);
  }, [progress]);

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
            <div
              className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 transition-all duration-300 ${getStepStyle(
                0
              )}`}
            >
              <img src={steps[0].icon} alt="" className="w-10 h-10" />
            </div>
          </div>
          {/* Línea */}
          <div
            className={`h-1 flex-1 mx-2 transition-all duration-300 ${
              step > 0 ? "bg-blue-600" : "bg-gray-200"
            }`}
            style={{
              opacity: step > 0 ? 1 : 0.4,
              height: "4px",
              marginTop: "38px",
            }}
          />
          {/* Paso 2 */}
          <div className="flex flex-col items-center flex-1">
            <div
              className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 transition-all duration-300 ${getStepStyle(
                1
              )}`}
            >
              <img src={steps[1].icon} alt="" className="w-10 h-10" />
            </div>
          </div>
          {/* Línea */}
          <div
            className={`h-1 flex-1 mx-2 transition-all duration-300 ${
              step > 1 ? "bg-blue-600" : "bg-gray-200"
            }`}
            style={{
              opacity: step > 1 ? 1 : 0.4,
              height: "4px",
              marginTop: "38px",
            }}
          />
          {/* Paso 3 */}
          <div className="flex flex-col items-center flex-1">
            <div
              className={`w-20 h-20 rounded-full border-4 flex items-center justify-center mb-2 transition-all duration-300 ${getStepStyle(
                2
              )}`}
            >
              <img src={steps[2].icon} alt="" className="w-10 h-10" />
            </div>
          </div>
        </div>
        {/* Texto de estado */}
        <div className="text-center mt-4">
          <span className="text-2xl font-bold text-gray-700">
            {step === 0 && "Cargando"}
            {step === 1 && "Analizando"}
            {step === 2 && "Terminado"}
          </span>
        </div>
      </div>
      <Characteristics />
    </div>
  );
}
