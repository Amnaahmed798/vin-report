"use client";

import { useEffect, useRef } from "react";
import Image from "next/image";

const HISTORY_CHECKS = [
  {
    number: "01",
    title: "Accident & Damage History",
    description:
      "Comprehensive accident and damage records from NMVTIS and insurance databases, including severity, location, and repair history.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
      />
    ),
    image: "/images/damagehistory.jpg",
  },
  {
    number: "02",
    title: "Odometer Readings",
    description:
      "Complete odometer history to detect rollback, tampering, or inconsistencies across ownership transfers.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    ),
    image: "/images/odometercheck.jpg",
  },
  {
    number: "03",
    title: "Ownership History",
    description:
      "Number of previous owners, ownership type (personal, lease, fleet), duration, and geographic history.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"
      />
    ),
    image: "/images/ownershiphistory.jpg",
  },
  {
    number: "04",
    title: "Title History",
    description:
      "Complete title record including salvage, junk, rebuilt, flood, fire, and lemon brand checks from state DMVs.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
      />
    ),
    image: "/images/tittlehistory.jpeg",
  },
  {
    number: "05",
    title: "Theft Records",
    description:
      "Checked against NMVTIS databases and participating insurance records for reported stolen vehicle status and theft recovery.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"
      />
    ),
    image: "/images/theftrecord.jpeg",
  },
  {
    number: "06",
    title: "Service Records",
    description:
      "Oil changes, tire rotations, brake service, and other maintenance records reported by dealers and service centers.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085"
      />
    ),
    image: "/images/servicerecord.jpg",
  },
  {
    number: "07",
    title: "Safety Recalls",
    description:
      "Open NHTSA recall campaigns, why they were issued, and the free remedy information for your vehicle.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
      />
    ),
    image: "/images/safteyrecalls.jpg",
  },
  {
    number: "08",
    title: "Vehicle Specifications",
    description:
      "Year, make, model, trim, engine, transmission, drive type, fuel type, and body style decoded from the VIN.",
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12"
      />
    ),
    image: "/images/vehicalspecs.webp",
  },
];

export default function HistoryChecks() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const section = sectionRef.current;

    if (!section) return;

    const elements = section.querySelectorAll(".history-reveal");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: "0px 0px -80px 0px",
      }
    );

    elements.forEach((element) => observer.observe(element));

    return () => observer.disconnect();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="features"
      className="relative overflow-hidden bg-white py-24 sm:py-28 lg:py-32"
    >
      {/* =====================================================
          BACKGROUND
      ===================================================== */}

      <div
        className="
          pointer-events-none
          absolute
          left-1/2
          top-0
          h-[500px]
          w-[900px]
          -translate-x-1/2
          rounded-full
          bg-blue-50/60
          blur-3xl
        "
        aria-hidden="true"
      />

      <div
        className="
          pointer-events-none
          absolute
          bottom-0
          left-0
          h-[300px]
          w-[300px]
          rounded-full
          bg-slate-50
          blur-3xl
        "
        aria-hidden="true"
      />

      <div className="relative mx-auto max-w-[1240px] px-5 sm:px-8">

        {/* =====================================================
            SECTION HEADER
        ===================================================== */}

        <div className="mx-auto max-w-[760px] text-center">

          {/* Label */}

          <div
            className="
              history-reveal
              inline-flex
              items-center
              gap-2
              rounded-full
              border
              border-blue-100
              bg-blue-50/70
              px-4
              py-2
              text-[11px]
              font-bold
              uppercase
              tracking-[0.18em]
              text-blue-600
            "
          >
            <span className="h-1.5 w-1.5 rounded-full bg-blue-600" />

            Vehicle intelligence
          </div>

          {/* Heading */}

          <h2
            className="
              history-reveal
              mt-6
              text-[40px]
              font-extrabold
              leading-[1.05]
              tracking-[-1.8px]
              text-slate-950
              sm:text-5xl
              lg:text-[56px]
            "
          >
            Know what you&apos;re buying.
            <br />

            <span className="text-slate-400">
              Before you buy.
            </span>
          </h2>

          {/* Description */}

          <p
            className="
              history-reveal
              mx-auto
              mt-6
              max-w-[650px]
              text-base
              leading-7
              text-slate-500
              sm:text-lg
            "
          >
            A vehicle can look perfect on the outside and still
            have a history you need to know about. We bring the
            important details together in one clear report.
          </p>

        </div>

        {/* =====================================================
            FEATURE GRID
        ===================================================== */}

        <div
          className="
            mt-16
            grid
            gap-5
            sm:mt-20
            sm:grid-cols-2
            lg:grid-cols-3
          "
        >

          {HISTORY_CHECKS.map((item) => (
            <article
              key={item.number}
              className="
                history-reveal
                history-card
                group
                relative
                overflow-hidden
                rounded-[24px]
                border
                border-slate-200
                bg-white
                shadow-[0_8px_30px_rgba(15,23,42,0.04)]
                transition-all
                duration-500
                hover:-translate-y-2
                hover:border-blue-200
                hover:shadow-[0_25px_60px_rgba(15,23,42,0.10)]
              "
            >

              {/* Top blue line */}

              <div
                className="
                  absolute
                  left-0
                  right-0
                  top-0
                  z-20
                  h-[3px]
                  origin-left
                  scale-x-0
                  bg-blue-600
                  transition-transform
                  duration-500
                  group-hover:scale-x-100
                "
              />

              {/* Image (if present) */}

              {item.image ? (
                <div className="relative h-[180px] w-full overflow-hidden">
                  <Image
                    src={item.image}
                    alt={item.title}
                    fill
                    className="object-cover transition-transform duration-500 group-hover:scale-105"
                    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-white/90 via-white/20 to-transparent" />
                </div>
              ) : null}

              <div className="p-7">

              {/* Header row */}

              <div className="flex items-start justify-between">

                {/* Icon */}

                <div
                  className="
                    flex
                    h-12
                    w-12
                    items-center
                    justify-center
                    rounded-2xl
                    bg-blue-50
                    text-blue-600
                    transition-colors
                    duration-300
                    group-hover:bg-blue-600
                    group-hover:text-white
                  "
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.8}
                  >
                    {item.icon}
                  </svg>
                </div>

                {/* Number */}

                <span
                  className="
                    text-xs
                    font-extrabold
                    tracking-widest
                    text-slate-300
                    transition-colors
                    duration-300
                    group-hover:text-blue-600
                  "
                >
                  {item.number}
                </span>

              </div>

              {/* Content */}

              <h3
                className="
                  mt-5
                  text-[21px]
                  font-bold
                  tracking-[-0.5px]
                  text-slate-950
                "
              >
                {item.title}
              </h3>

              <p
                className="
                  mt-3
                  text-[14px]
                  leading-6
                  text-slate-500
                "
              >
                {item.description}
              </p>

              </div>

            </article>
          ))}

        </div>

        {/* =====================================================
            TRUST ROW
        ===================================================== */}


      </div>
    </section>
  );
}
