"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { capturePdf } from "@/lib/api";
import Navbar from "@/components/Navbar";

function PayContent() {
  const params = useParams<{ vin: string }>();
  const vin = decodeURIComponent(params?.vin ?? "");
  const search = useSearchParams();
  const token = search.get("token");

  const [status, setStatus] = useState<"working" | "done" | "error">(
    vin && token ? "working" : "error",
  );
  const [message, setMessage] = useState(
    vin && token
      ? "Verifying payment…"
      : "No payment token found. The payment may have been cancelled.",
  );

  useEffect(() => {
    if (!vin || !token) return;
    let cancelled = false;
    (async () => {
      try {
        const blob = await capturePdf(vin, token);
        if (cancelled) return;
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${vin}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 30000);
        setStatus("done");
        setMessage("Payment successful — your report is downloading.");
      } catch (err) {
        if (cancelled) return;
        setStatus("error");
        setMessage(err instanceof Error ? err.message : "Could not process the download.");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [vin, token]);

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <Navbar />
      <main className="mx-auto flex w-full max-w-xl flex-1 items-center justify-center px-4 py-20">
        <div className="w-full rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50">
            {status === "working" && (
              <span className="h-6 w-6 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
            )}
            {status === "done" && (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-7 w-7 text-emerald-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            )}
            {status === "error" && (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-7 w-7 text-rose-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
                />
              </svg>
            )}
          </div>

          <h1 className="mt-5 text-xl font-bold text-slate-900">
            {status === "working" && "Processing payment"}
            {status === "done" && "Payment complete"}
            {status === "error" && "Download unavailable"}
          </h1>

          <p className="mt-2 text-sm leading-relaxed text-slate-500">{message}</p>

          <Link
            href={`/report/${vin}`}
            className="mt-6 inline-flex items-center justify-center rounded-full bg-slate-950 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-600"
          >
            Back to report
          </Link>
        </div>
      </main>
    </div>
  );
}

export default function PayPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen flex-col bg-slate-50">
          <Navbar />
          <main className="flex flex-1 items-center justify-center px-4">
            <span className="h-8 w-8 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
          </main>
        </div>
      }
    >
      <PayContent />
    </Suspense>
  );
}
