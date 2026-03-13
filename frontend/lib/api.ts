// frontend/lib/api.ts

export type CartItem = {
  sku: string;
  name: string;
  qty: number;
  unit: string;
  unit_price: number;
  line_total: number;
};

export type ChatResponse = {
  reply: string;
  cart: null | { items: CartItem[]; total: number; status: string };
  needs_admin: boolean;
  order_id: number;
};

const API_BASE = (
  process.env.NEXT_PUBLIC_API_BASE ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000"
).replace(/\/$/, "");

export async function sendChat(
  sessionId: string,
  message: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
    cache: "no-store",
  });

  const raw = await res.text();

  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${raw}`);
  }

  const data = JSON.parse(raw);

  return {
    reply: data?.reply ?? "",
    cart: data?.cart ?? null,
    needs_admin: Boolean(data?.needs_admin),
    order_id: Number(data?.order_id ?? 0),
  };
}