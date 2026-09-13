"use client";

import { useState } from "react";
import Link from "next/link";
import Navbar from "./Navbar";

export type LegalSection = {
  id: string;
  label: string;
};

export default function LegalPage({
  title,
  updated,
  intro,
  sections,
  children,
}: {
  title: string;
  updated: string;
  intro: string;
  sections: LegalSection[];
  children: React.ReactNode;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <Navbar />
      <main className="flex-1 bg-white">
        {/* Hero band */}
        <div className="border-b border-slate-100 bg-slate-50">
          <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-600 transition hover:text-blue-700"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                <path fillRule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clipRule="evenodd" />
              </svg>
              Back to VIN Lookup
            </Link>
            <h1 className="mt-4 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
              {title}
            </h1>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-500">{intro}</p>
            <p className="mt-4 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-500">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-3.5 w-3.5 text-blue-500">
                <path d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clipRule="evenodd" />
              </svg>
              Last Updated: {updated}
            </p>
          </div>
        </div>

        {/* Content: sidebar TOC + main */}
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-[260px_1fr] lg:gap-12">
            {/* Mobile "On this page" nav */}
            <div className="lg:hidden">
              <button
                type="button"
                onClick={() => setMobileOpen((o) => !o)}
                aria-expanded={mobileOpen}
                aria-controls="legal-toc-mobile"
                className="flex w-full items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-bold text-slate-700"
              >
                <span>On this page</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  className={`h-4 w-4 text-slate-400 transition-transform ${mobileOpen ? "rotate-180" : ""}`}
                >
                  <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
                </svg>
              </button>
              {mobileOpen && (
                <nav id="legal-toc-mobile" className="mt-2 rounded-xl border border-slate-200 bg-white p-2">
                  {sections.map((s) => (
                    <a
                      key={s.id}
                      href={`#${s.id}`}
                      onClick={() => setMobileOpen(false)}
                      className="block rounded-lg px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-blue-600"
                    >
                      {s.label}
                    </a>
                  ))}
                </nav>
              )}
            </div>

            {/* Desktop sticky sidebar TOC */}
            <aside className="hidden lg:block">
              <nav className="sticky top-8 rounded-2xl border border-slate-200 bg-slate-50 p-5">
                <p className="mb-3 text-xs font-bold uppercase tracking-wider text-slate-500">
                  On this page
                </p>
                <ol className="list-inside list-decimal space-y-2 text-[13px] leading-5 text-slate-600 marker:text-slate-300">
                  {sections.map((s) => (
                    <li key={s.id}>
                      <a href={`#${s.id}`} className="transition hover:text-blue-600">
                        {s.label}
                      </a>
                    </li>
                  ))}
                </ol>
              </nav>
            </aside>

            {/* Main content */}
            <div className="mt-8 lg:mt-0">
              <div className="legal-prose max-w-full text-[15px] leading-7 text-slate-700">
                {children}
              </div>

              {/* Back to top */}
              <div className="mt-14 border-t border-slate-200 pt-8">
                <a
                  href="#"
                  className="inline-flex items-center gap-1.5 text-sm font-semibold text-blue-600 hover:text-blue-700"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                    <path fillRule="evenodd" d="M10 18a.75.75 0 01-.75-.75V6.31l-4.22 4.22a.75.75 0 11-1.06-1.06l5.5-5.5a.75.75 0 011.06 0l5.5 5.5a.75.75 0 11-1.06 1.06l-4.22-4.22v10.94A.75.75 0 0110 18z" clipRule="evenodd" />
                  </svg>
                  Back to top
                </a>
              </div>

              {/* Footer note */}
              <div className="mt-8 pb-4 text-center">
                <p className="text-xs text-slate-400">
                  &copy; {new Date().getFullYear()} Car Inspection Pro. All rights reserved.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}