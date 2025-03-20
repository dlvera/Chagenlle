from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagCreateResponse
from app.utils.security import get_current_user, get_db


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