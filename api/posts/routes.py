from fastapi.routing import APIRouter

from .like_repository import LikeRepository
from posts.schemas import SLike, SLikeService, SPost, SPostService
from .post_repository import PostRepository, SortTypes


posts_router = APIRouter(prefix="/posts", tags=["Posts"])
posts_repository = PostRepository()
likes_repository = LikeRepository()


@posts_router.get("/all")
async def posts_all(sort_by: SortTypes | None = None) -> list[SPostService] | None:
    return await posts_repository.get(sort_type=sort_by)


@posts_router.get("/{id}")
async def posts_get_by_id(id: int) -> SPostService | None:
    return await posts_repository.get(id_=id)


@posts_router.post("/add")
async def posts_add(schema: SPost) -> SPostService:
    return await posts_repository.post(schema=schema, commit=True)


@posts_router.put("/update/{id}")
async def posts_update(id: int, schema: SPost) -> SPost | None:
    return await posts_repository.update(id_=id, schema=schema, commit=True)


@posts_router.delete("/delete/{id}")
async def posts_delete(id: int) -> SPostService | None:
    return await posts_repository.delete(id_=id, commit=True)


@posts_router.post("/like/{post_id}")
async def posts_like(post_id: int, schema: SLike) -> SLikeService | None:
    return await likes_repository.post(schema=schema, commit=True)


@posts_router.get("/likes/{post_id}")
async def posts_like_get(post_id: int) -> list[int] | None:
    return await likes_repository.get(id_=post_id)
