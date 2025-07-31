import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const data = [
  { name: "Errores de formato", value: 4.5, color: "#F87171" },
  { name: "Valores nulos", value: 6.3, color: "#FBBF24" },
  { name: "Duplicados", value: 17.1, color: "#34D399" },
];

export default function MetricsCard() {
  return (
    <>
      <div className="flex-1 bg-white rounded-xl shadow p-6 border border-yellow-100 hover:border-yellow-400 transition group">
        <div className="flex items-center gap-2 mb-3">
          <img
            src="/img/iconos/svg/tortaIcon.svg"
            className="w-10 h-10 bg-[#fcf5ac] rounded-xs p-2"
            alt="Icono de grafico de torta"
          />
          <span className="font-bold text-yellow-600 group-hover:text-yellow-700">
            Métricas de calidad
          </span>
        </div>
        <div className="flex flex-row gap-4 items-center">
          <ResponsiveContainer width={120} height={120}>
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={35}
                outerRadius={55}
                paddingAngle={3}
                startAngle={90}
                endAngle={-270}
              >
                {data.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-col gap-2">
            {data.map((m, i) => (
              <div key={i} className="flex items-center gap-2 text-xs">
                <span
                  className="w-3 h-3 rounded-full inline-block"
                  style={{ background: m.color }}
                ></span>
                <span className="font-semibold">{m.value}%</span>
                <span className="text-gray-700">{m.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
