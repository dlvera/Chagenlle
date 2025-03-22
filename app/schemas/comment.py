from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, TYPE_CHECKING

class CommentBase(BaseModel):
    content: str = Field(..., min_length=2, max_length=500)
    model_config = ConfigDict(from_attributes=True)
class CommentCreate(CommentBase):
    post_id: int
    # model_config = ConfigDict(from_attributes=True)
class CommentCreateResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime
    # post: "PostRead"  
    model_config = ConfigDict(from_attributes=True)
class CommentRead(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: "UserRead"  
    post: "PostRead"  
    model_config = ConfigDict(from_attributes=True)

if TYPE_CHECKING:
    from .post import PostRead
    from .user import UserRead

