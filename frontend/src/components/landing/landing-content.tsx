import { DiseaseShowcase } from "@/components/landing/disease-showcase";
import { HowItWorks } from "@/components/landing/how-it-works";

export function LandingContent() {
  return (
    <section className="shell content-panel">
      <HowItWorks />
      <DiseaseShowcase />
    </section>
  );
}

