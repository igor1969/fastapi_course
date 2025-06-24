from sqlalchemy import select
from pydantic import EmailStr

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserWithHashed_password


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hased_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashed_password.model_validate(model)