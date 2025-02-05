import datetime
import enum
from sqlalchemy import Date, Select, cast, func

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
                q= q
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
