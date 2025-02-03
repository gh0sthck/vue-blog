from functools import wraps
from typing import Callable
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio.session import AsyncSession

from logs import BlogLogger
from database import Model, async_session


class Repository:
    LOGGER = BlogLogger()

    def __init__(self, model: Model, schema: BaseModel):
        self.model = model
        self.schema = schema
        self.session = async_session()
        self.commit = False
        self.logger = self.LOGGER.get_logger()

    def __get_session(func: Callable):
        wraps(func)

        async def wrapper(self, *args, **kwargs):
            try:
                async with self.session as session:
                    return await func(self, _session=session, *args, **kwargs)
            except Exception as ex:
                print("EXCEPTION IN REPOSITORY", ex)
                # self.logger.error(ex)

        return wrapper

    @__get_session
    async def get(
        self, id_: int | None = None, _session: AsyncSession = ...
    ) -> list[BaseModel] | BaseModel | None:
        q = (
            Select(self.model)
            if not id_
            else Select(self.model).where(self.model.id == id_)
        )
        r = await _session.execute(q)
        if id_ is not None:
            pre_result = r.scalar_one_or_none()
            return (
                self.schema.model_validate(pre_result.__dict__) if pre_result else None
            )
        pre_result = r.scalars().all()
        if pre_result:
            return [self.schema.model_validate(obj=r.__dict__) for r in pre_result]
        return []

    @__get_session
    async def post(
        self, model: BaseModel, commit: bool = False, _session: AsyncSession = ...
    ) -> BaseModel:
        pass

    async def update(self, id: int, model: BaseModel) -> BaseModel | None:
        pass

    async def delete(self, id: int) -> BaseModel | None:
        pass
