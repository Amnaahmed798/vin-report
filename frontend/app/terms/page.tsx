import type { Metadata } from "next";
import LegalPage, { type LegalSection } from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Terms & Conditions | Car Inspection Pro",
  description:
    "Review the terms governing your use of Car Inspection Pro's VIN decoding and vehicle history reporting services.",
};

const SECTIONS: LegalSection[] = [
  { id: "introduction-acceptance", label: "Introduction and Acceptance" },
  { id: "description-services", label: "Description of Services" },
  { id: "eligibility", label: "Eligibility" },
  { id: "vin-submission", label: "VIN Submission" },
  { id: "vehicle-data-reports", label: "Vehicle Data and Reports" },
  { id: "no-guarantee", label: "No Guarantee of Complete History" },
  { id: "user-responsibilities", label: "User Responsibilities" },
  { id: "purchases-payments", label: "Purchases and Payments" },
  { id: "refund-policy", label: "Refund Policy" },
  { id: "intellectual-property", label: "Intellectual Property" },
  { id: "third-party-data", label: "Third-Party Data and Services" },
  { id: "prohibited-uses", label: "Prohibited Uses" },
  { id: "disclaimer-warranties", label: "Disclaimer of Warranties" },
  { id: "limitation-liability", label: "Limitation of Liability" },
  { id: "indemnification", label: "Indemnification" },
  { id: "termination", label: "Termination / Suspension" },
  { id: "changes-terms", label: "Changes to Terms" },
  { id: "contact", label: "Contact" },
];

