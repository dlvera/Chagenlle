from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate, 
    db: AsyncSession = Depends(get_db)): 
    
    # Verificar disponibilidad del username
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  # Mejor código para conflictos
            detail="Username already registered"
        )
    
    # Crear usuario con mejor manejo de errores
    try:
        new_user = User(username=user.username)
        new_user.set_password(user.password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
            headers={"X-Error": "UserCreationFailed"}
        )