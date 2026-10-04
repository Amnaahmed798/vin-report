"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import { downloadBlob, paypalCapture, paypalDownload, paypalOrderStatus } from "@/lib/api";

const POLL_INTERVAL_MS = 2500;
const POLL_TIMEOUT_MS = 120000;

function ThankYouBody() {
  const params = useSearchParams();
  const vin = params.get("vin") ?? "";
  const orderId = params.get("order") ?? "";
  const planName = params.get("name") ?? "";
  const planPrice = params.get("price") ?? "";

  const [payable, setPayable] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [orderError, setOrderError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);
  const [downloadDone, setDownloadDone] = useState(false);
  const startedAtRef = useRef<number | null>(null);

  useEffect(() => {
    if (!orderId) return;
    startedAtRef.current = Date.now();
    setConfirming(true);

    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;

    const poll = async () => {
      if (cancelled) return;
      try {
        const status = await paypalOrderStatus(orderId);
        if (cancelled) return;
        if (status.status === "paid") {
          setPayable(true);
          setConfirming(false);
          return;
        }
      } catch {
        if (cancelled) return;
        setOrderError(null);
      }

      if (Date.now() - (startedAtRef.current ?? 0) > POLL_TIMEOUT_MS) {
        setConfirming(false);
        setOrderError(
          "We're still waiting for PayPal to confirm your payment. It usually takes a few seconds — check back shortly.",
        );
        return;
      }
      timer = setTimeout(poll, POLL_INTERVAL_MS);
    };

    const tryCapture = async () => {
      if (cancelled) return;
      try {
        const status = await paypalCapture(orderId);
        if (cancelled) return;
        if (status.status === "paid") {
          setPayable(true);
          setConfirming(false);
          return;
        }
      } catch {
        // Buyer may not have approved yet — fall through to polling.
      }
      poll();
    };

    tryCapture();

    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [orderId]);

  async function handleDownload() {
    if (!orderId || downloading || !payable) return;
    setDownloading(true);
    setDownloadError(null);
    try {
      const blob = await paypalDownload(orderId);
      const filename = vin ? `${vin}.pdf` : "vehicle-report.pdf";
      downloadBlob(blob, filename);
      setDownloadDone(true);
    } catch (err) {
      setDownloadError(err instanceof Error ? err.message : "Download failed. Please try again.");
    } finally {
      setDownloading(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <Navbar />
      <main className="mx-auto flex w-full max-w-xl flex-1 items-center justify-center px-4 py-20">
        <div className="w-full rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-7 w-7 text-emerald-500">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
            </svg>
          </div>

          <h1 className="mt-5 text-xl font-bold text-slate-900">
            {orderId ? (payable ? "Payment Successful — Thank You!" : "Thank You!") : "Thank You"}
          </h1>

          {(vin || planName) && (
            <div className="mt-4 rounded-lg bg-slate-50 p-4">
              {vin && (
                <p className="text-sm text-slate-500">
                  VIN: <span className="font-mono font-semibold text-slate-700">{vin}</span>
                </p>
              )}
              {planName && (
                <p className="mt-1 text-sm text-slate-500">
                  Plan: <span className="font-semibold text-slate-700">{planName}{planPrice ? ` ($${planPrice})` : ""}</span>
                </p>
              )}
            </div>
          )}

          {orderId && confirming && (
            <>
              <div className="mt-6 flex flex-col items-center gap-3">
                <span className="h-8 w-8 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
                <p className="text-sm leading-relaxed text-slate-500">
                  Confirming your payment with PayPal…
                </p>
              </div>
            </>
          )}

          {orderId && payable && (
            <>
              <p className="mt-4 text-sm leading-relaxed text-slate-500">
                Your payment was confirmed and your vehicle history report is ready.
              </p>

              <button
                type="button"
                onClick={handleDownload}
                disabled={downloading}
                className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3 text-sm font-bold text-white shadow-md shadow-blue-600/20 transition-all hover:bg-blue-700 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-70"
              >
                {downloading ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                    Preparing your report…
                  </>
                ) : downloadDone ? (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-7.25 9.5a.75.75 0 01-1.13.05l-4.25-4.5a.75.75 0 111.09-1.03l3.65 3.864 6.738-8.832a.75.75 0 011.009-.104z" clipRule="evenodd" />
                    </svg>
                    Downloaded — check your downloads
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                    Download Your Report
                  </>
                )}
              </button>

              {downloading && (
                <p className="mt-3 text-xs leading-relaxed text-slate-500">
                  The first download generates your report, which can take up to 2 minutes. Please keep this tab open.
                </p>
              )}

              {downloadError && (
                <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2.5">
                  <p className="text-xs font-semibold text-red-700">{downloadError}</p>
                  <p className="mt-1 text-[11px] text-red-600">
                    If this keeps happening, refresh the page in a moment and try again.
                  </p>
                </div>
              )}

              <p className="mt-4 text-xs leading-relaxed text-slate-400">
                Your download link stays active for a while after your purchase.
              </p>
            </>
          )}

          {orderId && !confirming && !payable && orderError && (
            <div className="mt-5 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2.5">
              <p className="text-xs font-semibold text-amber-800">{orderError}</p>
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="mt-2 inline-block text-xs font-bold text-blue-600 hover:underline"
              >
                Refresh
              </button>
            </div>
          )}

          {!orderId && (
            <p className="mt-4 text-sm leading-relaxed text-slate-500">
              We couldn&apos;t find an order linked to this page. If you just made a purchase,
              go back and try again.
            </p>
          )}

          <Link
            href="/"
            className="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-bold text-slate-700 transition-all hover:bg-slate-50"
          >
            Back to Home
          </Link>
        </div>
      </main>
    </div>
  );
}

export default function ThankYouPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen flex-col bg-slate-50">
          <Navbar />
          <main className="mx-auto flex w-full max-w-xl flex-1 items-center justify-center px-4 py-20">
            <div className="flex flex-col items-center gap-3">
              <span className="h-8 w-8 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
              <p className="text-sm text-slate-500">Loading…</p>
            </div>
          </main>
        </div>
      }
    >
      <ThankYouBody />
    </Suspense>
  );
}