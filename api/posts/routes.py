import enum
from fastapi.routing import APIRouter

from posts.models import Post
from posts.schemas import SPost, SPostService
from .post_repository import PostRepository, SortTypes


posts_router = APIRouter(prefix="/posts", tags=["Posts"])
posts_repository = PostRepository()



@posts_router.get("/all")
async def posts_all(sort_by: SortTypes | None = None) -> list[SPostService] | None:
    return await posts_repository.get(sort_type=sort_by)


@posts_router.get("/{id}")
async def posts_get_by_id(id: int) -> SPostService | None:
    return await posts_repository.get(id_=id)


@posts_router.post("/add")
async def posts_add(schema: SPost) -> SPost:
    return await posts_repository.post(schema=schema, commit=True)


@posts_router.put("/update/{id}")
async def posts_update(id: int, schema: SPost) -> SPost | None:
    return await posts_repository.update(id_=id, schema=schema, commit=True)


@posts_router.delete("/delete/{id}")
async def posts_delete(id: int) -> SPost | None:
    return await posts_repository.delete(id_=id, commit=True)
