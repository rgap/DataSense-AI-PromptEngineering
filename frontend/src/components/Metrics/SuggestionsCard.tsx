import type { Sugerencia } from "@/types/index";

type SuggestionsProps = {
  sugerencias: Sugerencia[];
};

export default function SuggestionsCard({ sugerencias }: SuggestionsProps) {
  return (
    <>
      <div className="flex-1 bg-white rounded-xl shadow p-6 border border-blue-200 hover:border-blue-600 transition group">
        <div className="flex items-center gap-2 mb-3">
          <img
            src="/img/iconos/svg/rayoIcon.svg"
            className="w-10 h-10 bg-[#bad7fd] rounded-xs p-2"
            alt="Icono de Sugerencias Clave"
          />
          <span className="font-bold text-blue-700 group-hover:text-blue-900">
            Sugerencias clave
          </span>
        </div>
        <ul className="list-none pl-0">
          {sugerencias.map((s, i) => (
            <li key={i} className="flex items-center gap-2 mb-1">
              <span>✅</span>
              <span>{s.mensaje}</span>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
