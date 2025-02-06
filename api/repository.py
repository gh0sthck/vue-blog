import datetime
from functools import wraps
from typing import Callable
from pydantic import BaseModel
from sqlalchemy import Insert, Select, Update, Delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from logs import BlogLogger
from database import Model, async_session


class Repository:
    LOGGER = BlogLogger("repository")

    def __init__(self, model: Model, schema: BaseModel):
        self.model = model
        self.schema = schema
        self.session = async_session()
        self.commit = False
        self.logger = self.LOGGER.get_logger()

    def _session(func: Callable):
        wraps(func)

        async def wrapper(self, *args, **kwargs):

            try:
                async with self.session as session:
                    return await func(self, _session=session, *args, **kwargs)
            except Exception as ex:
                self.logger.error(ex)

        return wrapper

    @_session
    async def get(
        self, id_: int | None = None, _session: AsyncSession = ...
    ) -> list[BaseModel] | BaseModel | None:
        q = (
            Select(self.model)
            if id_ is None
            else Select(self.model).where(self.model.id == id_)
        )
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

    @_session
    async def post(
        self, schema: BaseModel, commit: bool = False, _session: AsyncSession = ...
    ) -> BaseModel:
        q = Insert(self.model).values(schema.model_dump())
        db_id = await _session.execute(q)
        self.logger.debug(f"Post executed {q}")
        model_dict = q.compile().params
        model_dict["id"] = db_id.inserted_primary_key[0] 
        if commit:
            await _session.commit()
        return self.schema.model_validate(model_dict)

    @_session
    async def update(
        self,
        id_: int,
        schema: BaseModel,
        commit: bool = False,
        _session: AsyncSession = ...,
    ) -> BaseModel | None:
        p = await self.get(id_=id_)
        if p:
            q = (
                Update(self.model)
                .where(self.model.id == id_)
                .values(schema.model_dump())
            )
            await _session.execute(q)
            self.logger.debug(f"Update executed {q}")
            if commit:
                await _session.commit()
            return schema
        return None

    @_session
    async def delete(
        self, id_: int, commit: bool = False, _session: AsyncSession = ...
    ) -> BaseModel | None:
        p = await self.get(id_=id_)
        if p:
            q = Delete(self.model).where(self.model.id == id_)
            await _session.execute(q)
            self.logger.debug(f"Delete executed {q}")
            if commit:
                await _session.commit()
            return self.schema.model_validate(p)
        return None
