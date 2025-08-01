import type { Sugerencia } from "@/types/index";

type SuggestionsProps = {
  sugerencias: Sugerencia[];
};

export default function SuggestionsCard({ sugerencias }: SuggestionsProps) {
  return (
    <>
      <div className="flex-1 bg-white rounded-xl shadow p-4 lg:p-6 border border-blue-200 hover:border-blue-600 transition group">
        <div className="flex items-center gap-2 mb-3">
          <img src="/img/iconos/svg/rayoIcon.svg" className="w-8 h-8 lg:w-10 lg:h-10 bg-[#bad7fd] rounded-xs p-2" alt="Icono de Sugerencias Clave" />
          <span className="font-bold text-sm lg:text-base text-blue-700 group-hover:text-blue-900">Sugerencias clave</span>
        </div>
        <ul className="list-none pl-0 space-y-2">
          {sugerencias.map((s, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="flex-shrink-0 mt-0.5">✅</span>
              <span className="text-sm lg:text-base">{s.mensaje}</span>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
