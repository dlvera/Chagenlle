from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        # Verificar si el usuario ya existe
        if await self.repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de usuario ya está registrado"
            )
        
        # Crear nuevo usuario
        user = await self.repository.create(user_data)
        return UserInDB(
            id=user.id,
            username=user.username,
            created_at=user.created_at
        )