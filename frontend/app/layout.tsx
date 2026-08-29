import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Footer from "@/components/Footer";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Car Inspection Pro — Free Vehicle History Report",
  description:
    "Enter a VIN to get recalls, complaints, TSBs, safety ratings, and fuel economy data from official U.S. government sources.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <div className="flex flex-1 flex-col">{children}</div>
        <Footer />
        <noscript>
          <style>{".history-reveal{opacity:1;transform:none}.history-image{opacity:1;transform:none}"}</style>
        </noscript>
      </body>
    </html>
  );
}
