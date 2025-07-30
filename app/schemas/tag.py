from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING  # ✅ Añadir TYPE_CHECKING


# Esquemas base comunes
class TagBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)
    model_config = ConfigDict(from_attributes=True)
# Esquemas para creación
class TagCreate(BaseModel):
    name: str

    
class TagCreateResponse(TagBase):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Esquemas para respuesta
class TagRead(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # post: list["PostRead"]
    if TYPE_CHECKING:
        from .post import PostRead
        posts: list["PostRead"] = [] 
    model_config = ConfigDict(from_attributes=True)

if TYPE_CHECKING:
    from .post import PostRead  # ✅ Importación diferida

TagRead.model_rebuild()  # ✅ Reconstruir el modelo