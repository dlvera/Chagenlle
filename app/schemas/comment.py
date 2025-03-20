from __future__ import annotations  # Para forward references
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from pydantic import Field

from app.schemas.post import PostRead



# Esquemas base comunes
class CommentBase(BaseModel):
    content: str = Field(..., min_length=2, max_length=500)

# Esquemas para creación
class CommentCreate(CommentBase):
    post_id: int

# Esquemas para respuesta
class CommentRead(CommentBase):
    id: int
    created_at: datetime
    # user: Optional["UserRead"]
    post: Optional[PostRead] = None
    model_config = ConfigDict(from_attributes=True)

