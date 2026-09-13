"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";
import { useState } from "react";
import { validateVin } from "@/lib/api";

const SAMPLE_VINS = [
  {
    vin: "WBADX7C5XDJ589276",
    label: "BMW 335i",
  },
  {
    vin: "1HGCM82633A004352",
    label: "Honda Accord",
  },
];

export default function Hero() {
  const router = useRouter();

  const [vin, setVin] = useState("");
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const trimmed = vin.trim().toUpperCase();

    const err = validateVin(trimmed);

    if (err) {
      setError(err);
      return;
    }

    setError(null);

    router.push(`/plans/${trimmed}`);
  }

  return (
    <section className="relative isolate overflow-hidden bg-slate-50">

      {/* =====================================================
          BACKGROUND
      ===================================================== */}

      {/* Large soft blue glow */}

      <div
        className="
          pointer-events-none
          absolute
          -left-[220px]
          top-[80px]
          h-[600px]
          w-[600px]
          rounded-full
          bg-blue-100/70
          blur-[100px]
        "
        aria-hidden="true"
      />

      <div
        className="
          pointer-events-none
          absolute
          -right-[180px]
          bottom-[-180px]
          h-[550px]
          w-[550px]
          rounded-full
          bg-blue-50
          blur-[100px]
        "
        aria-hidden="true"
      />

      {/* Subtle grid */}

      <div
        className="
          pointer-events-none
          absolute
          inset-0
          opacity-40
          hero-grid
        "
        aria-hidden="true"
      />

      {/* =====================================================
          MAIN CONTAINER
      ===================================================== */}

      <div
        className="
          relative
          mx-auto
          grid
          min-h-[680px]
          max-w-[1280px]
          items-center
          gap-8
          px-5
          pb-16
          pt-12
          sm:px-8
          sm:pb-20
          sm:pt-16
          lg:grid-cols-[0.95fr_1.05fr]
          lg:gap-0
          lg:pb-20
          lg:pt-12
        "
      >

        {/* =====================================================
            LEFT — VEHICLE
        ===================================================== */}

        <div
          className="
            animate-fade-up
            order-2
            relative
            flex
            min-h-[340px]
            items-center
            justify-center
            lg:order-1
            lg:min-h-[570px]
          "
        >

          {/* Decorative circle */}

          <div
            className="
              pointer-events-none
              absolute
              left-1/2
              top-1/2
              h-[340px]
              w-[340px]
              -translate-x-1/2
              -translate-y-1/2
              rounded-full
              border
              border-blue-100
              bg-blue-50/50
              sm:h-[440px]
              sm:w-[440px]
            "
          />

          <div
            className="
              pointer-events-none
              absolute
              left-1/2
              top-1/2
              h-[270px]
              w-[270px]
              -translate-x-1/2
              -translate-y-1/2
              rounded-full
              border
              border-blue-100/70
              sm:h-[360px]
              sm:w-[360px]
            "
          />

          {/* Floor shadow */}

          <div
            className="
              pointer-events-none
              absolute
              bottom-[55px]
              left-1/2
              h-[55px]
              w-[75%]
              -translate-x-1/2
              rounded-[50%]
              bg-slate-900/15
              blur-2xl
              sm:bottom-[65px]
            "
          />

          {/* Car */}

          <Image
            src="/images/car.png"
            alt="Vehicle"
            width={1000}
            height={525}
            priority
            className="
              relative
              z-10
              w-full
              max-w-[680px]
              object-contain
              drop-shadow-[0_30px_35px_rgba(15,23,42,0.16)]
              transition-transform
              duration-700
              ease-out
              hover:scale-[1.025]
            "
          />

          {/* Floating information badge */}

          <div
            className="
              absolute
              bottom-[40px]
              left-[2%]
              z-20
              hidden
              items-center
              gap-3
              rounded-2xl
              border
              border-white
              bg-white/90
              px-4
              py-3
              shadow-[0_15px_40px_rgba(15,23,42,0.10)]
              backdrop-blur
              sm:flex
              lg:left-[0%]
            "
          >
            <div
              className="
                flex
                h-9
                w-9
                items-center
                justify-center
                rounded-full
                bg-emerald-50
                text-emerald-600
              "
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>

            <div>
              <p className="text-xs font-bold text-slate-900">
                Vehicle verified
              </p>

              <p className="mt-0.5 text-[11px] text-slate-400">
                Official data sources
              </p>
            </div>
          </div>

          {/* Floating report badge */}

          <div
            className="
              absolute
              right-[2%]
              top-[18%]
              z-20
              hidden
              rounded-2xl
              border
              border-white
              bg-white/90
              px-4
              py-3
              shadow-[0_15px_40px_rgba(15,23,42,0.10)]
              backdrop-blur
              sm:block
              lg:right-[0%]
            "
          >
            <div className="flex items-center gap-3">

              <div className="flex -space-x-1">
                <span className="h-7 w-7 rounded-full border-2 border-white bg-blue-100" />
                <span className="h-7 w-7 rounded-full border-2 border-white bg-blue-200" />
                <span className="h-7 w-7 rounded-full border-2 border-white bg-blue-300" />
              </div>

              <div>
                <p className="text-xs font-bold text-slate-900">
                  Full vehicle report
                </p>

                <p className="text-[11px] text-slate-400">
                  Ready in seconds
                </p>
              </div>

            </div>
          </div>
        </div>

        {/* =====================================================
            RIGHT — CONTENT
        ===================================================== */}

        <div
          className="
            order-1
            relative
            z-20
            lg:order-2
            lg:pl-8
            xl:pl-14
          "
        >

          {/* Eyebrow */}

          <div
            className="
              animate-fade-up
              inline-flex
              items-center
              gap-2
              rounded-full
              border
              border-blue-100
              bg-blue-50/80
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

            Vehicle history intelligence
          </div>

          {/* Heading */}

          <h1
            className="
              animate-fade-up
              delay-100
              mt-6
              max-w-[650px]
              text-[42px]
              font-extrabold
              leading-[1.04]
              tracking-[-2px]
              text-slate-950
              sm:text-5xl
              lg:text-[60px]
              xl:text-[64px]
            "
          >
            Know the car.
            <br />

            <span className="text-blue-600">
              Before you buy.
            </span>
          </h1>

          {/* Description */}

          <p
            className="
              animate-fade-up
              delay-200
              mt-6
              max-w-[570px]
              text-base
              leading-7
              text-slate-500
              sm:text-lg
            "
          >
            Get a clear picture of any vehicle before you make
            a decision. Check its history, recalls, specifications,
            and important records using its VIN.
          </p>

          {/* =====================================================
              SEARCH
          ===================================================== */}

          <div
            className="
              animate-fade-up
              delay-300
              mt-8
            "
          >

            {/* Search label */}

            <div className="mb-3 flex items-center gap-3">

              <span className="text-sm font-bold text-slate-950">
                Search by VIN
              </span>

              <span
                className="
                  h-[2px]
                  w-10
                  rounded-full
                  bg-blue-600
                "
              />
            </div>

            {/* VIN form */}

            <form
              onSubmit={handleSubmit}
              className="w-full max-w-[650px]"
            >
              <div
                className="
                  group
                  flex
                  min-h-[72px]
                  items-center
                  gap-3
                  rounded-2xl
                  border
                  border-slate-200
                  bg-white
                  p-2
                  pl-5
                  shadow-[0_15px_45px_rgba(15,23,42,0.08)]
                  transition-all
                  duration-300
                  focus-within:border-blue-300
                  focus-within:shadow-[0_20px_55px_rgba(37,99,235,0.12)]
                  sm:rounded-full
                "
              >

                {/* Search icon */}

                <div
                  className="
                    flex
                    h-10
                    w-10
                    shrink-0
                    items-center
                    justify-center
                    rounded-xl
                    bg-blue-50
                    text-blue-600
                    sm:rounded-full
                  "
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <circle cx="11" cy="11" r="7" />

                    <path
                      d="m20 20-4-4"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>

                {/* Input */}

                <input
                  id="vin-input"
                  type="text"
                  value={vin}
                  onChange={(e) => {
                    setVin(e.target.value.toUpperCase());
                    setError(null);
                  }}
                  placeholder="Enter your 17-character VIN"
                  maxLength={17}
                  autoComplete="off"
                  spellCheck={false}
                  aria-label="Vehicle identification number"
                  className="
                    min-w-0
                    flex-1
                    bg-transparent
                    px-1
                    text-base
                    font-semibold
                    tracking-[0.04em]
                    text-slate-900
                    outline-none
                    sm:tracking-[0.08em]
                    placeholder:font-sans
                    placeholder:tracking-normal
                    placeholder:text-slate-400
                  "
                />

                {/* Submit */}

                <button
                  type="submit"
                  className="
                    group/btn
                    flex
                    h-[54px]
                    w-[54px]
                    shrink-0
                    items-center
                    justify-center
                    rounded-xl
                    bg-blue-600
                    text-sm
                    font-bold
                    text-white
                    shadow-lg
                    shadow-blue-600/20
                    transition-all
                    duration-200
                    hover:-translate-y-0.5
                    hover:bg-blue-700
                    hover:shadow-xl
                    hover:shadow-blue-600/25
                    active:translate-y-0
                    sm:w-auto
                    sm:rounded-full
                    sm:px-7
                  "
                >
                  <span className="hidden sm:inline">
                    Check VIN
                  </span>

                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="
                      h-4
                      w-4
                      transition-transform
                      duration-200
                      group-hover/btn:translate-x-1
                    "
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2.5}
                  >
                    <path
                      d="M5 12h14"
                      strokeLinecap="round"
                    />

                    <path
                      d="m13 6 6 6-6 6"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>

              </div>

              {/* Error */}

              {error && (
                <p
                  className="
                    mt-3
                    px-3
                    text-sm
                    font-semibold
                    text-red-500
                  "
                >
                  {error}
                </p>
              )}
            </form>

            {/* =================================================
                SAMPLE VIN
            ================================================= */}

            <div className="mt-5 flex flex-wrap items-center gap-2">

              <span className="text-xs font-semibold text-slate-400">
                Try a sample:
              </span>

              {SAMPLE_VINS.map((sample) => (
                <button
                  key={sample.vin}
                  type="button"
                  onClick={() => {
                    setVin(sample.vin);
                    setError(null);
                  }}
                  className="
                    group
                    rounded-full
                    border
                    border-slate-200
                    bg-white
                    px-3
                    py-1.5
                    font-mono
                    text-[11px]
                    font-medium
                    text-slate-500
                    shadow-sm
                    transition-all
                    duration-200
                    hover:border-blue-200
                    hover:bg-blue-50
                    hover:text-blue-600
                  "
                >
                  {sample.vin}

                  <span
                    className="
                      ml-2
                      font-sans
                      text-slate-400
                      group-hover:text-blue-400
                    "
                  >
                    {sample.label}
                  </span>
                </button>
              ))}

            </div>

          </div>

          {/* =====================================================
              TRUST POINTS
          ===================================================== */}

          <div
            className="
              animate-fade-up
              delay-300
              mt-8
              flex
              flex-wrap
              gap-3
            "
          >
            {[
              {
                text: "Free VIN check",
                icon: (
                  <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                ),
              },
              {
                text: "No account required",
                icon: (
                  <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                ),
              },
              {
                text: "Official vehicle data",
                icon: (
                  <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                ),
              },
            ].map((item) => (
              <div
                key={item.text}
                className="
                  inline-flex
                  items-center
                  gap-2.5
                  rounded-full
                  border
                  border-slate-200
                  bg-white
                  px-4
                  py-2.5
                  shadow-sm
                "
              >
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-600 text-white">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    className="h-3.5 w-3.5"
                  >
                    {item.icon}
                  </svg>
                </span>
                <span className="text-sm font-medium text-slate-600">
                  {item.text}
                </span>
              </div>
            ))}
          </div>

        </div>
      </div>

      {/* =====================================================
          BOTTOM EDGE
      ===================================================== */}

      <div className="relative border-t border-slate-200 bg-slate-100/60">
        <div className="mx-auto flex max-w-[1240px] items-center justify-center px-5 py-4">
          <p className="text-center text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">
            Vehicle information made simple
          </p>
        </div>
      </div>

    </section>
  );
}




