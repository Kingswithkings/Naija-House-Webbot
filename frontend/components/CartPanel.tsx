import type { CartItem } from "../lib/api";

export default function CartPanel({ items, total, status }: { items: CartItem[]; total: number; status: string }) {
  return (
    <div style={{ background: "#111a2e", borderRadius: 14, padding: 16, height: "100%", border: "1px solid #1d2b4a" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
        <div style={{ fontWeight: 700 }}>Cart</div>
        <div style={{ fontSize: 12, opacity: 0.8 }}>{status}</div>
      </div>

      {items.length === 0 ? (
        <div style={{ opacity: 0.75 }}>Cart is empty.</div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {items.map((i) => (
            <div key={i.sku} style={{ padding: 10, borderRadius: 12, background: "#0b1324", border: "1px solid #1d2b4a" }}>
              <div style={{ fontWeight: 600 }}>{i.name}</div>
              <div style={{ fontSize: 12, opacity: 0.85 }}>
                Qty: {i.qty} • £{i.unit_price.toFixed(2)} each
              </div>
              <div style={{ marginTop: 6, fontWeight: 700 }}>£{i.line_total.toFixed(2)}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: 14, paddingTop: 12, borderTop: "1px solid #1d2b4a", display: "flex", justifyContent: "space-between" }}>
        <div style={{ fontWeight: 700 }}>Total</div>
        <div style={{ fontWeight: 900 }}>£{total.toFixed(2)}</div>
      </div>

      <div style={{ marginTop: 12, fontSize: 12, opacity: 0.8 }}>
        Tips: type <b>show cart</b>, <b>remove rice</b>, <b>checkout</b>
      </div>
    </div>
  );
}