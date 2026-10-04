"use client";

import { use, useEffect, useState, useCallback } from "react";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import { fetchVinDecode, paypalCheckout, type VinDecode } from "@/lib/api";

type Plan = {
  id: string;
  name: string;
  price: number;
  reports: number;
  badge?: string;
  color: string;
  features: string[];
  locked: string[];
};

const PLAN_PRICE_BASIC = Number(process.env.NEXT_PUBLIC_PLAN_PRICE_BASIC ?? 3);
const PLAN_PRICE_GOLD = Number(process.env.NEXT_PUBLIC_PLAN_PRICE_GOLD ?? 65);
const PLAN_PRICE_PREMIUM = Number(process.env.NEXT_PUBLIC_PLAN_PRICE_PREMIUM ?? 85);

const PLANS: Plan[] = [
  {
    id: "basic",
    name: "Basic",
    price: PLAN_PRICE_BASIC,
    reports: 1,
    color: "blue",
    features: [
      "Accident & Damage Records",
      "Title History & Brands",
      "Ownership History",
      "Odometer Check",
      "Service Records",
      "Theft Records",
      "Recall Check",
      "Safety Rating",
      "Fuel Economy",
      "TSB Count",
      "Downloadable PDF",
    ],
    locked: [],
  },
  {
    id: "gold",
    name: "Gold",
    price: PLAN_PRICE_GOLD,
    reports: 2,
    badge: "Most Popular",
    color: "blue",
    features: [
      "Accident & Damage Records",
      "Title History & Brands",
      "Ownership History",
      "Odometer Check",
      "Service Records",
      "Theft Records",
      "Recall Check",
      "Safety Rating",
      "Fuel Economy",
      "TSB Count",
      "Downloadable PDF",
    ],
    locked: [],
  },
  {
    id: "premium",
    name: "Premium",
    price: PLAN_PRICE_PREMIUM,
    reports: 3,
    badge: "Best Value",
    color: "blue",
    features: [
      "Accident & Damage Records",
      "Title History & Brands",
      "Ownership History",
      "Odometer Check",
      "Service Records",
      "Theft Records",
      "Recall Check",
      "Safety Rating",
      "Fuel Economy",
      "TSB Count",
      "Downloadable PDF",
    ],
    locked: [],
  },
];

const COLOR_MAP: Record<string, { ring: string; bg: string; text: string; btn: string; badge: string }> = {
  blue: {
    ring: "border-blue-500 ring-2 ring-blue-500/20",
    bg: "bg-blue-50",
    text: "text-blue-900",
    btn: "bg-blue-600 hover:bg-blue-700",
    badge: "bg-blue-100 text-blue-700",
  },
};

function SpecCell({ label, value }: { label: string; value?: string }) {
  if (!value) return null;
  return (
    <div className="flex flex-col gap-0.5 py-2.5 sm:flex-row sm:items-baseline sm:justify-between sm:gap-4">
      <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{label}</span>
      <span className="text-sm font-semibold text-slate-800 sm:text-right">{value}</span>
    </div>
  );
}

