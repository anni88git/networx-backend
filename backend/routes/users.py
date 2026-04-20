from fastapi import APIRouter, Query, HTTPException
from database import db
from bson import ObjectId

router = APIRouter()

@router.get("/search")
def search_users(q: str = Query(...)):
    # NO await here! Synchronous search.
    cursor = db.users.find({"name": {"$regex": q, "$options": "i"}}).limit(5)
    users = list(cursor)
    
    for user in users:
        user["_id"] = str(user["_id"])
    return users 

# --- FEATURE 2: CONNECT ROUTE ---
@router.post("/connect")
def send_connection(payload: dict):
    try:
        target_id = payload.get("targetId")
        if not target_id:
            raise HTTPException(status_code=400, detail="Missing target ID")

        # Updates the user in MongoDB so the connection request is saved
        result = db.users.update_one(
            {"_id": ObjectId(target_id)},
            {"$set": {"status": "Requested"}} 
        )
        return {"status": "success", "message": "Connection sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
