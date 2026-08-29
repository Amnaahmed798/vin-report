import Image from "next/image";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white">
      <div className="mx-auto max-w-[1240px] px-5 sm:px-8">

        {/* =====================================================
            MAIN FOOTER
        ===================================================== */}

        <div className="grid gap-12 py-16 sm:grid-cols-2 lg:grid-cols-4 lg:py-20">

          {/* =================================================
              BRAND + CTA
          ================================================= */}

          <div className="sm:col-span-2 lg:col-span-1">

            <Link
              href="/"
              aria-label="Car Inspection Pro home"
              className="inline-block"
            >
              <Image
                src="/images/carinspectionlogo.JPG"
                alt="Car Inspection Pro"
                width={840}
                height={253}
                className="h-auto w-[220px] object-contain"
              />
            </Link>

            <p className="mt-5 max-w-[300px] text-[13px] leading-6 text-slate-500">
              Professional vehicle history reports powered by
              NHTSA, NMVTIS & EPA data.
            </p>

            <Link
              href="/"
              className="
                mt-6
                inline-flex
                items-center
                gap-2
                rounded-lg
                bg-blue-600
                px-5
                py-2.5
                text-sm
                font-semibold
                text-white
                transition-all
                duration-200
                hover:bg-blue-700
              "
            >
              Get a Report
              <svg viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                <path
                  fillRule="evenodd"
                  d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z"
                  clipRule="evenodd"
                />
              </svg>
            </Link>
          </div>

          {/* =================================================
              REPORT
          ================================================= */}

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-950">
              Report
            </h3>

            <ul className="mt-5 space-y-3">
              {[
                { label: "Vehicle Checks", href: "/#features" },
                { label: "How It Works", href: "/#how-it-works" },
                { label: "Get a Report", href: "/" },
              ].map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-500 transition-colors hover:text-blue-600"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* =================================================
              DATA SOURCES
          ================================================= */}

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-950">
              Data Sources
            </h3>

            <ul className="mt-5 space-y-3">
              {[
                { label: "NHTSA Recalls", href: "https://www.nhtsa.gov/recalls", external: true },
                { label: "NHTSA Complaints", href: "https://www.nhtsa.gov/report-a-safety-problem", external: true },
                { label: "EPA Fuel Economy", href: "https://www.fueleconomy.gov", external: true },
                { label: "NMVTIS Records", href: "https://www.nhtsa.gov/nhtsa-data-visualizations", external: false },
              ].map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    {...(link.external ? { target: "_blank", rel: "noopener noreferrer" } : {})}
                    className="inline-flex items-center gap-1.5 text-sm text-slate-500 transition-colors hover:text-blue-600"
                  >
                    {link.label}
                    {link.external && (
                      <svg viewBox="0 0 20 20" fill="currentColor" className="h-3 w-3 opacity-40">
                        <path
                          fillRule="evenodd"
                          d="M4.25 5.5a.75.75 0 00-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 00.75-.75v-4a.75.75 0 011.5 0v4A2.25 2.25 0 0112.75 17h-8.5A2.25 2.25 0 012 14.75v-8.5A2.25 2.25 0 014.25 4h5a.75.75 0 010 1.5h-5zm7.25-.75a.75.75 0 01.75-.75h3.25a.75.75 0 01.75.75v3.25a.75.75 0 01-1.5 0V6.31l-5.47 5.47a.75.75 0 11-1.06-1.06l5.47-5.47H12.25a.75.75 0 01-.75-.75z"
                          clipRule="evenodd"
                        />
                      </svg>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* =================================================
              LEGAL
          ================================================= */}

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-950">
              Legal
            </h3>

            <ul className="mt-5 space-y-3">
              {[
                { label: "Privacy Policy", href: "/privacy" },
                { label: "Terms & Conditions", href: "/terms" },
                { label: "Disclaimer", href: "/disclaimer" },
              ].map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-500 transition-colors hover:text-blue-600"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* =====================================================
            BOTTOM BAR
        ===================================================== */}

        <div
          className="
            flex
            flex-col
            items-center
            justify-between
            gap-3
            border-t
            border-slate-200
            py-6
            sm:flex-row
          "
        >
          <p className="text-xs text-slate-400">
            &copy; {new Date().getFullYear()} Car Inspection Pro. All rights reserved.
          </p>

          <span className="text-xs text-slate-400">
            Free reports &middot; No account required
          </span>
        </div>

      </div>
    </footer>
  );
}