export default function PlansPage({ params }: { params: Promise<{ vin: string }> }) {
  const { vin: rawVin } = use(params);
  const vin = decodeURIComponent(rawVin).toUpperCase();

  const [vehicle, setVehicle] = useState<VinDecode["vehicle"] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [checkoutPlanId, setCheckoutPlanId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchVinDecode(vin)
      .then((r) => {
        if (!cancelled) setVehicle(r.vehicle);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to decode VIN");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [vin]);

  const copyVin = useCallback(() => {
    navigator.clipboard.writeText(vin).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }, [vin]);

  function handleBuyNow(plan: Plan) {
    if (checkoutPlanId) return;
    setCheckoutPlanId(plan.id);
    paypalCheckout(vin, plan.id)
      .then((res) => {
        window.location.href = res.approve_url;
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Could not start checkout. Please try again.");
        setCheckoutPlanId(null);
      });
  }

  const vehicleLabel = vehicle
    ? `${vehicle.ModelYear} ${vehicle.Make} ${vehicle.Model}${vehicle.Trim ? ` ${vehicle.Trim}` : ""}`
    : null;

  const subtitleParts = vehicle
    ? [vehicle.Make, vehicle.Model, vehicle.Trim].filter(Boolean)
    : [];

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <Navbar />
      <main className="mx-auto w-full max-w-5xl px-4 py-10 sm:px-6 lg:px-8">

        {/* ===================================================
            LOADING / ERROR
        =================================================== */}
        {loading && (
          <div className="flex flex-col items-center gap-3 py-24">
            <span className="h-8 w-8 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
            <p className="text-sm text-slate-500">Decoding VIN…</p>
          </div>
        )}

        {error && (
          <div className="mx-auto max-w-md rounded-xl border border-red-200 bg-red-50 p-8 text-center">
            <p className="text-sm font-semibold text-red-600">{error}</p>
            <Link href="/" className="mt-4 inline-block text-sm font-bold text-blue-600 hover:underline">
              Try another VIN
            </Link>
          </div>
        )}

        {vehicle && !loading && !error && (
          <>
            {/* ===================================================
                VEHICLE IDENTIFIED HEADER
            =================================================== */}
            <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 px-6 py-4 sm:px-8">
                <div className="flex items-center gap-2.5">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-3.5 w-3.5">
                      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Vehicle Identified</span>
                </div>
                <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-[11px] font-bold text-emerald-700">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-3 w-3">
                    <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                  </svg>
                  VIN DECODED
                </span>
              </div>

              <div className="px-6 py-6 sm:px-8">
                <h1 className="text-[28px] font-extrabold leading-tight text-slate-900 sm:text-[32px]">
                  {vehicleLabel}
                </h1>
                {subtitleParts.length > 0 && (
                  <p className="mt-1 text-sm text-slate-500">{subtitleParts.join(" · ")}</p>
                )}

                {/* VIN Copy Box */}
                <div className="mt-5 inline-flex w-full max-w-md items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 px-5 py-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">VIN</p>
                    <p className="mt-0.5 break-all font-mono text-base font-bold tracking-[0.1em] text-slate-900">{vin}</p>
                  </div>
                  <button
                    type="button"
                    onClick={copyVin}
                    className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-700"
                    title="Copy VIN"
                  >
                    {copied ? (
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4 text-emerald-500">
                        <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                        <path d="M7 3.5A1.5 1.5 0 018.5 2h3.879a1.5 1.5 0 011.06.44l3.122 3.12A1.5 1.5 0 0117 6.622V12.5a1.5 1.5 0 01-1.5 1.5h-1v-3.379a3 3 0 00-.879-2.121L10.5 5.379A3 3 0 008.379 4.5H7v-1z" />
                        <path d="M4.5 6A1.5 1.5 0 003 7.5v9A1.5 1.5 0 004.5 18h7a1.5 1.5 0 001.5-1.5v-5.879a1.5 1.5 0 00-.44-1.06L9.44 6.439A1.5 1.5 0 008.378 6H4.5z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* ===================================================
                SPECIFICATIONS + DATA AVAILABLE SIDE BY SIDE
            =================================================== */}
            <div className="mt-6 grid gap-6 lg:grid-cols-[1.6fr_1fr]">
              {/* Vehicle Specifications Table */}
              <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
                <div className="border-b border-slate-100 px-6 py-4 sm:px-8">
                  <h2 className="text-sm font-bold text-slate-900">Vehicle Specifications</h2>
                  <p className="mt-0.5 text-xs text-slate-400">Decoded from NHTSA vPIC database</p>
                </div>

                <div className="px-6 sm:px-8">
                  {/* Vehicle Identity */}
                  <div className="border-b border-slate-100 py-4">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Vehicle Identity</p>
                    <div className="grid grid-cols-2 gap-x-6">
                      <SpecCell label="Year" value={vehicle.ModelYear} />
                      <SpecCell label="Make" value={vehicle.Make} />
                      <SpecCell label="Model" value={vehicle.Model} />
                      <SpecCell label="Trim" value={vehicle.Trim} />
                      <SpecCell label="Body Class" value={vehicle.BodyClass} />
                      <SpecCell label="Doors" value={vehicle.Doors ? `${vehicle.Doors}-Door` : undefined} />
                      <SpecCell label="Vehicle Type" value={vehicle.VehicleType} />
                      <SpecCell label="Series" value={vehicle.Series} />
                    </div>
                  </div>

                  {/* Engine & Fuel */}
                  <div className="border-b border-slate-100 py-4">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Engine & Fuel</p>
                    <div className="grid grid-cols-2 gap-x-6">
                      <SpecCell label="Engine" value={
                        vehicle.DisplacementL ? `${vehicle.DisplacementL}L${vehicle.EngineHP ? ` ${vehicle.EngineHP}HP` : ""}` : undefined
                      } />
                      <SpecCell label="Cylinders" value={vehicle.EngineCylinders} />
                      <SpecCell label="Fuel Type" value={vehicle.FuelTypePrimary} />
                      <SpecCell label="Drive Type" value={vehicle.DriveType} />
                      <SpecCell label="Transmission" value={vehicle.TransmissionStyle} />
                    </div>
                  </div>

                  {/* Manufacturing */}
                  <div className="py-4">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Manufacturing</p>
                    <div className="grid grid-cols-2 gap-x-6">
                      <SpecCell label="Manufacturer" value={vehicle.ManufacturerName} />
                      <SpecCell label="Plant" value={vehicle.PlantCity} />
                      <SpecCell label="Plant State" value={vehicle.PlantState} />
                      <SpecCell label="Plant Country" value={vehicle.PlantCountry} />
                    </div>
                  </div>
                </div>
              </div>

              {/* Data Available */}
              <div className="rounded-2xl border border-slate-200 bg-white shadow-sm px-6 py-5 sm:px-8">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-3">Data Available for This Vehicle</p>
                <div className="space-y-2.5">
                  {[
                    { label: "Recalls", desc: "NHTSA recall campaigns" },
                    { label: "Safety Ratings", desc: "Crash test ratings" },
                    { label: "Complaints", desc: "Consumer complaints" },
                    { label: "Fuel Economy", desc: "EPA fuel economy data" },
                    { label: "Technical Service Bulletins", desc: "Manufacturer TSBs" },
                    { label: "Investigations", desc: "NHTSA investigations" },
                  ].map((item) => (
                    <div key={item.label} className="flex items-center gap-3 rounded-xl border border-blue-100 bg-blue-50/50 px-4 py-3">
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-3 w-3">
                          <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                        </svg>
                      </span>
                      <div>
                        <p className="text-sm font-semibold text-slate-800">{item.label}</p>
                        <p className="text-[11px] text-slate-400">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-5 rounded-xl border border-blue-200 bg-blue-600 px-4 py-3">
                  <p className="text-xs font-semibold text-white">Unlock the full history</p>
                  <p className="mt-0.5 text-[11px] leading-relaxed text-blue-100">
                    Get accident records, title history, ownership details, and more with a paid report.
                  </p>
                </div>
              </div>
            </div>

            {/* ===================================================
                CHOOSE YOUR REPORT
            =================================================== */}
            <div className="mt-10 mb-6 text-center">
              <h2 className="text-2xl font-extrabold text-slate-900">Choose Your Vehicle Report</h2>
              <p className="mt-2 text-sm text-slate-500">
                Get detailed information about this vehicle
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
              {PLANS.map((plan) => {
                const c = COLOR_MAP[plan.color];
                return (
                  <div
                  key={plan.id}
                  className="relative flex flex-col rounded-2xl border border-blue-100 bg-white text-left shadow-sm transition-all hover:border-blue-200 hover:shadow-md"
                >
                    {plan.badge && (
                      <div className={`absolute -top-3 left-1/2 -translate-x-1/2 rounded-full px-4 py-1 text-[11px] font-bold uppercase tracking-wider ${c.badge}`}>
                        {plan.badge}
                      </div>
                    )}

                    <div className={`rounded-t-2xl px-6 pt-7 pb-5 text-center ${c.bg}`}>
                      <p className="text-sm font-bold text-slate-500">{plan.name} Plan</p>
                      <p className={`mt-2 text-4xl font-extrabold ${c.text}`}>${plan.price}</p>
                      <p className="mt-1 text-xs text-slate-400">
                        {plan.reports} report{plan.reports > 1 ? "s" : ""} — ${Math.round(plan.price / plan.reports)} each
                      </p>
                    </div>

                    <div className="flex flex-1 flex-col px-6 pb-6 pt-5">
                      <ul className="flex-1 space-y-3">
                        {plan.features.map((f) => (
                          <li key={f} className="flex items-start gap-2.5">
                            <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-3 w-3">
                                <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                              </svg>
                            </span>
                            <span className="text-sm font-medium text-slate-700">{f}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="border-t border-slate-100 p-4">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleBuyNow(plan);
                        }}
                        disabled={checkoutPlanId !== null}
                        className="w-full rounded-xl bg-blue-600 py-3 text-sm font-bold text-white shadow-md shadow-blue-600/20 transition-all hover:bg-blue-700 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-70"
                      >
                        {checkoutPlanId === plan.id ? (
                          <span className="inline-flex items-center justify-center gap-2">
                            <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                            Opening secure checkout…
                          </span>
                        ) : (
                          "Buy Now"
                        )}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Checkout note */}
            <div className="mt-6">
              <p className="text-center text-xs text-slate-400">
                Secure checkout powered by PayPal — pay on PayPal&apos;s hosted page, then download your report
              </p>
            </div>

            {/* Trust Footer */}
            <div className="mt-10 flex flex-wrap items-center justify-center gap-6 text-xs text-slate-400">
              <span className="flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4 text-emerald-500">
                  <path fillRule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clipRule="evenodd" />
                </svg>
                Secure payment via PayPal
              </span>
              <span>No account required</span>
              <span>Instant PDF download</span>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
