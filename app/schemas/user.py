from __future__ import annotations
from typing import List
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from datetime import datetime
from app.schemas.post import PostRead
import re

# Esquemas base comunes
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

# Esquemas para creación
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=10)

    @field_validator('username')
    def validate_username(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError("Username can only contain letters, numbers and underscore")
        return value

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        errors = []
        if len(value) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r'[A-Z]', value):
            errors.append("La contraseña debe contener al menos una mayúscula")
        if not re.search(r'[0-9]', value):
            errors.append("La contraseña debe contener al menos un número")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            errors.append("La contraseña debe contener al menos un carácter especial")
        
        if errors:
            raise ValueError("\n".join(errors))
        
        return value
    
class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)   
    
# Esquemas para respuesta
class UserRead(UserBase):
    id: int
    created_at: datetime
    posts: List[PostRead] = []
    # comments: List["CommentRead"]
    model_config = ConfigDict(from_attributes=True) 
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

