from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path

from app.db import log_message
from app.catalog import Catalog
from app.order_flow import handle_chat

router = APIRouter()

CATALOG = Catalog(csv_path=Path(__file__).resolve().parents[2] / "data" / "products.csv")

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    log_message(req.session_id, "user", req.message)
    result = handle_chat(req.session_id, req.message, CATALOG)
    log_message(req.session_id, "assistant", result["reply"])
    return result