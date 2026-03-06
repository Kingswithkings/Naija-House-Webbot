from fastapi import APIRouter
from pathlib import Path
from app.catalog import Catalog

router = APIRouter()

CATALOG = Catalog(csv_path=Path(__file__).resolve().parents[2] / "data" / "products.csv")

@router.get("/products")
def list_products():
    return [
        {
            "sku": p.sku,
            "name": p.name,
            "price": p.price,
            "unit": p.unit,
            "in_stock": p.in_stock,
            "aliases": p.aliases,
            "category": getattr(p, "category", None) or "Uncategorized",  # ✅ NEW
        }
        for p in CATALOG.products
    ]