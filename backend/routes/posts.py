from fastapi import APIRouter, HTTPException, status
from database import db
from models import PostModel
from bson import ObjectId
from typing import List

router = APIRouter()

# 1. GET: Fetch all posts for the feed
@router.get("/", response_model=List[dict])
async def get_posts():
    try:
        # Fetching posts, sorted by newest first
        cursor = db.posts.find().sort("created_at", -1)
        posts = await cursor.to_list(length=100)
        
        # MongoDB uses _id (ObjectId), but frontend needs a string
        for post in posts:
            post["_id"] = str(post["_id"])
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. POST: Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostModel):
    try:
        # Pydantic v2 uses model_dump() instead of dict()
        post_dict = post.model_dump()
        result = await db.posts.insert_one(post_dict)
        
        return {"message": "Post created!", "id": str(result.inserted_id)}
    except Exception as e:
        # CRITICAL: This will now show us the EXACT error from MongoDB or Python
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")

# 3. DELETE: Remove a post
@router.delete("/{post_id}")
async def delete_post(post_id: str):
    try:
        delete_result = await db.posts.delete_one({"_id": ObjectId(post_id)})
        if delete_result.deleted_count == 1:
            return {"message": "Post deleted successfully"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Post ID format")