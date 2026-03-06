import sqlite3
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "store.db"


def _conn():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = _conn()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL, -- 'user' | 'assistant'
        text TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        items TEXT NOT NULL,          -- JSON list
        status TEXT NOT NULL,         -- draft|checkout|confirmed|cancelled
        pickup_time TEXT,
        customer_name TEXT,
        customer_phone TEXT,
        flagged INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_state (
        session_id TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        context TEXT NOT NULL,  -- JSON
        updated_at TEXT NOT NULL
    );
    """)

    con.commit()
    con.close()


def now_iso():
    return datetime.utcnow().isoformat(timespec="seconds")


def log_message(session_id: str, role: str, text: str):
    con = _conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO messages(session_id, role, text, created_at) VALUES(?,?,?,?)",
        (session_id, role, text, now_iso())
    )
    con.commit()
    con.close()


def get_state(session_id: str) -> tuple[str, dict]:
    con = _conn()
    cur = con.cursor()
    row = cur.execute("SELECT state, context FROM user_state WHERE session_id=?", (session_id,)).fetchone()
    con.close()
    if not row:
        return "browsing", {}
    return row["state"], json.loads(row["context"])


def set_state(session_id: str, state: str, context: dict):
    con = _conn()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO user_state(session_id, state, context, updated_at)
    VALUES(?,?,?,?)
    ON CONFLICT(session_id) DO UPDATE SET
      state=excluded.state,
      context=excluded.context,
      updated_at=excluded.updated_at
    """, (session_id, state, json.dumps(context), now_iso()))
    con.commit()
    con.close()


def get_or_create_draft_order(session_id: str) -> dict:
    con = _conn()
    cur = con.cursor()
    row = cur.execute("""
        SELECT * FROM orders
        WHERE session_id=? AND status IN ('draft','checkout')
        ORDER BY id DESC LIMIT 1
    """, (session_id,)).fetchone()

    if row:
        con.close()
        return dict(row)

    ts = now_iso()
    cur.execute("""
        INSERT INTO orders(session_id, items, status, created_at, updated_at)
        VALUES(?,?,?,?,?)
    """, (session_id, json.dumps([]), "draft", ts, ts))
    con.commit()
    order_id = cur.lastrowid
    row2 = cur.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    con.close()
    return dict(row2)


def update_order(order_id: int, **fields):
    if not fields:
        return
    con = _conn()
    cur = con.cursor()

    fields["updated_at"] = now_iso()
    cols = ", ".join([f"{k}=?" for k in fields.keys()])
    vals = list(fields.values())
    vals.append(order_id)

    cur.execute(f"UPDATE orders SET {cols} WHERE id=?", vals)
    con.commit()
    con.close()


def get_order(order_id: int) -> dict | None:
    con = _conn()
    cur = con.cursor()
    row = cur.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    con.close()
    return dict(row) if row else None