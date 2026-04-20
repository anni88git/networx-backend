import uuid
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 1. Added an invisible 'id' to Comments so we can target them for editing
class CommentModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: str
    text: str
    time: str = "Just now"

class PostModel(BaseModel):
    author: str
    avatar: Optional[str] = ""
    text: str
    postImage: Optional[str] = ""
    time: str = "Just now"
    comments: List[CommentModel] = []
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
