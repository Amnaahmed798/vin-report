import Link from "next/link";
import Navbar from "./Navbar";

export default function LegalPage({
  title,
  updated,
  children,
}: {
  title: string;
  updated: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <Navbar />
      <div className="flex flex-1 justify-center bg-white px-4 py-12">
        <article className="w-full max-w-3xl">
          <Link
            href="/"
            className="text-sm font-medium text-blue-600 transition hover:text-blue-700"
          >
            ← Back to VIN lookup
          </Link>
          <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
            {title}
          </h1>
          <p className="mt-1 text-sm text-slate-400">Last updated: {updated}</p>
          <div className="prose prose-slate mt-8 max-w-none text-sm leading-7 text-slate-700">
            {children}
          </div>
        </article>
      </div>
    </div>
  );
}
