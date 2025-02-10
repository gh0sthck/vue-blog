from sqlalchemy import Insert, Select, and_, Delete
from posts.models import Like
from posts.schemas import SLike, SLikeService
from repository import Repository


class LikeRepository(Repository):
    def __init__(self):
        super().__init__(Like, SLikeService)

    @Repository._session
    async def get(self, id_: int, _session=...) -> list[int]:
        q = Select(Like).where(self.model.c.post_id == id_)
        r = await _session.execute(q)
        pre_result = r.fetchall()
        self.logger.debug(f"Get like executed (id) = {id_}")
        if pre_result:
            self.logger.debug(f"Get like result = {pre_result}")
            return [u_id[2] for u_id in pre_result]
        return []

    @Repository._session
    async def post(
        self, schema: SLike, commit: bool = False, _session=...
    ) -> SLikeService | None:
        u_liked = await self.get(id_=schema.post_id)
        if schema.user_id not in u_liked:
            q = Insert(Like).values(schema.model_dump())
            db_id = await _session.execute(q)
            model_dict = q.compile().params
            model_dict["id"] = db_id.inserted_primary_key[0]
            self.logger.debug(f"Post like executed, dict result = {model_dict}")
            if commit:
                await _session.commit()
            return SLikeService.model_validate(model_dict)
        return None

    @Repository._session
    async def delete(
        self, schema: SLike, commit: bool = False, _session=...
    ) -> SLikeService | None:
        q = Select(Like).where(and_(self.model.c.user_id == schema.user_id, self.model.c.post_id == schema.post_id))
        r = await _session.execute(q)
        delete_model = r.fetchall()[0]
        schema_model = self.schema(id=delete_model[0], user_id=delete_model[2], post_id=delete_model[1])
        q2 = Delete(Like).where(self.model.c.id == schema_model.id)
        await _session.execute(q2)
        if commit:
            await _session.commit() 
        return schema_model
