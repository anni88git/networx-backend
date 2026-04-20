from fastapi import APIRouter, HTTPException
from database import db
from typing import List

router = APIRouter()

# 1. SEND: Save a new message
@router.post("/send")
def send_message(msg: dict): 
    try:
        # Synchronous insert
        result = db.messages.insert_one(msg)
        return {"status": "sent", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. HISTORY: Get chat between two users
@router.get("/history/{u1}/{u2}")
def get_history(u1: str, u2: str):
    try:
        query = {
            "$or": [
                {"sender": u1, "receiver": u2},
                {"sender": u2, "receiver": u1}
            ]
        }
        # Synchronous find and list conversion
        cursor = db.messages.find(query).sort("timestamp", 1).limit(100)
        messages = list(cursor)
        for m in messages:
            m["_id"] = str(m["_id"])
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
