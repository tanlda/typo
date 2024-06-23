import '@/styles/globals.scss'
import type { Metadata } from "next";
export const metadata: Metadata = {
  title: 'Microtypo',
  description: 'Microtypo Data Engineer Project',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="light">{children}</body>
    </html>
  );
}
