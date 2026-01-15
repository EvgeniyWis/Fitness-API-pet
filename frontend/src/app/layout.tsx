import type { Metadata } from "next";
import "./globals.css";
import { MainLayout } from "@/widgets/layout/main-layout/ui";

export const metadata: Metadata = {
  title: "Fitness App",
  description: "Fitness app frontend",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body>
        <MainLayout>{children}</MainLayout>
      </body>
    </html>
  );
}
