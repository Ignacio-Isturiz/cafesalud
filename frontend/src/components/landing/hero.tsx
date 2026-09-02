import { MessageCircleMore, Play, ShieldCheck, Sprout } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

import { images } from "@/constants/images";

const trustItems = [
  { id: "knowledge", icon: ShieldCheck, text: <>Basado en<br />conocimiento experto</> },
  { id: "answers", icon: MessageCircleMore, text: <>Respuestas claras<br />y explicadas</> },
  { id: "recommendations", icon: Sprout, text: <>Recomendaciones<br />prácticas</> },
];

export function Hero() {
  return (
    <section className="hero" id="inicio">
      <Image className="hero-image" src={images.hero} alt="Rama de café con frutos maduros en un cafetal de montaña" fill priority sizes="(max-width: 800px) 100vw, 58vw" />
      <div className="hero-wash" aria-hidden="true" />
      <div className="shell hero-inner">
        <div className="hero-copy">
          <p className="eyebrow">Tecnología al servicio de tu cultivo</p>
          <h1>Diagnóstico inteligente<br />para <span>plantas de café</span></h1>
          <p className="hero-lede">Nuestro sistema experto te ayuda a identificar posibles enfermedades en tu cultivo a partir de los síntomas que observas y las condiciones del entorno.</p>
          <div className="hero-actions">
            <Link className="primary-button" href="/diagnostico"><Sprout size={18} /> Comenzar diagnóstico</Link>
            <a className="secondary-button" href="#como-funciona"><Play size={18} /> Ver cómo funciona</a>
          </div>
          <div className="trust-row">
            {trustItems.map(({ id, icon: Icon, text }) => <div className="trust-item" key={id}><Icon /><span>{text}</span></div>)}
          </div>
        </div>
      </div>
    </section>
  );
}
