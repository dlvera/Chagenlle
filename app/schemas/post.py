from __future__ import annotations  # Para forward references
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from pydantic import Field

from app.schemas.tag import TagRead

# Esquemas base comunes
class PostBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=5)

# Esquemas para creación
class PostCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[int]] = None  # Lista de IDs de tags
    
class PostCreateResponse(PostBase):
    id: int
    user_id:int
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead]
    model_config = ConfigDict(from_attributes=True)

# Esquemas para respuesta
class PostRead(PostBase):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id:int
    # user: Optional[UserRead] = None
    # comments: List[CommentRead] = []
    tags: List[TagRead]
    model_config = ConfigDict(from_attributes=True)
