from re import S
import pytest
import httpx
import pytest_asyncio

from posts.schemas import SPost, SPostService
from main import app

URL = "http://localhost:8000/posts"


@pytest_asyncio.fixture
async def get_client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=URL
    ) as cli:
        yield cli


@pytest.mark.asyncio
async def test_posts_endp_get(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get("/all/")
    resp_specific = await client.get("/2/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert isinstance(SPost.model_validate(resp.json()[0]), SPost)
    assert resp_specific.status_code == 200
    assert resp_specific.json() is not None
    assert isinstance(SPostService.model_validate(resp_specific.json()), SPostService)


@pytest.mark.asyncio
async def test_posts_endp_insert(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    model = SPost(
        id=123,
        title="test-post-insertgggg",
        text="test-post2",
        author=0,
    )
    resp = await client.post(url="/add/", json=model.model_dump())
    all_posts = await client.get("/all/")
    assert resp.status_code == 200
    assert model.title in [p["title"] for p in all_posts.json()]


@pytest.mark.asyncio
async def test_posts_endp_update(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    new_model = SPost(
        id=2,
        title="updatemodel",
        text="text-updatedmodel",
        author=0,
    )
    resp = await client.put(url=f"/update/{new_model.id}/", json=new_model.model_dump())
    all_posts = await client.get(url="/all/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)
    assert new_model.title in [p["title"] for p in all_posts.json()]


@pytest.mark.asyncio
async def test_posts_endp_delete(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.delete(url="/delete/3/") 
    all_posts = await client.get(url="/all/") 
    assert resp.status_code == 200
    assert resp.json() is not None
    assert resp.json() not in all_posts.json() 
