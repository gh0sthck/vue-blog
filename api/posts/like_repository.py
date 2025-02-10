from sqlalchemy import Insert, Select
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
