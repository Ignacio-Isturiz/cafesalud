import { FeatureGrid } from "@/components/landing/feature-grid";
import { Hero } from "@/components/landing/hero";
import { InfoBand } from "@/components/landing/info-band";
import { LandingContent } from "@/components/landing/landing-content";

export default function Home() {
  return <><Hero /><FeatureGrid /><LandingContent /><div className="shell"><InfoBand /></div></>;
}

