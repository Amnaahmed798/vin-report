"use client";

import { useEffect, useRef, useState } from "react";
import { getQuickBooksAuthUrl, pdfCheckout, type PdfCheckoutResult } from "@/lib/api";

export type CheckoutPlan = {
  id: string;
  name: string;
  price: number;
  reports: number;
};

type CheckoutModalProps = {
  vin: string;
  plan: CheckoutPlan | null;
  clientId: string | null;
  configured: boolean;
  env: string;
  open: boolean;
  onPaid: (result: PdfCheckoutResult, plan: CheckoutPlan) => void;
  onClose: () => void;
  onRefreshStatus: () => void;
};

declare global {
  interface Window {
    intuit?: {
      ipp?: {
        anywhere?: {
          setup: (opts: { clientId: string }) => Promise<unknown>;
          payments: {
            hostedFields: {
              create: (opts: {
                form: string;
                onTokenizeSuccess: (tokenize: { paymentToken?: string; token?: string }) => void;
                onTokenizeError: (error: { message?: string }) => void;
              }) => Promise<{
                attach: () => Promise<unknown>;
                detach: () => Promise<unknown>;
                tokenize: () => Promise<string | { paymentToken?: string; token?: string } | undefined>;
              }>;
            };
          };
        };
      };
    };
  }
}

const INTUIT_SDK_URL = "https://js.intuit.com/IntuitPayments/3.0.0/intuit-payments.js";

let sdkPromise: Promise<boolean> | null = null;

function loadIntuitSdk(onSdkUnavailable: () => void): Promise<boolean> {
  if (typeof window === "undefined") return Promise.resolve(false);
  if (window.intuit?.ipp?.anywhere) return Promise.resolve(true);
  if (sdkPromise) return sdkPromise;
  sdkPromise = new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = INTUIT_SDK_URL;
    script.async = true;
    script.onload = () => {
      if (window.intuit?.ipp?.anywhere) {
        resolve(true);
      } else {
        sdkPromise = null;
        onSdkUnavailable();
        resolve(false);
      }
    };
    script.onerror = () => {
      sdkPromise = null;
      onSdkUnavailable();
      resolve(false);
    };
    document.head.appendChild(script);
  });
  return sdkPromise;
}

type HostedFieldsInstance = {
  attach: () => Promise<unknown>;
  detach: () => Promise<unknown>;
  tokenize: () => Promise<string | { paymentToken?: string; token?: string } | undefined>;
};

type Phase = "loading" | "not-configured" | "unavailable" | "ready" | "paying";

