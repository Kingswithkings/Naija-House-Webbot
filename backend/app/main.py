from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.db import init_db
from app.routes.chat import router as chat_router
from app.routes.products import router as products_router

app = FastAPI(title="Conversational Ordering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://global-food-webbot-cdaf.vercel.app",
        "https://naija-house-webbot.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    root = Path(__file__).resolve().parent
    return {
        "ok": True,
        "db_exists": (root / "store.db").exists(),
        "csv_exists": (root / "data" / "products.csv").exists(),
        "nlu_exists": (root / "app" / "nlu.py").exists(),
        "catalog_exists": (root / "app" / "catalog.py").exists(),
        "order_flow_exists": (root / "app" / "order_flow.py").exists(),
    }

app.include_router(products_router)
app.include_router(chat_router)

init_db()