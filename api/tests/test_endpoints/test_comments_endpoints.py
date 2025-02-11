import pytest
import httpx
import pytest_asyncio

from users.schemas import SJWTPayload
from users.utils import encode_jwt
from comments.schemas import SCommentView, SReview, SReviewView
from main import app

URL = "http://localhost:8000/comments"


@pytest_asyncio.fixture
async def get_client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=URL
    ) as cli:
        yield cli


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_comments_endp_insert(id_, get_user_list, pre_db_comments, get_client):
    client: httpx.AsyncClient = get_client
    client.cookies.set(
        "access_token",
        encode_jwt(
            SJWTPayload(
                username=get_user_list[id_ - 10]["username"],
                email=get_user_list[id_ - 10]["email"],
            )
        ).decode(),
    )
    payload = SReview(text=f"test-review-insert-{id_}", author=id_ + 10)
    resp = await client.post(f"{id_+10}", json=payload.model_dump())
    assert resp.status_code == 200
    assert isinstance(SCommentView.model_validate(resp.json()), SCommentView)


@pytest.mark.asyncio
@pytest.mark.parametrize("post_id", [i for i in range(10, 20)])
async def test_comments_endp_getcomm(post_id, pre_db_comments, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get(f"get/{post_id}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert isinstance(SCommentView.model_validate(resp.json()[0]), SCommentView)


@pytest.mark.asyncio
@pytest.mark.parametrize("comment_id", [i for i in range(10, 20)])
async def test_comments_endp_getreview(comment_id, pre_db_comments, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get(f"reviews/{comment_id}")
    assert resp.status_code == 200
    assert isinstance(SReviewView.model_validate(resp.json()), SReviewView)
