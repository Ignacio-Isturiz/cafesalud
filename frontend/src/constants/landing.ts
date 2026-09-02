import { images } from "@/constants/images";

export const navigation = [
  { label: "Inicio", href: "#inicio" },
  { label: "Características", href: "#caracteristicas" },
  { label: "Cómo funciona", href: "#como-funciona" },
  { label: "Enfermedades", href: "#enfermedades" },
  { label: "Sobre el proyecto", href: "#sobre-proyecto" },
  { label: "Contacto", href: "#contacto" },
] as const;

export const diseases = [
  {
    id: "coffee_rust",
    name: "Roya del café",
    description: "Manchas amarillas y polvo anaranjado en el envés de las hojas.",
    image: images.diseases.rust,
  },
  {
    id: "iron_spot",
    name: "Mancha de hierro",
    description: "Manchas pequeñas de color café con centro grisáceo y borde amarillo.",
    image: images.diseases.ironSpot,
  },
  {
    id: "american_leaf_spot",
    name: "Ojo de gallo (Gotera)",
    description: "Manchas circulares con centro claro y borde oscuro, causa defoliación.",
    image: images.diseases.americanLeafSpot,
  },
] as const;

