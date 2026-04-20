from fastapi import APIRouter, HTTPException, status
from database import db
from models import PostModel
from bson import ObjectId
from typing import List
from pydantic import BaseModel

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_posts():
    try:
        cursor = db.posts.find().sort("created_at", -1).limit(100)
        posts = list(cursor)
        for post in posts:
            post["_id"] = str(post["_id"])
            if "comments" not in post:
                post["comments"] = []
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostModel):
    try:
        post_dict = post.model_dump()
        result = db.posts.insert_one(post_dict)
        return {"message": "Post created!", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")

@router.delete("/{post_id}")
def delete_post(post_id: str):
    try:
        delete_result = db.posts.delete_one({"_id": ObjectId(post_id)})
        if delete_result.deleted_count == 1:
            return {"message": "Post deleted successfully"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Post ID format")

class CommentInput(BaseModel):
    author: str
    text: str
    time: str = "Just now"

@router.post("/{post_id}/comment")
def add_comment(post_id: str, comment: CommentInput):
    try:
        import uuid
        comment_dict = comment.model_dump()
        comment_dict["id"] = str(uuid.uuid4()) # Force an ID here just in case
        
        result = db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"comments": comment_dict}}
        )
        if result.modified_count == 1:
            return {"message": "Comment added successfully"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")

# --- FEATURE 4: UPDATE POST ROUTE ---
class UpdateTextInput(BaseModel):
    text: str

@router.put("/{post_id}")
def update_post(post_id: str, data: UpdateTextInput):
    try:
        result = db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"text": data.text}}
        )
        if result.matched_count == 1:
            return {"message": "Post updated"}
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        # --- FEATURE 4: DELETE COMMENT ROUTE ---
@router.delete("/{post_id}/comment/{comment_id}")
def delete_comment(post_id: str, comment_id: str):
    try:
        # $pull completely removes the comment from the array
        result = db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"comments": {"id": comment_id}}}
        )
        if result.modified_count == 1:
            return {"message": "Comment deleted"}
        raise HTTPException(status_code=404, detail="Comment not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- FEATURE 4: UPDATE COMMENT ROUTE ---
@router.put("/{post_id}/comment/{comment_id}")
def update_comment(post_id: str, comment_id: str, data: UpdateTextInput):
    try:
        # The $ operator finds the exact comment in the array that matches the ID
        result = db.posts.update_one(
            {"_id": ObjectId(post_id), "comments.id": comment_id},
            {"$set": {"comments.$.text": data.text}}
        )
        if result.matched_count == 1:
            return {"message": "Comment updated"}
        raise HTTPException(status_code=404, detail="Comment not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
