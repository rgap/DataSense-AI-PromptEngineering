export default function Characteristics() {
  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
        <div className="bg-white rounded-xl shadow p-6 flex flex-col text-left items-start">
          <img
            src="/img/iconos/svg/rayoIcon.svg"
            alt="Icono de Analisis instantaneo"
            className="w-8 h-8 mb-2 bg-[#bad7fd] rounded-xs p-1 mr-2"
          />
          <h3 className="font-bold text-lg mb-1">Análisis Instantáneo</h3>
          <p className="text-gray-500 text-sm">
            Obtén insights en segundos con IA avanzada
          </p>
        </div>
        <div className="bg-white rounded-xl shadow p-6 flex flex-col text-left items-start">
          <img
            src="/img/iconos/svg/guardIcon.svg"
            alt=""
            className="w-8 h-8 mb-2 bg-[#bffcd4] rounded-xs p-1 mr-2"
          />
          <h3 className="font-bold text-lg mb-1">Datos Seguros</h3>
          <p className="text-gray-500 text-sm">
            Tus datos están protegidos y encriptados
          </p>
        </div>
        <div className="bg-white rounded-xl shadow p-6 flex flex-col text-left items-start">
          <img
            src="/img/iconos/svg/tortaIcon.svg"
            alt=""
            className="w-8 h-8 mb-2 bg-[#FEFCE8] rounded-xs p-1 mr-2"
          />
          <h3 className="font-bold text-lg mb-1">Visualizaciones</h3>
          <p className="text-gray-500 text-sm">
            Gráficos interactivos y fáciles de entender
          </p>
        </div>
      </div>
    </>
  );
}
