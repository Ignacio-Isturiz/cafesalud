import Image from "next/image";

import { diseases } from "@/constants/landing";

export function DiseaseShowcase() {
  return (
    <section className="disease-showcase" id="enfermedades">
      <div className="section-heading"><h2>Enfermedades que puedes identificar</h2><span /></div>
      <div className="disease-grid">
        {diseases.map((disease) => (
          <article className="disease-card" key={disease.id}>
            <div className="disease-image"><Image src={disease.image} alt={`Hoja de café con ${disease.name}`} fill sizes="(max-width: 700px) 100vw, 20vw" /></div>
            <div><h3>{disease.name}</h3><p>{disease.description}</p></div>
          </article>
        ))}
      </div>
    </section>
  );
}

