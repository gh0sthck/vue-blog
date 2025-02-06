import datetime

from pydantic import BaseModel
from sqlalchemy import Insert, Select
from sqlalchemy.ext.asyncio.session import AsyncSession
from repository import Repository
from .schemas import SCommentView


class CommentsRepository(Repository):
    def __init__(self, model, schema):
        super().__init__(model, schema)

    @Repository._session
    async def post(
        self, schema: BaseModel, commit: bool = False, _session=...
    ) -> BaseModel:
        q = Insert(self.model).values(schema.model_dump())
        db_id = await _session.execute(q)
        self.logger.debug(f"Post executed {q}")
        model_dict = q.compile().params
        model_dict["id"] = db_id.inserted_primary_key[0]
        model_dict["create_date"] = datetime.datetime.now()
        if commit:
            await _session.commit()
        return self.schema.model_validate(model_dict)

    @Repository._session
    async def get_comments(
        self, post_id: int, _session: AsyncSession = ...
    ) -> list[SCommentView]:
        q = Select(self.model).where(self.model.columns[1] == post_id)
        result = await _session.execute(q)
        pre_result = result.fetchall()
        if pre_result:
            return [self.schema(id=mod[0], post_id=mod[1], review_id=mod[2]) for mod in pre_result]
        return []
