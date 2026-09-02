import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { Footer } from "@/components/layout/footer";
import { Header } from "@/components/layout/header";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });

export const metadata: Metadata = {
  title: "CaféSalud | Sistema experto para plantas de café",
  description: "Orientación diagnóstica preliminar para enfermedades en plantas de café.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body className={inter.variable}><Header /><main>{children}</main><Footer /></body></html>;
}

