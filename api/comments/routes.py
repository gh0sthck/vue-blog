from fastapi import Depends
from fastapi.routing import APIRouter

from users.routes import get_current_user
from users.schemas import SUserService

from .comments_repository import CommentsRepository

from .models import Comment, Review
from .schemas import SCommentView, SReview, SComment, SReviewView

comments_router = APIRouter(prefix="/comments", tags=["Comments"])
review_repo = CommentsRepository(model=Review, schema=SReviewView)
comments_repo = CommentsRepository(model=Comment, schema=SCommentView)


@comments_router.post("/{id}")
async def comments_insert(id: int, review: SReview, current_user: SUserService = Depends(get_current_user)) -> SCommentView:
    review.author = current_user.id 
    r = await review_repo.post(schema=review, commit=True)
    return await comments_repo.post(
        schema=SComment(post_id=id, review_id=r.id), commit=True
    )


@comments_router.get("/reviews/{id}")
async def reviews_by_id(id: int) -> SReviewView | None:
    return await review_repo.get(id_=id)


@comments_router.get("/get/{post_id}")
async def comments_by_post(post_id: int) -> list[SCommentView]:
    return await comments_repo.get_comments(post_id=post_id)


@comments_router.get("/reviews_all/{id}")
async def reviews_all(id: int) -> list[SReviewView] | None:
    return [await reviews_by_id(m.review_id) for m in await comments_by_post(post_id=id)]
