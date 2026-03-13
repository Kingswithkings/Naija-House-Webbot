from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import traceback

from app.db import log_message
from app.catalog import Catalog
from app.order_flow import handle_chat

router = APIRouter()

CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "products.csv"
CATALOG = Catalog(csv_path=CATALOG_PATH)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        print(f"CHAT REQUEST: session_id={req.session_id}, message={req.message}")
        print(f"CATALOG PATH: {CATALOG_PATH}")
        print(f"CATALOG EXISTS: {CATALOG_PATH.exists()}")

        log_message(req.session_id, "user", req.message)
        result = handle_chat(req.session_id, req.message, CATALOG)
        log_message(req.session_id, "assistant", result.get("reply", ""))

        return result

    except Exception as e:
        print("CHAT ERROR:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"CHAT ERROR: {repr(e)}")