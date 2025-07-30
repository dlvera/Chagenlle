from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.schemas.user import UserCreate, UserInDB, UserResponse
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError

from app.services.user_service import UserService

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
    
@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    try:
        return await service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))