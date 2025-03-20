from __future__ import annotations  # Para forward references
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from pydantic import Field



# Esquemas base comunes
class TagBase(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=30)
    model_config = ConfigDict(from_attributes=True)

# Esquemas para creación
class TagCreate(BaseModel):
    name: str
    posts: Optional[List[int]] = None  # Lista de IDs de post
    
class TagCreateResponse(TagBase):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Esquemas para respuesta
class TagRead(TagBase):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
  
    # posts: List[PostRead] = []
    model_config = ConfigDict(from_attributes=True)