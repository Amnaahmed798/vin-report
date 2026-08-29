import type { Metadata } from "next";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Privacy Policy — Car Inspection Pro",
  description: "Privacy policy for the free Car Inspection Pro vehicle history report.",
};

export default function PrivacyPage() {
  return (
    <LegalPage title="Privacy Policy" updated="August 11, 2026">
      <h2 className="text-lg font-semibold text-slate-900">1. What We Collect</h2>
      <p>
        Car Inspection Pro does not require an account and does not collect personally
        identifiable information. When you look up a VIN, we may collect basic
        technical data such as your IP address and the pages you visit in order
        to operate the service, enforce rate limits, and prevent abuse.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">2. How We Use It</h2>
      <p>
        Technical data is used solely for operating and securing the service. We
        do not sell, rent, or share this data with third parties for marketing
        purposes.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">3. Third-Party Data Sources</h2>
      <p>
        The vehicle information shown in reports comes from public U.S.
        government sources, including the National Highway Traffic Safety
        Administration (NHTSA) and the U.S. Department of Energy. When you request
        a report, those agencies&apos; public APIs are queried on your behalf.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">4. Cookies</h2>
      <p>
        This site does not use advertising or tracking cookies.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">5. Contact</h2>
      <p>
        If you have questions about this policy, please contact us using the
        details provided on the site.
      </p>
    </LegalPage>
  );
}
