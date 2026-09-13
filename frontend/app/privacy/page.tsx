import type { Metadata } from "next";
import LegalPage, { type LegalSection } from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Privacy Policy | Car Inspection Pro",
  description:
    "Learn how Car Inspection Pro collects, uses, protects, and handles information when you use our VIN and vehicle history reporting services.",
};

const SECTIONS: LegalSection[] = [
  { id: "introduction", label: "Introduction" },
  { id: "information-we-collect", label: "Information We Collect" },
  { id: "how-we-use", label: "How We Use Information" },
  { id: "vin-vehicle-data", label: "VIN and Vehicle Data" },
  { id: "payment-information", label: "Payment Information" },
  { id: "no-cookies", label: "No Cookies or Tracking" },
  { id: "third-party-services", label: "Third-Party Services" },
  { id: "data-sharing", label: "Data Sharing and Disclosure" },
  { id: "data-retention", label: "Data Retention" },
  { id: "data-security", label: "Data Security" },
  { id: "your-rights", label: "Your Privacy Rights" },
  { id: "children-privacy", label: "Children's Privacy" },
  { id: "international-users", label: "International Users" },
  { id: "changes-privacy", label: "Changes to This Policy" },
  { id: "contact-us", label: "Contact Us" },
];

export default function PrivacyPage() {
  return (
    <LegalPage
      title="Privacy Policy"
      updated="September 10, 2026"
      intro="This Privacy Policy explains how Car Inspection Pro collects, uses, stores, protects, and shares information when you visit our website and use our vehicle history reporting services."
      sections={SECTIONS}
    >
      {/* ===== 1 ===== */}
      <h2 id="introduction" className="text-xl font-bold text-slate-900">
        1. Introduction
      </h2>
      <p>
        Car Inspection Pro provides a vehicle history information service. Users
        can enter a Vehicle Identification Number (VIN) to obtain vehicle
        information and vehicle history reports compiled from publicly available
        U.S. government and authorized third-party data sources.
      </p>
      <p>
        This Privacy Policy applies to visitors, users, and customers of the Car
        Inspection Pro website. It describes the types of information we may
        collect, how we use that information, the circumstances under which it may
        be shared, and the choices available to you.
      </p>
      <p>
        By accessing or using the Car Inspection Pro website, you acknowledge that
        you have read and understood this Privacy Policy. If you do not agree with
        any part of this policy, please do not use the website or the services we
        provide.
      </p>

      {/* ===== 2 ===== */}
      <h2 id="information-we-collect" className="text-xl font-bold text-slate-900">
        2. Information We Collect
      </h2>

      <h3 className="text-base font-semibold text-slate-800">
        A. Information You Provide
      </h3>
      <p>
        The primary information you provide when using Car Inspection Pro is a
        Vehicle Identification Number (VIN) entered into the website to perform a
        lookup or request a report.
      </p>
      <p>
        We do not require you to create an account or provide your name, email
        address, or contact information to use the free VIN lookup feature. We do
        not currently collect email addresses or contact information through the
        website.
      </p>
      <p>
        If you purchase a vehicle history report, payment-related information is
        collected and processed by QuickBooks Payments, our payment processor.
        We do not collect or store your payment card number or other sensitive
        payment credentials on our servers.
      </p>

      <h3 className="text-base font-semibold text-slate-800">
        B. Automatically Collected Information
      </h3>
      <p>
        When you visit the Car Inspection Pro website, certain technical
        information may be collected automatically to operate the service
        securely and reliably. This may include:
      </p>
      <ul>
        <li>Your IP address, used to enforce rate limits and prevent abuse.</li>
        <li>Browser type and version.</li>
        <li>Device type and operating system.</li>
        <li>Pages visited and the date and time of access.</li>
        <li>Referring URLs that led you to the website.</li>
        <li>Basic diagnostic and error information.</li>
      </ul>
      <p>
        We do not use cookies or similar tracking technologies. See Section 6.
      </p>
      <p>
        This technical information is used for security, abuse prevention,
        troubleshooting, and improving the website. It is not used to build
        advertising profiles.
      </p>

      <h3 className="text-base font-semibold text-slate-800">
        C. Vehicle Information
      </h3>
      <p>
        The VIN you enter is used to generate vehicle information and reports.
        VIN-related information may be processed by our backend systems and
        transmitted to third-party data and API providers where necessary to
        retrieve the vehicle data that makes up your report. See Section 4 for
        more information about VIN and vehicle data handling.
      </p>

      {/* ===== 3 ===== */}
      <h2 id="how-we-use" className="text-xl font-bold text-slate-900">
        3. How We Use Information
      </h2>
      <p>We use the information described above for the following purposes:</p>
      <ul>
        <li>Processing VIN search requests.</li>
        <li>Generating and delivering vehicle history reports.</li>
        <li>Providing you with reports you have purchased.</li>
        <li>Processing payments through our payment provider.</li>
        <li>Preventing fraud, abuse, and unauthorized access.</li>
        <li>Maintaining the security and integrity of the website.</li>
        <li>Improving website functionality and user experience.</li>
        <li>Troubleshooting technical problems.</li>
        <li>Meeting legal and regulatory obligations where applicable.</li>
        <li>Communicating service-related information when necessary.</li>
      </ul>
      <p>
        We do not sell, rent, or trade your personal information to third parties
        for marketing purposes.
      </p>

      {/* ===== 4 ===== */}
      <h2 id="vin-vehicle-data" className="text-xl font-bold text-slate-900">
        4. VIN and Vehicle Data
      </h2>
      <p>
        A Vehicle Identification Number (VIN) is required to use our service
        because it is the standard identifier used to retrieve vehicle
        information. Entering a VIN allows our systems to decode the VIN and
        compile information about the vehicle from available data sources.
      </p>
      <p>
        To generate a report, the VIN and resulting vehicle information may be
        transmitted to third-party data and API providers. This transmission is
        necessary to retrieve the underlying data and is performed automatically
        by our backend systems.
      </p>
      <p>
        Vehicle data displayed in reports may come from government, public,
        commercial, or other third-party data sources, depending on the type of
        report requested. This includes data from the National Highway Traffic
        Safety Administration (NHTSA), the U.S. Department of Energy, and
        authorized NMVTIS data providers.
      </p>
      <p>
        We do not claim ownership of third-party vehicle data. All vehicle data
        remains subject to the rights of its respective sources and providers.
      </p>

      {/* ===== 5 ===== */}
      <h2 id="payment-information" className="text-xl font-bold text-slate-900">
        5. Payment Information
      </h2>
      <p>
        When you purchase a vehicle history report, payment processing is handled
        by QuickBooks Payments, our third-party payment provider.
      </p>
      <p>
        Depending on where you buy, payment information is collected either
        directly by QuickBooks on a secure hosted checkout page or in your
        browser by the Intuit Payments JavaScript SDK (which sends a secure,
        one-time token to QuickBooks). In either case, we do not collect, store,
        or transmit your complete payment card number, expiration date, or CVV
        on our servers.
      </p>
      <p>
        After a completed purchase, we may retain a minimal record of the
        transaction (such as an order identifier, plan type, amount, and date) for
        accounting, reporting, and customer-support purposes. This record does not
        include your payment card details.
      </p>

      {/* ===== 6 ===== */}
      <h2 id="no-cookies" className="text-xl font-bold text-slate-900">
        6. No Cookies or Tracking Technologies
      </h2>
      <p>
        Car Inspection Pro does not use cookies, browser storage, or similar
        tracking technologies on our website.
      </p>

      <h3 className="text-base font-semibold text-slate-800">
        No Cookies
      </h3>
      <p>
        We do not place or read cookies on your device, and we do not use
        advertising trackers, analytics cookies, or cross-site tracking of any
        kind. Our website functions without requiring cookies or local storage.
      </p>

      <h3 className="text-base font-semibold text-slate-800">
        Server Logs Are Not Tracking
      </h3>
      <p>
        When you visit the website, our web server may automatically record
        standard technical information about requests, as described in Section
        2B, such as your IP address, browser type, and pages visited. This is
        server-side logging, not a cookie. It is used for security, abuse
        prevention, and troubleshooting, and is not used to build advertising
        profiles.
      </p>

      <h3 className="text-base font-semibold text-slate-800">
        Changes
      </h3>
      <p>
        If we ever introduce cookies or other tracking technologies in the
        future, we will update this policy to describe them.
      </p>

      {/* ===== 7 ===== */}
      <h2 id="third-party-services" className="text-xl font-bold text-slate-900">
        7. Third-Party Services
      </h2>
      <p>
        Car Inspection Pro relies on a number of third-party services to operate.
        These services have their own privacy policies and terms, which govern how
        they handle information they receive from us or directly from you:
      </p>
      <ul>
        <li>
          <strong>QuickBooks Payments:</strong> Processes payments for purchased
          reports. It collects payment information directly from you on its secure
          checkout page.
        </li>
        <li>
          <strong>NHTSA vPIC and related APIs:</strong> Provide VIN decoding and
          vehicle specification data. These are public U.S. government services.
        </li>
        <li>
          <strong>NHTSA data services:</strong> Provide recall, complaint, safety
          rating, technical service bulletin, and investigation data.
        </li>
        <li>
          <strong>U.S. Department of Energy:</strong> Provides fuel economy data.
        </li>
        <li>
          <strong>NMVTIS data providers:</strong> May provide additional vehicle
          history data for certain types of reports.
        </li>
        <li>
          <strong>Hosting and infrastructure providers:</strong> Host the website
          and backend services.
        </li>
      </ul>
      <p>
        We encourage you to review the privacy policies of these third parties,
        as their practices are outside of our control.
      </p>

      {/* ===== 8 ===== */}
      <h2 id="data-sharing" className="text-xl font-bold text-slate-900">
        8. Data Sharing and Disclosure
      </h2>
      <p>
        Information may be shared with the following categories of recipients in
        the circumstances described below:
      </p>
      <ul>
        <li>
          <strong>Service and infrastructure providers:</strong> Providers that
          host the website, operate the backend, and help deliver the service.
        </li>
        <li>
          <strong>Vehicle data providers:</strong> Government and third-party APIs
          that supply vehicle data used to generate reports.
        </li>
        <li>
          <strong>Payment processors:</strong> QuickBooks Payments, which
          processes payment transactions.
        </li>
        <li>
          <strong>Security and fraud prevention:</strong> Where necessary to
          protect the security of the service and its users.
        </li>
        <li>
          <strong>Legal authorities:</strong> Where disclosure is required by law
          or in response to a valid legal request.
        </li>
        <li>
          <strong>Business transfers:</strong> In the event of a merger,
          acquisition, or sale of assets, information may be transferred as part
          of the transaction.
        </li>
      </ul>
      <p>
        We do not sell, rent, or trade your personal information. Any sharing is
        limited to the purposes described in this policy.
      </p>

      {/* ===== 9 ===== */}
      <h2 id="data-retention" className="text-xl font-bold text-slate-900">
        9. Data Retention
      </h2>
      <p>
        We retain information only for as long as reasonably necessary to fulfill
        the purposes described in this Privacy Policy, including to comply with
        legal obligations, resolve disputes, maintain security, and pursue
        legitimate business purposes.
      </p>
      <p>
        The specific retention period for any information depends on the nature of
        the information and the purpose for which it was collected. For example,
        transaction records may be retained for accounting and support purposes,
        while temporary technical logs may be retained for a shorter period and
        then deleted.
      </p>
      <p>
        When information is no longer needed, we take reasonable steps to delete it
        or to de-identify it.
      </p>

      {/* ===== 10 ===== */}
      <h2 id="data-security" className="text-xl font-bold text-slate-900">
        10. Data Security
      </h2>
      <p>
        We take reasonable measures to help protect information from unauthorized
        access, use, alteration, and disclosure. These measures include:
      </p>
      <ul>
        <li>Transport Layer Security (HTTPS/TLS) encryption for data in transit.</li>
        <li>Access controls on backend systems and data sources.</li>
        <li>Server security controls, including firewalls and monitoring.</li>
        <li>Regular maintenance and security updates.</li>
      </ul>
      <p>
        No method of electronic transmission or storage is completely secure, and
        we cannot guarantee absolute security. The transmission of information to
        and from the website is at your own risk.
      </p>

      {/* ===== 11 ===== */}
      <h2 id="your-rights" className="text-xl font-bold text-slate-900">
        11. Your Privacy Rights
      </h2>
      <p>
        Depending on your jurisdiction, you may have certain rights regarding the
        information we hold about you. These may include the right to:
      </p>
      <ul>
        <li>
          <strong>Access</strong> information we hold about you.
        </li>
        <li>
          <strong>Correct</strong> inaccurate information.
        </li>
        <li>
          <strong>Delete</strong> information we no longer need.
        </li>
        <li>
          <strong>Port</strong> information in a structured, machine-readable
          format where applicable.
        </li>
        <li>
          <strong>Restrict or object</strong> to certain processing.
        </li>
        <li>
          <strong>Withdraw consent</strong> where processing is based on consent.
        </li>
      </ul>
      <p>
        Because Car Inspection Pro does not maintain user accounts and collects
        only a limited amount of information, most of these rights will have
        limited practical application. If you wish to exercise any rights you may
        have, please contact us using the details in Section 15.
      </p>

      {/* ===== 12 ===== */}
      <h2 id="children-privacy" className="text-xl font-bold text-slate-900">
        12. Children&apos;s Privacy
      </h2>
      <p>
        Car Inspection Pro is not directed toward children, and our services are
        intended for adults. We do not knowingly collect personal information
        from children.
      </p>
      <p>
        If you believe a child has provided information through our website,
        please contact us so that any such information can be deleted.
      </p>

      {/* ===== 13 ===== */}
      <h2 id="international-users" className="text-xl font-bold text-slate-900">
        13. International Users
      </h2>
      <p>
        Car Inspection Pro operates from within the United States. Depending on
        our hosting and service providers, information may be processed in the
        United States or in other countries in which our providers operate.
      </p>
      <p>
        By using the website, users located outside these countries acknowledge
        that their information may be processed in locations other than their
        country of residence, where data protection laws may differ.
      </p>

      {/* ===== 14 ===== */}
      <h2 id="changes-privacy" className="text-xl font-bold text-slate-900">
        14. Changes to This Privacy Policy
      </h2>
      <p>
        We may update this Privacy Policy from time to time to reflect changes in
        our practices, the services we offer, or legal requirements. When we make
        material changes, we will update the &quot;Last Updated&quot; date at the
        top of this page.
      </p>
      <p>
        We encourage you to review this Privacy Policy periodically. Your
        continued use of the website after any changes constitutes acceptance of
        the updated policy.
      </p>

      {/* ===== 15 ===== */}
      <h2 id="contact-us" className="text-xl font-bold text-slate-900">
        15. Contact Us
      </h2>
      <p>
        If you have questions or concerns about this Privacy Policy or how your
        information is handled, you may reach us through the contact channel
        available on the Car Inspection Pro website.
      </p>
    </LegalPage>
  );
}