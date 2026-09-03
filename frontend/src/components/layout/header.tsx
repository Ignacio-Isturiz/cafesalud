import { Menu, Sprout } from "lucide-react";
import Link from "next/link";

import { navigation } from "@/constants/landing";
import { BrandMark } from "@/components/ui/brand-mark";

export function Header() {
  return (
    <header className="site-header">
      <div className="shell header-inner">
        <Link href="/" className="brand" aria-label="CaféSalud, inicio">
          <BrandMark priority />
          <span className="brand-copy">
            <strong>Café<span>Salud</span></strong>
            <small>Sistema Experto</small>
          </span>
        </Link>

        <nav className="desktop-nav" aria-label="Navegación principal">
          {navigation.map((item, index) => (
            <Link className={index === 0 ? "active" : ""} href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>

        <Link className="primary-button header-action" href="/diagnostico">
          <Sprout size={17} />
          Probar diagnóstico
        </Link>
        <button className="menu-button" aria-label="Abrir menú" type="button"><Menu /></button>
      </div>
    </header>
  );
}
