import { Check } from "lucide-react";

import type { QuestionOption } from "@/types/diagnosis";

interface OptionCardProps {
  option: QuestionOption;
  selected: boolean;
  multiple?: boolean;
  onSelect: () => void;
}

export function OptionCard({ option, selected, multiple = false, onSelect }: OptionCardProps) {
  return (
    <button
      aria-pressed={selected}
      className={selected ? "option-card selected" : "option-card"}
      onClick={onSelect}
      type="button"
    >
      <span className={multiple ? "option-indicator square" : "option-indicator"}>{selected && <Check />}</span>
      <span className="option-copy">
        <strong>{option.label}</strong>
        {option.description && <small>{option.description}</small>}
      </span>
    </button>
  );
}
