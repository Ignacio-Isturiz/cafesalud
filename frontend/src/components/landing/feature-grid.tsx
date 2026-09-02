import { BrainCircuit, ChartNoAxesCombined, Crosshair, Sprout } from "lucide-react";

const features = [
  { icon: BrainCircuit, title: "Conocimiento experto", text: "Sistema basado en reglas y conocimiento relacionado con enfermedades del café." },
  { icon: Crosshair, title: "Diagnóstico preliminar", text: "Obtén una hipótesis diagnóstica con nivel de coincidencia y explicación." },
  { icon: Sprout, title: "Recomendaciones útiles", text: "Recibe sugerencias prácticas para manejar la enfermedad y mejorar tu cultivo." },
  { icon: ChartNoAxesCombined, title: "Mejora continua", text: "Arquitectura preparada para incorporar nuevas enfermedades y conocimiento." },
];

export function FeatureGrid() {
  return (
    <section className="shell feature-grid" id="caracteristicas" aria-label="Características">
      {features.map(({ icon: Icon, title, text }) => (
        <article className="feature-card" key={title}>
          <span className="feature-icon"><Icon /></span>
          <div><h2>{title}</h2><p>{text}</p></div>
        </article>
      ))}
    </section>
  );
}

