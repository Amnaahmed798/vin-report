import type { Metadata } from "next";
import LegalPage, { type LegalSection } from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Disclaimer | Car Inspection Pro",
  description:
    "Important information about vehicle history reports, third-party data, report accuracy, and the limitations of VIN reports.",
};

const SECTIONS: LegalSection[] = [
  { id: "general-information", label: "General Information" },
  { id: "no-guarantee-history", label: "No Guarantee of Complete History" },
  { id: "accuracy-data", label: "Accuracy of Data" },
  { id: "no-mechanical-inspection", label: "No Mechanical Inspection" },
  { id: "no-guarantee-condition", label: "No Guarantee of Vehicle Condition" },
  { id: "no-legal-advice", label: "No Legal or Financial Advice" },
  { id: "third-party-sources", label: "Third-Party Sources" },
  { id: "user-decision", label: "User Decision" },
  { id: "limitation-liability", label: "Limitation of Liability" },
  { id: "contact", label: "Contact" },
];

export default function DisclaimerPage() {
  return (
    <LegalPage
      title="Disclaimer"
      updated="September 10, 2026"
      intro="This Disclaimer outlines important information about Car Inspection Pro vehicle history reports, including the sources and limitations of the data we provide. Please read it carefully."
      sections={SECTIONS}
    >
      {/* ===== 1 ===== */}
      <h2 id="general-information" className="text-xl font-bold text-slate-900">
        1. General Information
      </h2>
      <p>
        Car Inspection Pro provides vehicle information and vehicle history
        reports for informational purposes. These reports are intended to help you
        understand more about a vehicle&apos;s history as reflected in available
        databases. They are not a certification of any vehicle&apos;s condition,
        value, or history.
      </p>
      <p>
        Car Inspection Pro is an independent service and is not affiliated with
        CARFAX, AutoCheck, or any other commercial vehicle history provider.
        Reports produced by Car Inspection Pro are not CARFAX or AutoCheck
        reports and should not be represented as such.
      </p>

      {/* ===== 2 ===== */}
      <h2 id="no-guarantee-history" className="text-xl font-bold text-slate-900">
        2. No Guarantee of Complete Vehicle History
      </h2>
      <p>
        A vehicle history report may not contain every event in a vehicle&apos;s
        history. Accidents, repairs, title transfers, odometer readings, thefts,
        and service visits are not always reported to the databases we use, and
        many events are never recorded anywhere.
      </p>
      <p>
        <strong>
          The absence of a record in a report does not mean the event never
          occurred.
        </strong>
        For example, a vehicle that does not show an accident in the report may
        still have been involved in an accident that was never reported. Reports
        should be used only as one source of information about a vehicle.
      </p>

      {/* ===== 3 ===== */}
      <h2 id="accuracy-data" className="text-xl font-bold text-slate-900">
        3. Accuracy of Data
      </h2>
      <p>
        Vehicle information is compiled from external and third-party sources,
        including public U.S. government databases and authorized data providers.
        We present this information as it is provided by those sources.
      </p>
      <p>
        Because the data originates from third parties, it may contain errors,
        delays, omissions, or outdated information. We do not independently verify
        every piece of data included in a report, and we make no representation
        that any report is complete, accurate, or current.
      </p>

      {/* ===== 4 ===== */}
      <h2 id="no-mechanical-inspection" className="text-xl font-bold text-slate-900">
        4. No Mechanical Inspection
      </h2>
      <p>
        <strong>A VIN report is not a physical or mechanical inspection of any
        vehicle.</strong>
      </p>
      <p>
        A vehicle history report is compiled from database records and cannot
        reveal the physical condition of a vehicle. A vehicle may have mechanical
        problems, structural damage, or other issues that are not recorded in any
        database.
      </p>
      <p>A vehicle history report does not replace:</p>
      <ul>
        <li>A professional mechanic&apos;s inspection.</li>
        <li>A test drive and hands-on evaluation of the vehicle.</li>
        <li>An independent vehicle inspection.</li>
        <li>A review of the vehicle&apos;s original documents.</li>
      </ul>

      {/* ===== 5 ===== */}
      <h2 id="no-guarantee-condition" className="text-xl font-bold text-slate-900">
        5. No Guarantee of Vehicle Condition
      </h2>
      <p>
        A vehicle history report cannot guarantee the condition of any vehicle,
        including its:
      </p>
      <ul>
        <li>Mechanical condition.</li>
        <li>Structural condition.</li>
        <li>Safety.</li>
        <li>Reliability.</li>
        <li>Current condition.</li>
        <li>Future performance.</li>
      </ul>
      <p>
        Only a physical inspection by a qualified professional, together with a
        review of the vehicle&apos;s documents, can assess the true condition of a
        vehicle.
      </p>

      {/* ===== 6 ===== */}
      <h2 id="no-legal-advice" className="text-xl font-bold text-slate-900">
        6. No Legal or Financial Advice
      </h2>
      <p>
        A vehicle history report is not legal, financial, insurance, or other
        professional advice. Nothing in a report should be relied upon as advice
        relating to the purchase, sale, valuation, financing, or insurance of any
        vehicle.
      </p>
      <p>
        You should consult qualified professionals where you need legal, financial,
        insurance, or mechanical guidance.
      </p>

      {/* ===== 7 ===== */}
      <h2 id="third-party-sources" className="text-xl font-bold text-slate-900">
        7. Third-Party Sources
      </h2>
      <p>
        Vehicle information may come from third-party, government, public, and
        commercial databases. These sources include NHTSA, the U.S. Department of
        Energy, and authorized NMVTIS data providers.
      </p>
      <p>
        The availability, accuracy, and completeness of these sources are outside
        of our control. Changes to, outages of, or limitations in these sources
        can affect the reports we are able to produce. We are not responsible for
        the content or accuracy of any third-party data.
      </p>

      {/* ===== 8 ===== */}
      <h2 id="user-decision" className="text-xl font-bold text-slate-900">
        8. User Decision
      </h2>
      <p>
        You, the user, are responsible for how you use the information in a
        report. Before purchasing or relying on any vehicle, you should
        independently verify important information, including:
      </p>
      <ul>
        <li>The vehicle&apos;s physical and mechanical condition.</li>
        <li>The accuracy of the VIN.</li>
        <li>The vehicle&apos;s title status with the relevant DMV.</li>
        <li>Any outstanding liens or financial obligations on the vehicle.</li>
        <li>Additional history from other sources.</li>
      </ul>
      <p>
        Do not make a vehicle purchase or other significant decision based solely
        on information in a Car Inspection Pro report.
      </p>

      {/* ===== 9 ===== */}
      <h2 id="limitation-liability" className="text-xl font-bold text-slate-900">
        9. Limitation of Liability
      </h2>
      <p>
        To the fullest extent permitted by applicable law, Car Inspection Pro, its
        owners, employees, and affiliates shall not be liable for any losses or
        damages arising from your use of, or reliance on, the website or any
        report or information it provides.
      </p>
      <p>
        This includes, but is not limited to, financial losses related to the
        purchase or sale of a vehicle, repair costs, and incidental or
        consequential damages.
      </p>
      <p>
        To the extent permitted by applicable law, our total aggregate liability
        shall not exceed the amount you paid for the specific report that gave
        rise to the claim.
      </p>

      {/* ===== 10 ===== */}
      <h2 id="contact" className="text-xl font-bold text-slate-900">
        10. Contact
      </h2>
      <p>
        If you have any questions about this Disclaimer or the information in our
        reports, you may reach us through the contact channel available on the Car
        Inspection Pro website.
      </p>
    </LegalPage>
  );
}