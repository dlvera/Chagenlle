from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

class PostBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=5)
    model_config = ConfigDict(from_attributes=True)
class PostCreate(PostBase):
    tags: List[int]
    # tags: List["TagRead"] 
    # model_config = ConfigDict(from_attributes=True)

class PostCreateResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    tags: List["TagRead"]
    model_config = ConfigDict(from_attributes=True)

class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    user: "UserRead"  # ✅
    comments: list["CommentRead"]  # ✅
    tags: list["TagRead"]
    model_config = ConfigDict(from_attributes=True)
    
if TYPE_CHECKING:
    from .tag import TagRead  # ✅ Importación diferida
    from .user import UserRead
    from .comment import CommentRead

