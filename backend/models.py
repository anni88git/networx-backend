from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostModel(BaseModel):
    author: str
    avatar: Optional[str] = ""
    text: str
    postImage: Optional[str] = ""
    time: str = "Just now"
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