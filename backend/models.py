from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 1. Define what a Comment looks like
class CommentModel(BaseModel):
    author: str
    text: str
    time: str = "Just now"

# 2. Add the comments list to the Post
class PostModel(BaseModel):
    author: str
    avatar: Optional[str] = ""
    text: str
    postImage: Optional[str] = ""
    time: str = "Just now"
    comments: List[CommentModel] = [] # NEW: Empty list by default
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserModel(BaseModel):
    name: str
    email: str
    role: str = "Professional Connection"
    avatar: str = ""

class MessageModel(BaseModel):
    sender: str
    receiver: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
