from fastapi import APIRouter, HTTPException, status
from database import db
from models import PostModel
from bson import ObjectId
from typing import List
from pydantic import BaseModel

router = APIRouter()

# 1. GET: Fetch all posts for the feed
@router.get("/", response_model=List[dict])
def get_posts():
    try:
        cursor = db.posts.find().sort("created_at", -1).limit(100)
        posts = list(cursor)
        
        for post in posts:
            post["_id"] = str(post["_id"])
            # Fallback for old posts that don't have a comments array yet
            if "comments" not in post:
                post["comments"] = []
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. POST: Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostModel):
    try:
        post_dict = post.model_dump()
        result = db.posts.insert_one(post_dict)
        return {"message": "Post created!", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")

# 3. DELETE: Remove a post
@router.delete("/{post_id}")
def delete_post(post_id: str):
    try:
        delete_result = db.posts.delete_one({"_id": ObjectId(post_id)})
        if delete_result.deleted_count == 1:
            return {"message": "Post deleted successfully"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Post ID format")

# 4. POST: Add a comment to a specific post
class CommentInput(BaseModel):
    author: str
    text: str
    time: str = "Just now"

@router.post("/{post_id}/comment")
def add_comment(post_id: str, comment: CommentInput):
    try:
        # $push safely adds the comment to the array inside the specific post
        result = db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"comments": comment.model_dump()}}
        )
        if result.modified_count == 1:
            return {"message": "Comment added successfully"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")
