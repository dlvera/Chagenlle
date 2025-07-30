from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserInDB
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username))
        return result.scalars().first()
     
    async def create(self, user_data: UserCreate) -> User:
        user = User(username=user_data.username)
        user.set_password(user_data.password)
        self.session.add(user)
        await self.session.commit()
        return user