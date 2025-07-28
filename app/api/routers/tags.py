from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagCreateResponse, TagRead
from app.core.utils.security import get_current_user, get_db
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=TagCreateResponse)
async def create_tag(
    tags: TagCreate,
    # current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_tag = Tag(
        name=tags.name,
        # user_id=current_user.id
    )
    
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag

@router.get("/", response_model=List[TagRead])
async def read_tags(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Tag)
        .where(Tag.deleted_at == None)
        .options(selectinload(Tag.posts))  # ✅ Cargar posts relacionados
    )
    tags = result.scalars().all()
    return tags