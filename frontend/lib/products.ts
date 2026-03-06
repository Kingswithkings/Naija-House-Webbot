// frontend/lib/products.ts

export type Product = {
  sku: string;
  name: string;
  price: number;
  unit: string;
  in_stock: number;
  aliases: string[];
  category: string;
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000";

export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch(`${API_BASE}/products`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Products API error: ${res.status}`);
  }

  const data = await res.json();

  return (data ?? []).map((p: any) => ({
    sku: p.sku,
    name: p.name,
    price: Number(p.price),
    unit: p.unit,
    in_stock: Number(p.in_stock),
    aliases: Array.isArray(p.aliases) ? p.aliases : [],
    category: p.category || "Uncategorized",
  }));
}