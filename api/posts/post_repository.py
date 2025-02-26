import datetime
import enum
from sqlalchemy import Date, Insert, Select, cast, func
from sqlalchemy.ext.asyncio.session import AsyncSession

from .models import Post
from .schemas import SPost, SPostService
from repository import Repository


class SortTypes(enum.Enum):
    ALL: str = "all"
    NEWEST: str = "newest"
    OLDEST: str = "oldest"
    TODAY: str = "today"
    TITLE: str = "title"


class PostRepository(Repository):
    def __init__(self):
        super().__init__(Post, SPostService)

    @Repository._session
    async def get(
        self, id_: int | None = None, sort_type: SortTypes | None = None, _session=...
    ) -> list[SPostService] | SPostService | None:
        q = (
            Select(self.model)
            if id_ is None
            else Select(self.model).where(self.model.id == id_)
        )
        self.logger.debug(f"SortType: {sort_type}")
        match sort_type:
            case SortTypes.ALL:
                q = q
            case SortTypes.TITLE:
                q = q.order_by(self.model.title)
            case SortTypes.TODAY:
                q = q.where(cast(self.model.created_date, Date) == func.current_date())
                self.logger.debug(q)
            case SortTypes.NEWEST:
                q = q.order_by(self.model.created_date.desc())
            case SortTypes.OLDEST:
                q = q.order_by(self.model.created_date)
        r = await _session.execute(q)
        if id_ is not None:
            pre_result = r.scalar_one_or_none()
            self.logger.debug(f"Get Pre result (id {id_}) = {pre_result}")
            return (
                self.schema.model_validate(pre_result.__dict__) if pre_result else None
            )
        pre_result = r.scalars().all()
        if pre_result:
            self.logger.debug(f"Get Pre result = {pre_result}")
            return [self.schema.model_validate(obj=r.__dict__) for r in pre_result]
        return []

    @Repository._session
    async def get_by_userid(self, user_id: int, _session: AsyncSession=...) -> list[SPostService]:
        q = Select(self.model).where(self.model.author==user_id)
        r = await _session.execute(q)
        pre_result = r.scalars().all() 
        if pre_result:
            self.logger.debug(f"Get pre result (posts by uid) = {pre_result}")
            return [self.schema.model_validate(r, from_attributes=True) for r in pre_result]
        return []

    @Repository._session
    async def post(
        self, schema: SPost, commit: bool = False, _session = ...
    ) -> SPostService:
        q = Insert(self.model).values(schema.model_dump())
        id_ = await _session.execute(q)
        self.logger.debug(f"Post executed {q}")
        if commit:
            await _session.commit()
        model_dict = q.compile().params
        model_dict["created_date"] = datetime.datetime.now()
        model_dict["id"] = id_.inserted_primary_key[0]
        model_dict["update_date"] = datetime.datetime.now()
        return self.schema.model_validate(model_dict)