export default function TermsPage() {
  return (
    <LegalPage
      title="Terms & Conditions"
      updated="September 10, 2026"
      intro="These Terms & Conditions govern your use of Car Inspection Pro's VIN decoding and vehicle history reporting services. Please read them carefully before using our website."
      sections={SECTIONS}
    >
      {/* ===== 1 ===== */}
      <h2 id="introduction-acceptance" className="text-xl font-bold text-slate-900">
        1. Introduction and Acceptance
      </h2>
      <p>
        Welcome to Car Inspection Pro. These Terms &amp; Conditions
        (&quot;Terms&quot;) set out the terms under which you may use the Car
        Inspection Pro website and the services it provides. Our website offers
        VIN (Vehicle Identification Number) decoding and vehicle history
        reporting services to help you obtain information about a vehicle.
      </p>
      <p>
        By accessing or using the Car Inspection Pro website, you agree to be
        bound by these Terms, together with our Privacy Policy and Disclaimer,
        which are incorporated by reference. If you do not agree to these Terms,
        you should stop using the website immediately.
      </p>

      {/* ===== 2 ===== */}
      <h2 id="description-services" className="text-xl font-bold text-slate-900">
        2. Description of Services
      </h2>
      <p>
        Car Inspection Pro provides the following services:
      </p>
      <ul>
        <li>
          <strong>VIN Decoding:</strong> The ability to enter a VIN and receive
          basic vehicle information, such as make, model, year, and
          specifications, decoded from public databases.
        </li>
        <li>
          <strong>Free Vehicle Information:</strong> Display of publicly available
          data about a vehicle, including recalls, complaints, safety ratings,
          fuel economy, technical service bulletins, and investigations.
        </li>
        <li>
          <strong>Paid Reports:</strong> Generation and delivery of a downloadable
          vehicle history report (PDF) that includes additional data sourced from
          authorized data providers, where available.
        </li>
      </ul>
      <p>
        We may add, modify, or discontinue any aspect of the services at any time.
      </p>

      {/* ===== 3 ===== */}
      <h2 id="eligibility" className="text-xl font-bold text-slate-900">
        3. Eligibility
      </h2>
      <p>
        By using Car Inspection Pro, you represent that you are at least 18 years
        of age and have the legal capacity to enter into these Terms. The services
        are provided for personal, non-commercial use unless otherwise agreed.
      </p>
      <p>
        You are responsible for ensuring that your use of the website complies
        with all applicable laws and regulations in your jurisdiction.
      </p>

      {/* ===== 4 ===== */}
      <h2 id="vin-submission" className="text-xl font-bold text-slate-900">
        4. VIN Submission
      </h2>
      <p>
        When using the VIN lookup or report services, you are responsible for
        entering a correct and complete Vehicle Identification Number.
      </p>
      <ul>
        <li>
          Entering an incorrect, incomplete, or mistyped VIN may produce incorrect
          or irrelevant results.
        </li>
        <li>
          We do not guarantee that every VIN will return complete information. Some
          vehicle types, older models, or vehicles not sold in the United States
          may have limited or no data available.
        </li>
        <li>
          You are responsible for verifying that the VIN you entered matches the
          vehicle you intend to research.
        </li>
      </ul>

      {/* ===== 5 ===== */}
      <h2 id="vehicle-data-reports" className="text-xl font-bold text-slate-900">
        5. Vehicle Data and Reports
      </h2>
      <p>
        Vehicle information and reports are compiled from the data sources
        available to us at the time the report is generated. This data may
        contain:
      </p>
      <ul>
        <li>Missing information for some vehicles or events.</li>
        <li>Delays between when an event occurs and when it appears in a database.</li>
        <li>Errors or inconsistencies in the underlying source data.</li>
        <li>
          Historical information that is not complete or that may be outdated.
        </li>
      </ul>
      <p>
        The report should be treated as an informational tool that helps you
        understand a vehicle&apos;s history, not as an absolute guarantee of that
        vehicle&apos;s condition or history.
      </p>

      {/* ===== 6 ===== */}
      <h2 id="no-guarantee" className="text-xl font-bold text-slate-900">
        6. No Guarantee of Complete Vehicle History
      </h2>
      <p>
        A vehicle history report can never include every event in a vehicle&apos;s
        history. Not every accident, repair, title transfer, odometer reading,
        theft, service visit, or other event is reported to the databases from
        which our reports are compiled.
      </p>
      <p>
        Many vehicle events are never recorded at all. For example, a vehicle may
        have been involved in an accident that was repaired privately and never
        reported to an insurance company, a state agency, or any database we use.
        Similarly, routine maintenance may be performed by an independent mechanic
        and never appear in any record accessible to us.
      </p>
      <p>
        <strong>
          The absence of an event in a report does not prove that the event never
          occurred.
        </strong>
        Conversely, the presence of an event in a report reflects only what was
        reported to the underlying source database.
      </p>

      {/* ===== 7 ===== */}
      <h2 id="user-responsibilities" className="text-xl font-bold text-slate-900">
        7. User Responsibilities
      </h2>
      <p>You agree, when using the website, to:</p>
      <ul>
        <li>Provide accurate information, including correct VINs.</li>
        <li>Use reports and information lawfully and for legitimate purposes.</li>
        <li>Not abuse, disrupt, or interfere with the website or its services.</li>
        <li>Not attempt to gain unauthorized access to any part of the website.</li>
        <li>Not interfere with the operation of the website or other users.</li>
        <li>Not scrape, harvest, or otherwise misuse the data or services.</li>
        <li>Not use the service for any unlawful purpose.</li>
      </ul>
      <p>
        You are solely responsible for how you use the information obtained
        through the website.
      </p>

      {/* ===== 8 ===== */}
      <h2 id="purchases-payments" className="text-xl font-bold text-slate-900">
        8. Purchases and Payments
      </h2>
      <p>
        Car Inspection Pro offers paid vehicle history report plans. When you
        purchase a plan, you agree to pay the price displayed at the time of
        purchase.
      </p>
      <ul>
        <li>All prices are shown in U.S. dollars (USD).</li>
        <li>
          Payment is processed by QuickBooks Payments, our third-party payment
          provider. Depending on where you buy, payment information is collected
          either on a secure hosted checkout page or in your browser by the Intuit
          Payments JavaScript SDK and tokenized before transmission. We do not
          collect or store your complete payment card number on our servers.
        </li>
        <li>
          Applicable sales tax may be charged where required by law.
        </li>
        <li>
          Payment is considered complete when the payment processor confirms the
          transaction.
        </li>
        <li>
          Following a successful purchase, vehicle history reports are generated
          and made available for download through the website, up to the number
          of reports included in your plan as shown at the time of purchase.
        </li>
      </ul>

      {/* ===== 9 ===== */}
      <h2 id="refund-policy" className="text-xl font-bold text-slate-900">
        9. Refund Policy
      </h2>
      <p>
        If a report cannot be generated due to a technical error on our side, or
        if you encounter a problem accessing a report you purchased, we will work
        with you to resolve the issue. Depending on the circumstances, this may
        include regenerating the report or processing a refund.
      </p>
      <p>
        Because vehicle history reports are delivered digitally and the underlying
        data is purchased from third-party providers at the time of generation,
        refunds for successfully delivered reports are generally not available.
      </p>
      <p>
        Refund requests should be submitted through the contact channel available
        on the website and will be considered on a case-by-case basis.
      </p>

      {/* ===== 10 ===== */}
      <h2 id="intellectual-property" className="text-xl font-bold text-slate-900">
        10. Intellectual Property
      </h2>
      <p>
        The Car Inspection Pro website, including its design, branding, software,
        text, and original content, is the property of Car Inspection Pro and is
        protected by applicable intellectual property laws. You may not copy,
        reproduce, modify, distribute, or create derivative works from the website
        or its original content without our prior written consent.
      </p>
      <p>
        Vehicle data included in reports originates from third-party sources and
        remains subject to the rights of those respective providers. Your use of
        the report is limited to personal, non-commercial purposes.
      </p>

      {/* ===== 11 ===== */}
      <h2 id="third-party-data" className="text-xl font-bold text-slate-900">
        11. Third-Party Data and Services
      </h2>
      <p>
        Car Inspection Pro relies on third-party data sources and APIs to provide
        its services. These include public U.S. government databases (such as
        NHTSA and the U.S. Department of Energy) and authorized NMVTIS data
        providers.
      </p>
      <p>
        We cannot guarantee the availability, accuracy, completeness, or
        uninterrupted operation of these third-party services. Outages, changes,
        or data limitations affecting these providers may impact the reports we
        are able to generate.
      </p>

      {/* ===== 12 ===== */}
      <h2 id="prohibited-uses" className="text-xl font-bold text-slate-900">
        12. Prohibited Uses
      </h2>
      <p>You agree not to use the website or its services to:</p>
      <ul>
        <li>Resell, redistribute, or republish reports or their contents.</li>
        <li>
          Present Car Inspection Pro reports as being from another provider.
        </li>
        <li>Scrape, harvest, or systematically collect data or content.</li>
        <li>Automate VIN lookups beyond normal human usage.</li>
        <li>Attempt to bypass rate limits or security controls.</li>
        <li>Upload or transmit malicious code, including viruses.</li>
        <li>Engage in any activity that is unlawful, harmful, or fraudulent.</li>
      </ul>
      <p>
        We reserve the right to restrict or terminate access for conduct we
        consider, in our reasonable judgment, to violate these Terms.
      </p>

      {/* ===== 13 ===== */}
      <h2 id="disclaimer-warranties" className="text-xl font-bold text-slate-900">
        13. Disclaimer of Warranties
      </h2>
      <p>
        The website and the reports and information provided are made available on
        an &quot;as is&quot; and &quot;as available&quot; basis for informational
        purposes only.
      </p>
      <p>
        To the extent permitted by applicable law, we make no warranties,
        express or implied, including implied warranties of merchantability,
        fitness for a particular purpose, and non-infringement. In particular, we
        do not guarantee:
      </p>
      <ul>
        <li>The condition or mechanical state of any vehicle.</li>
        <li>The completeness of accident history records.</li>
        <li>The completeness of title status records.</li>
        <li>The completeness of odometer history records.</li>
        <li>The completeness of service history records.</li>
        <li>The future reliability or performance of any vehicle.</li>
        <li>Current or future market value of any vehicle.</li>
      </ul>
      <p>
        Your use of the website and reliance on any information is entirely at
        your own risk.
      </p>

      {/* ===== 14 ===== */}
      <h2 id="limitation-liability" className="text-xl font-bold text-slate-900">
        14. Limitation of Liability
      </h2>
      <p>
        To the fullest extent permitted by applicable law, Car Inspection Pro,
        its owners, employees, and affiliates shall not be liable for any
        indirect, incidental, special, consequential, or punitive damages, or any
        loss of profits, data, or opportunities, arising out of or in connection
        with your use of the website, the reports, or any information provided.
      </p>
      <p>
        This includes, but is not limited to, damages resulting from decisions
        made in reliance on information in a report, such as the purchase or sale
        of a vehicle.
      </p>
      <p>
        To the extent permitted by applicable law, our total aggregate liability
        for any claim arising from these Terms or your use of the services shall
        not exceed the amount you paid for the specific report that gave rise to
        the claim.
      </p>

      {/* ===== 15 ===== */}
      <h2 id="indemnification" className="text-xl font-bold text-slate-900">
        15. Indemnification
      </h2>
      <p>
        To the extent permitted by applicable law, you agree to indemnify, defend,
        and hold harmless Car Inspection Pro and its owners, employees, and
        affiliates from and against any claims, damages, liabilities, and expenses
        (including reasonable attorneys&apos; fees) arising out of or related to
        your misuse of the website, your violation of these Terms, or your
        violation of any applicable law.
      </p>

      {/* ===== 16 ===== */}
      <h2 id="termination" className="text-xl font-bold text-slate-900">
        16. Termination / Suspension
      </h2>
      <p>
        We may suspend or terminate your access to the website, in whole or in
        part, at any time and for any reason, including (but not limited to) if we
        reasonably believe you have:
      </p>
      <ul>
        <li>Engaged in abuse or attempted to disrupt the service.</li>
        <li>Committed fraud or attempted unauthorized transactions.</li>
        <li>Created a security threat to the website or its users.</li>
        <li>Violated these Terms.</li>
        <li>Used the website for illegal activity.</li>
      </ul>
      <p>
        Sections of these Terms that by their nature should survive termination,
        including the disclaimer of warranties, limitation of liability, and
        indemnification, will continue to apply.
      </p>

      {/* ===== 17 ===== */}
      <h2 id="changes-terms" className="text-xl font-bold text-slate-900">
        17. Changes to Terms
      </h2>
      <p>
        We may revise these Terms at any time by updating this page. When we make
        material changes, we will update the &quot;Last Updated&quot; date at the
        top of this page.
      </p>
      <p>
        Your continued use of the website after changes are posted constitutes
        acceptance of the revised Terms. If you do not agree with the revised
        Terms, you should stop using the website.
      </p>

      {/* ===== 18 ===== */}
      <h2 id="contact" className="text-xl font-bold text-slate-900">
        18. Contact
      </h2>
      <p>
        If you have any questions about these Terms &amp; Conditions, you may
        reach us through the contact channel available on the Car Inspection Pro
        website.
      </p>
    </LegalPage>
  );
}