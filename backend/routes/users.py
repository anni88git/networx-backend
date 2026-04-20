from fastapi import APIRouter, Query
from database import db

router = APIRouter()

@router.get("/search")
def search_users(q: str = Query(...)):
    # Synchronous search and list conversion
    cursor = db.users.find({"name": {"$regex": q, "$options": "i"}}).limit(5)
    users = list(cursor)
    
    for user in users:
        user["_id"] = str(user["_id"])
    return users
