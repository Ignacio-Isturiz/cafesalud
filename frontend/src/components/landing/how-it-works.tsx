import { ClipboardCheck, Leaf, Search, ShieldCheck } from "lucide-react";

const steps = [
  { icon: Leaf, title: "Responde preguntas", text: "Indica la parte afectada y responde sobre los síntomas que observas." },
  { icon: Search, title: "Análisis del sistema experto", text: "El motor analiza la información con su base de conocimiento." },
  { icon: ClipboardCheck, title: "Obtén resultados", text: "Recibe una posible enfermedad con nivel de coincidencia." },
  { icon: ShieldCheck, title: "Toma mejores decisiones", text: "Sigue recomendaciones para cuidar tu cultivo." },
];

export function HowItWorks() {
  return (
    <section className="how" id="como-funciona">
      <div className="section-heading"><h2>¿Cómo funciona?</h2><span /> <p>Un proceso simple en 4 pasos</p></div>
      <div className="steps">
        {steps.map(({ icon: Icon, title, text }, index) => (
          <article className="step" key={title}>
            <div className="step-visual"><b>{index + 1}</b><span><Icon /></span></div>
            <h3>{title}</h3><p>{text}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

