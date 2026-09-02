import { Mail, MapPin, Sprout } from "lucide-react";

export function Footer() {
  return (
    <footer className="footer" id="contacto">
      <div className="shell footer-inner">
        <div><strong>CaféSalud</strong><p>Orientación clara para cuidar mejor tu cafetal.</p></div>
        <div className="footer-details"><span><MapPin size={16} /> Colombia</span><span><Mail size={16} /> Proyecto académico</span><span><Sprout size={16} /> Agricultura responsable</span></div>
      </div>
    </footer>
  );
}

