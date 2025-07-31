const mockFileInfo = {
  name: "sales_data.csv",
  date: "15 Ene 2024",
  records: 12847,
  size: "2.4 MB",
  recent: [
    { name: "sales_data.csv", date: "14 Enero 2024" },
    { name: "inventory.csv", date: "12 Enero 2024" },
  ],
};

export default function SidebarIzq() {
  return (
    <>
      <aside
        className="w-80 flex-col flex-shrink-0 justify-between h-full min-h-screen shadow-2xl border-r border-gray-200 bg-white sticky top-0 rounded-lg px-6 py-8 z-10"
        style={{
          boxShadow: "8px 0 32px 0 rgba(44, 62, 80, 0.10)",
        }}
      >
        <div className="bg-[#E4ECFF] rounded-xl shadow p-6 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <img
              src="/img/iconos/svg/csvFile.svg"
              className="w-6 h-6"
              alt="Icono de archivo CSV"
            />
            <span className="font-semibold text-lg">{mockFileInfo.name}</span>
          </div>
          <div className="text-sm text-gray-500 mb-2">Archivo actual</div>
          <div className="text-sm mb-1 flex justify-between">
            Fecha de análisis:{" "}
            <span className="text-[#134CCA] font-medium">
              {mockFileInfo.date}
            </span>
          </div>
          <div className="text-sm mb-1 flex justify-between">
            Registros:{" "}
            <span className="text-[#134CCA] font-medium">
              {mockFileInfo.records.toLocaleString()}
            </span>
          </div>
          <div className="text-sm mb-4 flex justify-between">
            Tamaño:{" "}
            <span className="text-[#134CCA] font-medium">
              {mockFileInfo.size}
            </span>
          </div>
        </div>
        <button className="w-full py-2 rounded-lg bg-gradient-to-r from-[#094FC2] to-[#5A38AA] text-white font-bold shadow hover:opacity-90 transition cursor-pointer">
          <span className="inline-flex items-center gap-2">
            <img
              src="/img/iconos/svg/reupload.svg"
              className="w-5 h-5"
              alt=""
            />
            Subir nuevo archivo
          </span>
        </button>
        <div className="mt-10">
          <h2 className="font-bold text-2xl mb-2">Archivos recientes</h2>
          <ul>
            {mockFileInfo.recent.map((f) => (
              <li
                key={f.name}
                className="flex items-center gap-2 text-gray-400 text-sm mb-1"
              >
                <img
                  src="/img/iconos/svg/csvFile.svg"
                  className="w-4 h-4"
                  alt=""
                />
                <div className="flex flex-col gap-1">
                  <span className="text-black text-xl">{f.name}</span>
                  <span className="">{f.date}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </aside>
    </>
  );
}
