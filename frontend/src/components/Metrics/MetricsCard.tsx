import type { Metricas } from "@/types/index";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";

type MetricsCardProps = {
  metricas: Metricas;
};

export default function MetricsCard({ metricas }: MetricsCardProps) {
  const data = [
    {
      name: "Valores faltantes",
      value: metricas.porcentaje_valores_faltantes,
      color: "#FBBF24",
    },
    {
      name: "Duplicados",
      value: metricas.porcentaje_filas_duplicadas,
      color: "#34D399",
    },
    { name: "Salud", value: metricas.salud_del_dataset, color: "#60A5FA" },
  ];
  return (
    <>
      <div className="flex-1 bg-white rounded-xl shadow p-4 lg:p-6 border border-yellow-100 hover:border-yellow-400 transition group">
        <div className="flex items-center gap-2 mb-3">
          <img src="/img/iconos/svg/tortaIcon.svg" className="w-8 h-8 lg:w-10 lg:h-10 bg-[#fcf5ac] rounded-xs p-2" alt="Icono de grafico de torta" />
          <span className="font-bold text-sm lg:text-base text-yellow-600 group-hover:text-yellow-700">Métricas de calidad</span>
        </div>
        <div className="flex flex-col sm:flex-row gap-4 items-center">
          <div className="flex-shrink-0">
            <ResponsiveContainer width={100} height={100}>
              <PieChart>
                <Pie
                  data={data}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={25}
                  outerRadius={45}
                  paddingAngle={3}
                  startAngle={90}
                  endAngle={-270}
                >
                  {data.map(entry => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-col gap-2 w-full">
            {data.map((m, i) => (
              <div key={i} className="flex items-center justify-between sm:justify-start gap-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full inline-block" style={{ background: m.color }}></span>
                  <span className="text-gray-700">{m.name}</span>
                </div>
                <span className="font-semibold">{m.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
