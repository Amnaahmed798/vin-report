"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { fetchVinReport, type VinReport } from "@/lib/api";
import Navbar from "@/components/Navbar";

const PLANS_FROM_USD = 45;

type Stat = {
  label: string;
  value: string;
  tone: "ok" | "warn" | "na" | "bad";
};

type SpecItem = {
  label: string;
  value: string | undefined;
};

export default function ReportPage({ params }: { params: Promise<{ vin: string }> }) {
  const { vin: initialVin } = use(params);
  const [vin, setVin] = useState<string>(initialVin);
  const [report, setReport] = useState<VinReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchVinReport(initialVin)
      .then((r) => { if (!cancelled) setReport(r); })
      .catch((err: Error) => { if (!cancelled) setError(err.message); });
    return () => { cancelled = true; };
  }, [initialVin]);

  const vehicle = report?.vehicle;
  const statuses = report?.statuses ?? {};

  const v = vehicle as Record<string, string | undefined>;
  const specs: SpecItem[] = vehicle
    ? [
        { label: "Year", value: v.ModelYear },
        { label: "Make", value: v.Make },
        { label: "Model", value: v.Model },
        { label: "Trim", value: v.Trim || v.Series },
        { label: "Body Style", value: v.BodyClass },
        { label: "Doors", value: v.Doors },
        { label: "Engine", value: v.DisplacementL ? `${v.DisplacementL}L ${v.EngineCylinders || ""}-Cyl` : undefined },
        { label: "Horsepower", value: v.EngineHP ? `${v.EngineHP} HP` : undefined },
        { label: "Transmission", value: v.TransmissionStyle },
        { label: "Drive Type", value: v.DriveType },
        { label: "Fuel Type", value: v.FuelTypePrimary },
        { label: "Plant", value: v.PlantCity && v.PlantCountry ? `${v.PlantCity}, ${v.PlantCountry}` : v.PlantCountry },
      ].filter((s) => s.value)
    : [];

  const stats: Stat[] = [];
  if (report) {
    const recalls = report.recalls.length;
    const complaints = report.complaints.length;
    const tsbs = report.tsbs.length;
    const investigations = report.investigations.length;
    const fuelMpg = report.fuel?.comb08;

    stats.push({
      label: "Safety Recalls",
      value: statuses["Recalls"] === "unavailable" ? "N/A" : recalls > 0 ? `${recalls} Open` : "None Found",
      tone: statuses["Recalls"] === "unavailable" ? "na" : recalls > 0 ? "bad" : "ok",
    });
    stats.push({
      label: "Owner Complaints",
      value: statuses["Complaints"] === "unavailable" ? "N/A" : complaints > 0 ? `${complaints} Filed` : "None Found",
      tone: statuses["Complaints"] === "unavailable" ? "na" : complaints > 0 ? "warn" : "ok",
    });
    stats.push({
      label: "TSBs",
      value: statuses["TSB DB"] === "unavailable" ? "N/A" : tsbs > 0 ? `${tsbs} Found` : "None Found",
      tone: statuses["TSB DB"] === "unavailable" ? "na" : tsbs > 0 ? "warn" : "ok",
    });
    stats.push({
      label: "Investigations",
      value: statuses["Investigations DB"] === "unavailable" ? "N/A" : investigations > 0 ? `${investigations} Found` : "None Found",
      tone: statuses["Investigations DB"] === "unavailable" ? "na" : investigations > 0 ? "warn" : "ok",
    });
    stats.push({
      label: "Fuel Economy",
      value: fuelMpg ? `${fuelMpg} MPG` : "N/A",
      tone: fuelMpg ? "ok" : "na",
    });
    stats.push({
      label: "Crash Rating",
      value: report.safety.length > 0 ? "Tested" : "Not Rated",
      tone: report.safety.length > 0 ? "ok" : "na",
    });
  }

  const toneBg: Record<string, string> = {
    ok: "bg-emerald-50 text-emerald-700",
    warn: "bg-amber-50 text-amber-700",
    na: "bg-slate-50 text-slate-400",
    bad: "bg-rose-50 text-rose-700",
  };

  const toneDot: Record<string, string> = {
    ok: "bg-emerald-500",
    warn: "bg-amber-500",
    na: "bg-slate-300",
    bad: "bg-rose-500",
  };

  return (
    <div className="flex min-h-screen flex-col bg-slate-100">
      <Navbar />

      <main className="w-full flex-1 px-4 pb-20 sm:px-6 lg:px-8">

        {/* =================================================
            ERROR STATE
        ================================================= */}

        {error && (
          <div className="flex flex-col items-center justify-center py-32 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-rose-50">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
            </div>
            <h1 className="mt-6 text-2xl font-bold text-slate-900">Couldn&apos;t load report</h1>
            <p className="mt-2 max-w-md text-sm text-slate-500">{error}</p>
            <Link href="/" className="mt-8 inline-flex items-center gap-2 rounded-full bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700">
              Try another VIN
            </Link>
          </div>
        )}

        {!error && (
          <>
            {/* Back link */}
            <Link href="/" className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 transition-colors hover:text-blue-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                <path d="M19 12H5" />
                <path d="m12 19-7-7 7-7" />
              </svg>
              Back to search
            </Link>

            {/* =================================================
                HEADER
            ================================================= */}

            <div className="mt-4 overflow-hidden border border-slate-300 bg-white shadow-sm">
              <div className="h-[3px] w-full bg-gradient-to-r from-blue-600 to-blue-400" />

              <div className="flex flex-col gap-5 px-6 py-6 sm:px-8 lg:flex-row lg:items-center lg:justify-between">
                <div className="min-w-0">
                  <div className="flex items-center gap-2.5">
                    <span className="inline-flex items-center gap-1.5 rounded-md bg-blue-600 px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-white">
                      Free Preview
                    </span>
                    <span className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 bg-slate-50 px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-slate-500">
                      NHTSA + EPA Data
                    </span>
                  </div>
                  <h1 className="mt-3 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-[28px]">
                    {vehicle ? (
                      <>{vehicle.ModelYear} {vehicle.Make} {vehicle.Model}</>
                    ) : (
                      <span className="inline-block h-8 w-72 animate-pulse rounded bg-slate-200" />
                    )}
                  </h1>
                  <div className="mt-2.5 flex flex-wrap items-center gap-2">
                    <span className="rounded-md border border-slate-300 bg-slate-50 px-2.5 py-1 font-mono text-xs font-bold tracking-wider text-slate-700">
                      {vin}
                    </span>
                    {vehicle?.Trim && (
                      <span className="rounded-md border border-slate-300 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-500">
                        {vehicle.Trim || vehicle.Series}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex shrink-0 items-center gap-4">
                  <div className="text-right">
                    <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Plans Starting At</p>
                    <p className="mt-0.5 text-2xl font-extrabold text-slate-900">${PLANS_FROM_USD}</p>
                  </div>
                  <Link
                    href={`/plans/${vin}`}
                    className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-3 text-sm font-bold text-white shadow-md shadow-blue-600/20 transition-all hover:bg-blue-700 hover:shadow-lg"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Get Full Report
                  </Link>
                </div>
              </div>

              {/* Stats bar */}
              <div className="grid grid-cols-3 border-t border-slate-200 sm:grid-cols-6">
                {report
                  ? stats.map((s, i) => (
                      <div
                        key={s.label}
                        className={`px-4 py-3.5 ${i > 0 ? "border-l border-slate-200" : ""}`}
                      >
                        <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{s.label}</p>
                        <div className="mt-1.5 flex items-center gap-1.5">
                          <span className={`h-1.5 w-1.5 rounded-full ${toneDot[s.tone]}`} />
                          <span className={`text-sm font-bold ${toneBg[s.tone]}`}>{s.value}</span>
                        </div>
                      </div>
                    ))
                  : Array.from({ length: 6 }).map((_, i) => (
                      <div key={i} className={`px-4 py-3.5 ${i > 0 ? "border-l border-slate-200" : ""}`}>
                        <div className="h-3 w-16 animate-pulse rounded bg-slate-200" />
                        <div className="mt-2 h-4 w-12 animate-pulse rounded bg-slate-200" />
                      </div>
                    ))
                }
              </div>
            </div>

            {/* =================================================
                TWO-COLUMN LAYOUT: DATA LEFT + MARKETING RIGHT
            ================================================= */}

            <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_340px]">

              {/* ---- LEFT: DATA ---- */}
              <div className="space-y-6">

                {/* Vehicle Specs */}
                {vehicle && specs.length > 0 && (
                  <div className="overflow-hidden border border-slate-300 bg-white shadow-sm">
                    <div className="flex items-center justify-between border-b border-slate-300 bg-slate-50 px-5 py-3">
                      <div className="flex items-center gap-3">
                        <h2 className="text-sm font-bold text-slate-900">Vehicle Specifications</h2>
                        <span className="bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-500">VIN DECODE</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 divide-x divide-y divide-slate-200 sm:grid-cols-3">
                      {specs.map((spec) => (
                        <div key={spec.label} className="px-5 py-3.5">
                          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{spec.label}</p>
                          <p className="mt-1 text-sm font-semibold text-slate-800">{spec.value}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Fuel Economy */}
                {report?.fuel && (
                  <div className="overflow-hidden border border-slate-300 bg-white shadow-sm">
                    <div className="flex items-center justify-between border-b border-slate-300 bg-slate-50 px-5 py-3">
                      <div className="flex items-center gap-3">
                        <h2 className="text-sm font-bold text-slate-900">Fuel Economy</h2>
                        <span className="bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-600">EPA</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 divide-x divide-slate-200">
                      {[
                        { label: "City", value: report.fuel.city08, unit: "MPG" },
                        { label: "Highway", value: report.fuel.highway08, unit: "MPG" },
                        { label: "Combined", value: report.fuel.comb08, unit: "MPG" },
                      ].map((item) => (
                        <div key={item.label} className="px-5 py-5 text-center">
                          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{item.label}</p>
                          <p className="mt-1 text-2xl font-extrabold text-slate-900">{item.value || "—"}</p>
                          <p className="text-[10px] text-slate-400">{item.unit}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Safety Ratings */}
                {report && report.safety.length > 0 && (
                  <div className="overflow-hidden border border-slate-300 bg-white shadow-sm">
                    <div className="flex items-center justify-between border-b border-slate-300 bg-slate-50 px-5 py-3">
                      <div className="flex items-center gap-3">
                        <h2 className="text-sm font-bold text-slate-900">NHTSA Safety Ratings</h2>
                        <span className="bg-blue-50 px-2 py-0.5 text-[10px] font-bold text-blue-600">NCAP</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 divide-x divide-y divide-slate-200">
                      {report.safety.slice(0, 1).map((s) => {
                        const ratings = [
                          { label: "Overall", value: s.OverallRating },
                          { label: "Front (Driver)", value: s.FrontCrashDriversideRating },
                          { label: "Front (Pass.)", value: s.FrontCrashPassengersideRating },
                          { label: "Side (Driver)", value: s.SideCrashDriversideRating },
                          { label: "Side (Pass.)", value: s.SideCrashPassengersideRating },
                          { label: "Rollover", value: s.RolloverRating },
                        ];
                        return ratings.map((r) => (
                          <div key={r.label} className="px-5 py-3.5">
                            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{r.label}</p>
                            <p className="mt-1 text-lg font-extrabold text-slate-900">
                              {r.value && r.value !== "0" ? (
                                <span className="text-blue-600">{r.value}</span>
                              ) : (
                                <span className="text-slate-300">—</span>
                              )}
                              {r.value && r.value !== "0" && <span className="ml-0.5 text-xs font-normal text-slate-400">/5</span>}
                            </p>
                          </div>
                        ));
                      })}
                    </div>
                  </div>
                )}

                {/* Recalls */}
                {report && report.recalls.length > 0 && (
                  <div className="overflow-hidden border border-slate-300 bg-white shadow-sm">
                    <div className="flex items-center justify-between border-b border-slate-300 bg-slate-50 px-5 py-3">
                      <div className="flex items-center gap-3">
                        <h2 className="text-sm font-bold text-slate-900">Safety Recalls</h2>
                        <span className="bg-rose-50 px-2 py-0.5 text-[10px] font-bold text-rose-600">{report.recalls.length}</span>
                      </div>
                    </div>
                    <div className="overflow-x-auto">
                      <table className="w-full border-collapse text-left">
                        <thead>
                          <tr className="border-b border-slate-300 bg-slate-50">
                            <th className="px-4 py-2.5 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">Campaign</th>
                            <th className="px-4 py-2.5 text-left text-[11px] font-bold uppercase tracking-wider text-slate-500">Component</th>
                          </tr>
                        </thead>
                        <tbody>
                          {report.recalls.slice(0, 10).map((r, i) => (
                            <tr key={i} className={`border-b border-slate-200 hover:bg-slate-50/50 transition-colors ${i % 2 === 0 ? "bg-white" : "bg-slate-50/30"}`}>
                              <td className="px-4 py-3 font-mono text-xs font-bold text-blue-600">{r.NHTSACampaignNumber}</td>
                              <td className="px-4 py-3 text-xs text-slate-700">{r.Component}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

              </div>

              {/* ---- RIGHT: MARKETING SIDEBAR ---- */}
              <div className="space-y-6">

                {/* Sticky CTA */}
                <div className="lg:sticky lg:top-6">
                  <div className="overflow-hidden border border-blue-200 bg-white shadow-sm">
                    <div className="bg-blue-600 px-6 py-5 text-center">
                      <p className="text-[11px] font-bold uppercase tracking-widest text-blue-200">Plan Price Starting At</p>
                      <p className="mt-2 text-4xl font-extrabold text-white">${PLANS_FROM_USD}</p>
                      <p className="mt-1 text-sm text-blue-100">1–3 reports per plan</p>
                    </div>

                    <div className="px-6 py-5">
                      <p className="text-sm font-bold text-slate-900">Get the complete report including:</p>
                      <ul className="mt-4 space-y-3">
                        {[
                          { icon: "M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622", label: "Title History & Brands" },
                          { icon: "M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126z", label: "Accident & Damage Records" },
                          { icon: "M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z", label: "Ownership History" },
                          { icon: "M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z", label: "Odometer Readings" },
                          { icon: "M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z", label: "Theft Records" },
                          { icon: "M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085", label: "Service Records" },
                        ].map((item) => (
                          <li key={item.label} className="flex items-center gap-3">
                            <span className="flex h-8 w-8 shrink-0 items-center justify-center bg-emerald-100 text-emerald-600">
                              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                                <path d={item.icon} />
                              </svg>
                            </span>
                            <span className="text-sm font-medium text-slate-700">{item.label}</span>
                          </li>
                        ))}
                      </ul>

                      <Link
                        href={`/plans/${vin}`}
                        className="mt-6 flex w-full items-center justify-center gap-2 bg-blue-600 px-6 py-3.5 text-sm font-bold text-white shadow-md shadow-blue-600/20 transition-all hover:bg-blue-700 hover:shadow-lg"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
                          <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Buy a Plan &amp; Download
                      </Link>
                      <p className="mt-3 text-center text-[11px] text-slate-400">Instant download &middot; Secure payment via QuickBooks</p>
                    </div>
                  </div>

                  {/* Trust badges */}
                  <div className="mt-4 grid grid-cols-2 gap-3">
                    {[
                      { label: "NMVTIS Data", sub: "Official records" },
                      { label: "Instant PDF", sub: "Ready in seconds" },
                      { label: "No Signup", sub: "Buy as guest" },
                      { label: "Secure", sub: "SSL encrypted" },
                    ].map((badge) => (
                      <div key={badge.label} className="border border-slate-300 bg-white px-3 py-3 text-center">
                        <p className="text-[11px] font-bold text-slate-700">{badge.label}</p>
                        <p className="text-[10px] text-slate-400">{badge.sub}</p>
                      </div>
                    ))}
                  </div>
                </div>

              </div>

            </div>

          </>
        )}
      </main>
    </div>
  );
}

