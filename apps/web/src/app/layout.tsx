import type { Metadata } from "next";
import "../style.css";
export const metadata: Metadata = { title: "SonicLens — Hear your data", description: "Explore time-series data through grounded analysis and sound." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
