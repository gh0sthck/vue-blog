from sqlalchemy import Select
from sqlalchemy.ext.asyncio.session import AsyncSession


from users.models import User
from users.schemas import SUser, SUserService
from repository import Repository


class UsersRepository(Repository):
    def __init__(self):
        super().__init__(User, SUserService)

    @Repository._session
    async def get_by_usernmae(
        self, username: str, withpass: bool = False, _session: AsyncSession = ...
    ) -> SUserService | SUser | None:
        q = Select(self.model).where(self.model.username == username)
        r = await _session.execute(q)
        pre_result = r.scalar_one_or_none()
        if pre_result:
            if withpass:
                return SUser.model_validate(pre_result, from_attributes=True)
            return self.schema.model_validate(pre_result, from_attributes=True)
