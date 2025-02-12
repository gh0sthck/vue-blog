from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from users.routes import get_current_user
from users.schemas import SUserService

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


@posts_router.get("/by_user/{user_id}")
async def posts_get_by_userid(user_id: int) -> list[SPostService]:
    return await posts_repository.get_by_userid(user_id=user_id)


@posts_router.post("/add")
async def posts_add(
    schema: SPost, current_user: SUserService = Depends(get_current_user)
) -> SPostService:
    schema.author = current_user.id
    return await posts_repository.post(schema=schema, commit=True)


@posts_router.put("/update/{id}")
async def posts_update(
    id: int, schema: SPost, current_user: SUserService = Depends(get_current_user)
) -> SPost | None:
    post: SPostService = await posts_repository.get(id_=id)
    if post.author == current_user.id:
        schema.author = current_user.id
        return await posts_repository.update(id_=id, schema=schema, commit=True)
    raise HTTPException(status_code=403, detail="You havn't permissions to this page")


@posts_router.delete("/delete/{id}")
async def posts_delete(
    id: int, current_user: SUserService = Depends(get_current_user)
) -> SPostService | None:
    post: SPostService = await posts_repository.get(id_=id)
    if post.author == current_user.id:
        return await posts_repository.delete(id_=id, commit=True)
    raise HTTPException(status_code=403, detail="You havn't permissions to this page")


@posts_router.post("/like")
async def posts_like(
    schema: SLike, current_user: SUserService = Depends(get_current_user)
) -> SLikeService | None:
    schema.user_id = current_user.id
    return await likes_repository.post(schema=schema, commit=True)


@posts_router.post("/dislike")
async def posts_dislike(
    schema: SLike, current_user: SUserService = Depends(get_current_user)
) -> SLikeService | None:
    schema.user_id = current_user.id
    return await likes_repository.delete(schema=schema, commit=True)


@posts_router.get("/likes/{post_id}")
async def posts_like_get(post_id: int) -> list | None:
    return await likes_repository.get(id_=post_id)
