import pytest
import httpx
import pytest_asyncio

from posts.schemas import SPost, SPostInsert
from main import app

URL = "http://localhost:8000/posts"


@pytest_asyncio.fixture
async def get_client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=URL
    ) as cli:
        yield cli


@pytest.mark.asyncio
async def test_posts_endp_all(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get("/all/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert isinstance(SPost.model_validate(resp.json()[0]), SPost)


@pytest.mark.asyncio
async def test_posts_endp_insert(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    model = SPostInsert(
        id=123,
        title="test-post-insertgggg",
        text="test-post2",
        author=0,
    )
    resp = await client.post(url="/add/", json=model.model_dump())
    assert resp.status_code == 200
    assert SPost.model_validate(resp.json()) == SPost.model_validate(model.model_dump())
