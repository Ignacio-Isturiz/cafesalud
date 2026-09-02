import { Sprout } from "lucide-react";

export function RecommendationCard({ text, index }: { text: string; index: number }) {
  return (
    <li className="recommendation-card">
      <span><Sprout /></span>
      <div><small>Recomendación {index + 1}</small><p>{text}</p></div>
    </li>
  );
}
