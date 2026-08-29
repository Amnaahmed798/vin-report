import type { Metadata } from "next";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Disclaimer — Car Inspection Pro",
  description: "Legal disclaimer for the free Car Inspection Pro vehicle history report.",
};

export default function DisclaimerPage() {
  return (
    <LegalPage title="Disclaimer" updated="August 11, 2026">
      <h2 className="text-lg font-semibold text-slate-900">Not a CARFAX Report</h2>
      <p>
        Car Inspection Pro is an independent, free service. It is not affiliated with,
        endorsed by, or sponsored by CARFAX, AutoCheck, or any other commercial
        vehicle history provider. This report is not a CARFAX report and is not a
        substitute for one.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">Government Data Only</h2>
      <p>
        Reports include recalls, complaints, technical service bulletins,
        investigations, safety ratings, crash-test photos, and fuel economy data
        drawn from public U.S. government sources. We do not have access to
        private records such as title history, odometer readings, accident
        claims, insurance records, or previous owners.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">Accuracy</h2>
      <p>
        While we strive for accuracy, data from government sources may be
        incomplete, out of date, or subject to change. Vehicle identification
        details may be missing for some vehicles. We make no warranties,
        express or implied, regarding the completeness or accuracy of any
        information provided.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">Not Professional Advice</h2>
      <p>
        Nothing in this report constitutes legal, financial, or mechanical
        advice. You should obtain an independent inspection and title check
        before purchasing any vehicle.
      </p>
    </LegalPage>
  );
}
