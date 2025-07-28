from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        if await self.repository.get_by_email(user_data.email):
            raise ValueError("Email already registered")
        
        user = await self.repository.create(user_data)
        return UserInDB.model_validate(user)