export default function CheckoutModal({
  vin,
  plan,
  clientId,
  configured,
  env,
  open,
  onPaid,
  onClose,
  onRefreshStatus,
}: CheckoutModalProps) {
  const [phase, setPhase] = useState<Phase>("loading");
  const [error, setError] = useState<string | null>(null);
  const fieldsRef = useRef<HostedFieldsInstance | null>(null);
  const tokenRef = useRef<string>("");
  const formReadyRef = useRef(false);

  useEffect(() => {
    if (!open) return;
    formReadyRef.current = true;
    tokenRef.current = "";
    setError(null);
    setPhase("loading");

    if (!configured || !clientId) {
      setPhase("not-configured");
      return;
    }

    let cancelled = false;

    const init = async () => {
      const loaded = await loadIntuitSdk(() => {
        if (!cancelled) setPhase("unavailable");
      });
      if (cancelled || !loaded) return;

      try {
        const intuit = window.intuit?.ipp?.anywhere;
        if (!intuit) {
          if (!cancelled) setPhase("unavailable");
          return;
        }
        if (!formReadyRef.current) return;
        await intuit.setup({ clientId });
        if (cancelled || !formReadyRef.current) return;

        const fields = await intuit.payments.hostedFields.create({
          form: "#qb-checkout-form",
          onTokenizeSuccess: (tokenize) => {
            tokenRef.current = tokenize?.paymentToken ?? tokenize?.token ?? "";
          },
          onTokenizeError: (tokenizeError) => {
            if (!cancelled && formReadyRef.current) {
              setPhase("ready");
              setError(tokenizeError?.message || "Card details are invalid. Please check and try again.");
            }
          },
        });
        if (cancelled || !formReadyRef.current) return;
        await fields.attach();
        fieldsRef.current = fields;
        if (!cancelled) setPhase("ready");
      } catch (err) {
        console.error("Intuit.js hosted fields setup failed", err);
        if (!cancelled) setPhase("unavailable");
      }
    };

    init();

    return () => {
      cancelled = true;
      formReadyRef.current = false;
      fieldsRef.current?.detach?.().catch(() => undefined);
      fieldsRef.current = null;
    };
  }, [open, configured, clientId]);

  if (!open || !plan) return null;

  function resetAndClose() {
    fieldsRef.current?.detach?.().catch(() => undefined);
    fieldsRef.current = null;
    formReadyRef.current = false;
    onClose();
  }

  async function handlePay() {
    const fields = fieldsRef.current;
    if (!fields || phase !== "ready" || !plan) return;

    tokenRef.current = "";
    setPhase("paying");
    setError(null);

    let token = "";

    try {
      const raw = await fields.tokenize();
      if (typeof raw === "string") {
        token = raw;
      } else if (raw && typeof raw === "object") {
        token = raw.paymentToken ?? raw.token ?? "";
      }
      token = token || tokenRef.current;
      if (!token) throw new Error("Could not tokenize your card. Please try again.");

      const result = await pdfCheckout(vin, token, plan.id);
      onPaid(result, plan);
    } catch (err) {
      setPhase("ready");
      setError(err instanceof Error ? err.message : "Payment failed. Please try again.");
      fieldsRef.current?.detach?.().catch(() => undefined);
      fieldsRef.current = null;
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 p-4 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-label={`${plan.name} plan checkout`}
      onClick={(e) => {
        if (e.target === e.currentTarget) resetAndClose();
      }}
    >
      <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl sm:p-8">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Secure Checkout</p>
            <h2 className="mt-1 text-lg font-bold text-slate-900">
              {plan.name} Plan — ${plan.price}
            </h2>
            <p className="mt-0.5 text-xs text-slate-400">
              {plan.reports} vehicle report{plan.reports > 1 ? "s" : ""} · VIN{" "}
              <span className="font-mono font-semibold">{vin.slice(0, 8)}…</span>
            </p>
          </div>
          <button
            type="button"
            onClick={resetAndClose}
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 text-slate-400 transition-colors hover:bg-slate-50 hover:text-slate-600"
            aria-label="Close checkout"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
          </button>
        </div>

        {phase === "loading" && (
          <div className="flex flex-col items-center gap-3 py-12">
            <span className="h-8 w-8 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
            <p className="text-sm text-slate-500">Loading secure payment form…</p>
          </div>
        )}

        {phase === "not-configured" && (
          <div className="mt-6">
            {!clientId ? (
              <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                <p className="text-sm font-semibold text-amber-800">QuickBooks is not configured on the server</p>
                <p className="mt-1.5 text-xs leading-relaxed text-amber-700">
                  On the server that hosts this website, add the QuickBooks credentials to{" "}
                  <span className="font-mono">.env</span> and restart the backend:
                </p>
                <pre className="mt-2 overflow-x-auto rounded-lg bg-amber-100/70 p-3 font-mono text-[11px] leading-relaxed text-amber-900">
{`QB_CLIENT_ID=...
QB_CLIENT_SECRET=...
QB_ENV=sandbox
QB_REDIRECT_URI=https://your-domain/api/quickbooks/callback`}
                </pre>
              </div>
            ) : (
              <div className="rounded-xl border border-blue-200 bg-blue-50 p-4 text-center">
                <p className="text-sm font-semibold text-slate-800">One-time QuickBooks connection needed</p>
                <p className="mt-1.5 text-xs leading-relaxed text-slate-500">
                  The merchant must approve your app once so the server can charge cards.
                  Click below, sign in, and authorize — then check the connection.
                </p>
                <div className="mt-4 flex flex-col gap-2.5">
                  <a
                    href={getQuickBooksAuthUrl()}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#2CA01C] px-6 py-3 text-sm font-bold text-white shadow-md transition-all hover:brightness-110"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                      <path fillRule="evenodd" d="M12.232 4.232a3 3 0 014 4L7.5 16.923a5 5 0 01-7.05-.873.75.75 0 011.2-.9 3.5 3.5 0 004.91.612L6 15a.75.75 0 01.207-1.072L14 6z" clipRule="evenodd" />
                    </svg>
                    Connect QuickBooks
                  </a>
                  <button
                    type="button"
                    onClick={onRefreshStatus}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-6 py-2.5 text-sm font-bold text-blue-700 transition-all hover:bg-blue-50"
                  >
                    I&apos;ve connected — check again
                  </button>
                </div>
                <p className="mt-3 text-[11px] text-slate-400">
                  Environment: <span className="font-mono">{env || "sandbox"}</span>
                </p>
              </div>
            )}
          </div>
        )}

        {phase === "unavailable" && (
          <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4">
            <p className="text-sm font-semibold text-red-700">Secure payment form could not be loaded</p>
            <p className="mt-1 text-xs leading-relaxed text-red-600">
              The QuickBooks payment SDK failed to initialize (clientId:{" "}
              <span className="font-mono">{clientId ? `${clientId.slice(0, 6)}…` : "missing"}</span>).
              Please try again or contact support.
            </p>
          </div>
        )}

        {phase === "ready" && (
          <form id="qb-checkout-form" className="mt-6" onSubmit={(e) => e.preventDefault()}>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="mb-1.5 block text-xs font-semibold text-slate-600">Card Number</label>
                <div
                  data-intuit-payments-field="cardNumber"
                  className="h-11 rounded-xl border border-slate-300 bg-white px-3"
                />
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold text-slate-600">Expiration</label>
                <div
                  data-intuit-payments-field="expirationDate"
                  className="h-11 rounded-xl border border-slate-300 bg-white px-3"
                />
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold text-slate-600">CVC</label>
                <div
                  data-intuit-payments-field="cvc"
                  className="h-11 rounded-xl border border-slate-300 bg-white px-3"
                />
              </div>
              <div className="col-span-2">
                <label className="mb-1.5 block text-xs font-semibold text-slate-600">Postal Code</label>
                <div
                  data-intuit-payments-field="postalCode"
                  className="h-11 rounded-xl border border-slate-300 bg-white px-3"
                />
              </div>
            </div>

            <button
              type="button"
              onClick={handlePay}
              className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-bold text-white shadow-md shadow-blue-600/20 transition-all hover:bg-blue-700 hover:shadow-lg"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                <path d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clipRule="evenodd" />
              </svg>
              Pay ${plan.price}
            </button>
          </form>
        )}

        {phase === "paying" && (
          <div className="mt-6 flex flex-col items-center gap-3 py-8">
            <span className="h-8 w-8 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
            <p className="text-sm font-semibold text-slate-700">Processing payment…</p>
            <p className="text-xs text-slate-400">Please don&apos;t close this window.</p>
          </div>
        )}

        {error && phase === "ready" && (
            <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2.5">
              <p className="text-xs font-semibold text-red-700">{error}</p>
            </div>
          )}

        <div className="mt-6 flex items-center justify-center gap-1.5 border-t border-slate-100 pt-4">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4 text-blue-500">
            <path fillRule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clipRule="evenodd" />
          </svg>
          <p className="text-[11px] font-medium text-slate-400">
            Secured by QuickBooks · {env || "sandbox"}
          </p>
        </div>
      </div>
    </div>
  );
}