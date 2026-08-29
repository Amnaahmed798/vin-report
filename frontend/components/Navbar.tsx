import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50">
      {/* Top accent bar */}
      <div className="h-[3px] bg-gradient-to-r from-blue-600 via-blue-500 to-blue-400" />

      {/* Main navbar */}
      <div className="border-b border-slate-200/80 bg-white shadow-[0_1px_3px_rgba(0,0,0,0.04)]">
        <div className="mx-auto flex max-w-[1240px] items-center justify-between px-6 pt-3 pb-1 lg:px-8">

          {/* Logo */}
          <Link
            href="/"
            aria-label="Car Inspection Pro home"
            className="shrink-0 transition-opacity hover:opacity-90"
          >
            <Image
              src="/images/carinspectionlogo.JPG"
              alt="Car Inspection Pro"
              width={840}
              height={253}
              priority
              className="h-auto w-[220px] object-contain lg:w-[240px]"
            />
          </Link>

          {/* Navigation */}
          <nav className="hidden items-center gap-1.5 md:flex">
            <Link
              href="/#features"
              className="
                group
                relative
                rounded-full
                px-5
                py-2
                text-[14px]
                font-semibold
                uppercase
                tracking-[0.06em]
                text-slate-600
                transition-all
                duration-200
                hover:bg-blue-50
                hover:text-blue-700
                hover:shadow-[0_0_0_1px_rgba(37,99,235,0.1)]
              "
            >
              Features
              <span className="absolute bottom-0.5 left-1/2 h-[2px] w-0 -translate-x-1/2 rounded-full bg-blue-600 transition-all duration-300 group-hover:w-[60%]" />
            </Link>

            <Link
              href="/#sources"
              className="
                group
                relative
                rounded-full
                px-5
                py-2
                text-[14px]
                font-semibold
                uppercase
                tracking-[0.06em]
                text-slate-600
                transition-all
                duration-200
                hover:bg-blue-50
                hover:text-blue-700
                hover:shadow-[0_0_0_1px_rgba(37,99,235,0.1)]
              "
            >
              Data Sources
              <span className="absolute bottom-0.5 left-1/2 h-[2px] w-0 -translate-x-1/2 rounded-full bg-blue-600 transition-all duration-300 group-hover:w-[60%]" />
            </Link>

            <Link
              href="/privacy"
              className="
                group
                relative
                rounded-full
                px-5
                py-2
                text-[14px]
                font-semibold
                uppercase
                tracking-[0.06em]
                text-slate-600
                transition-all
                duration-200
                hover:bg-blue-50
                hover:text-blue-700
                hover:shadow-[0_0_0_1px_rgba(37,99,235,0.1)]
              "
            >
              Privacy Policy
              <span className="absolute bottom-0.5 left-1/2 h-[2px] w-0 -translate-x-1/2 rounded-full bg-blue-600 transition-all duration-300 group-hover:w-[60%]" />
            </Link>
          </nav>

          {/* Check VIN button */}
          <Link
            href="/"
            className="
              group
              flex
              h-[44px]
              items-center
              gap-2.5
              rounded-full
              bg-blue-600
              px-5
              text-[14px]
              font-semibold
              text-white
              shadow-[0_2px_8px_rgba(37,99,235,0.3)]
              transition-all
              duration-200
              hover:bg-blue-700
              hover:shadow-[0_4px_12px_rgba(37,99,235,0.4)]
            "
          >
            {/* Search icon */}
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="M21 21l-4.35-4.35" />
            </svg>

            <span>Check VIN</span>
          </Link>

        </div>
      </div>
    </header>
  );
}