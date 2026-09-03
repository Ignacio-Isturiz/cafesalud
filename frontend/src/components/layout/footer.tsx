import { Mail, MapPin, Sprout } from "lucide-react";

import { BrandMark } from "@/components/ui/brand-mark";

export function Footer() {
  return (
    <footer className="footer" id="contacto">
      <div className="shell footer-inner">
        <div className="footer-brand"><BrandMark /><div><strong>CaféSalud</strong><p>Orientación clara para cuidar mejor tu cafetal.</p></div></div>
        <div className="footer-details"><span><MapPin size={16} /> Colombia</span><span><Mail size={16} /> Proyecto académico</span><span><Sprout size={16} /> Agricultura responsable</span></div>
      </div>
    </footer>
  );
}
