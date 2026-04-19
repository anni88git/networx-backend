from fastapi import APIRouter, Query
from database import db
import re

# We define 'router' here to handle the routes for this file
router = APIRouter()

# CHANGED: @app.get is now @router.get
@router.get("/search")
async def search_users(q: str = Query(...)):
    # Simple regex search for your search bar
    cursor = db.users.find({"name": {"$regex": q, "$options": "i"}}).limit(5)
    users = await cursor.to_list(length=5)
    
    # Clean up the MongoDB _id for JSON
    for user in users:
        user["_id"] = str(user["_id"])
    return users