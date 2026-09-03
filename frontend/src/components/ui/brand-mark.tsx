import Image from "next/image";

interface BrandMarkProps {
  priority?: boolean;
}

export function BrandMark({ priority = false }: BrandMarkProps) {
  return (
    <span className="brand-mark" aria-hidden="true">
      <Image
        alt=""
        height={52}
        priority={priority}
        src="/images/brand/cafe-salud-logo.png"
        width={52}
      />
    </span>
  );
}
