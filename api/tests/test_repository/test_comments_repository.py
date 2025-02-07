import pytest

from comments.models import Comment, Review
from comments.schemas import SComment, SCommentView, SReview, SReviewView
from comments.comments_repository import CommentsRepository


repo_comments = CommentsRepository(model=Comment, schema=SCommentView)
repo_reviews = CommentsRepository(model=Review, schema=SReviewView)


@pytest.mark.asyncio
async def test_all_comments(pre_db_comments):
    r = await repo_comments.get_comments(post_id=11)
    assert isinstance(r, list)
    assert isinstance(r[0], SCommentView)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_insert_comments(id_, pre_db_comments):
    payload = SComment(
        post_id=id_ + 10,
        review_id=id_ + 10,
    )
    r = await repo_comments.post(schema=payload, commit=True)
    assert isinstance(r, SCommentView)
    assert r in await repo_comments.get_comments(post_id=id_ + 10)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_insert_reviews(id_, pre_db_comments):
    payload = SReview(text=f"test-review-insert-{id_}", author=id_ + 10)
    r = await repo_reviews.post(schema=payload, commit=True)
    assert isinstance(r, SReviewView)
