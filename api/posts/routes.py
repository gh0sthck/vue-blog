from typing import Annotated
from fastapi import Depends
from fastapi.routing import APIRouter

from posts.models import Post
from posts.schemas import SPost, SPostInsert
from repository import Repository


posts_router = APIRouter(prefix="/posts", tags=["Posts"])
posts_repository = Repository(model=Post, schema=SPost)


@posts_router.get("/all/")
async def posts_all() -> list[SPost] | None:
    return await posts_repository.get()


@posts_router.post("/add/")
async def posts_add(schema: SPostInsert) -> SPost:
    return await posts_repository.post(schema=schema, commit=True)

