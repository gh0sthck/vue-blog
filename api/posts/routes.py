from fastapi.routing import APIRouter

from posts.models import Post
from posts.schemas import SPost
from repository import Repository


posts_router = APIRouter(prefix="/posts", tags=["Posts"])
posts_repository = Repository(model=Post, schema=SPost)


@posts_router.get("/all/")
async def posts_all() -> list[SPost] | None:
    return await posts_repository.get()
