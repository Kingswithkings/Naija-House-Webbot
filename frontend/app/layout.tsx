import "./globals.css";

export const metadata = {
  title: "Naija House — Chat Order",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}