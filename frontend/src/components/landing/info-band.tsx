import { Clock3, Leaf, ShieldCheck, Sprout } from "lucide-react";

const items = [
  { icon: Sprout, title: "Basado en evidencia", text: "Reglas y conocimiento de expertos en fitopatología." },
  { icon: ShieldCheck, title: "Fácil de usar", text: "Interfaz intuitiva diseñada para caficultores." },
  { icon: Clock3, title: "Ahorra tiempo", text: "Obtén orientación rápida desde cualquier lugar." },
  { icon: Leaf, title: "Cuidado responsable", text: "Promueve prácticas sostenibles y cultivos saludables." },
];

export function InfoBand() {
  return (
    <section className="info-band" id="sobre-proyecto">
      {items.map(({ icon: Icon, title, text }) => <article key={title}><Icon /><div><h3>{title}</h3><p>{text}</p></div></article>)}
      <article className="closing-note"><span className="soil"><Sprout /></span><div><h3>Tu cultivo en buenas manos</h3><p>CaféSalud te acompaña para que tomes decisiones informadas y protejas tu café.</p></div></article>
    </section>
  );
}

