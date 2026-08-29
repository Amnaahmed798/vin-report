import type { Metadata } from "next";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Terms of Service — Car Inspection Pro",
  description: "Terms of service for the free Car Inspection Pro vehicle history report.",
};

export default function TermsPage() {
  return (
    <LegalPage title="Terms of Service" updated="August 11, 2026">
      <h2 className="text-lg font-semibold text-slate-900">1. Use of the Service</h2>
      <p>
        Car Inspection Pro provides free vehicle history information compiled from public
        U.S. government data sources. By using this service, you agree to use it
        for informational purposes only and not to resell, redistribute, or
        republish the data in a way that misrepresents its source.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">2. No Vehicle Purchase Decisions</h2>
      <p>
        Information provided by Car Inspection Pro must not be relied upon as the sole
        basis for purchasing, selling, or appraising any vehicle. Always verify
        the physical condition and history of a vehicle through independent
        inspections and title records before any transaction.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">3. Acceptable Use</h2>
      <p>
        You agree not to attempt to disrupt the service, bypass rate limits,
        scrape the site at high volume, or use automated tools in a way that
        impairs the experience of other users.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">4. Availability</h2>
      <p>
        The service is provided &quot;as is&quot; and may be modified, suspended,
        or discontinued at any time without notice. We are not liable for any
        interruption, error, or omission in the data provided.
      </p>

      <h2 className="text-lg font-semibold text-slate-900">5. Changes</h2>
      <p>
        We may update these Terms from time to time. Continued use of the
        service after changes are posted constitutes acceptance of the revised
        Terms.
      </p>
    </LegalPage>
  );
}
