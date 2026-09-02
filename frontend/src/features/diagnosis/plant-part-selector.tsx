"use client";

import { Apple, GitBranch, Leaf, MoveRight } from "lucide-react";

import type { PlantPart } from "@/types/diagnosis";

const parts: { id: PlantPart; title: string; text: string; icon: typeof Leaf }[] = [
  { id: "leaf", title: "Hoja", text: "Manchas, color, lesiones o defoliación", icon: Leaf },
  { id: "stem", title: "Tallo / Rama", text: "Lesiones, necrosis o secamiento", icon: GitBranch },
  { id: "fruit", title: "Fruto", text: "Manchas, caída o desarrollo anormal", icon: Apple },
];

interface PlantPartSelectorProps {
  selected: PlantPart | null;
  loading: boolean;
  error: string | null;
  onSelect: (part: PlantPart) => void;
  onContinue: () => void;
}

export function PlantPartSelector({ selected, loading, error, onSelect, onContinue }: PlantPartSelectorProps) {
  return (
    <div className="diagnosis-selector">
      <div className="part-grid">
        {parts.map(({ id, title, text, icon: Icon }) => (
          <button aria-pressed={selected === id} className={selected === id ? "part-card selected" : "part-card"} key={id} onClick={() => onSelect(id)} type="button">
            <span><Icon /></span><strong>{title}</strong><small>{text}</small>
          </button>
        ))}
      </div>
      {error && <p className="diagnosis-error" role="alert">{error}</p>}
      <button className="primary-button diagnosis-next" disabled={!selected || loading} onClick={onContinue} type="button">
        {loading ? "Cargando preguntas…" : "Continuar"} {!loading && <MoveRight size={18} />}
      </button>
      <p className="diagnosis-note">Responde según lo que observas. Podrás volver y revisar tus respuestas antes del análisis.</p>
    </div>
  );
}
