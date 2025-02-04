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
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert isinstance(SPost.model_validate(resp.json()[0]), SPost)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_posts_endp_specific(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp_specific = await client.get(f"/{id_}/")
    assert resp_specific.status_code == 200
    assert resp_specific.json() is not None
    assert resp_specific.json()["id"] == id_
    assert isinstance(SPostService.model_validate(resp_specific.json()), SPostService)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(20, 30)])
async def test_posts_endp_insert(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    model = SPost(
        id=id_,
        title=f"post_test-{id_}",
        text="test-post2",
        author=id_-20,
    )
    resp = await client.post(url="/add/", json=model.model_dump())
    all_posts = await client.get("/all/")
    assert resp.status_code == 200
    assert resp.json()["id"] == id_ 
    assert model.title in [p["title"] for p in all_posts.json()]


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_posts_endp_update(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    new_model = SPost(
        id=id_,
        title=f"post_test-update{id_}",
        text="text-updatedmodel",
        author=id_,
    )
    resp = await client.put(url=f"/update/{new_model.id}/", json=new_model.model_dump())
    all_posts = await client.get(url="/all/")
    assert resp.status_code == 200
    assert resp.json() is not None
    assert resp.json()["id"] == id_
    assert new_model.title in [p["title"] for p in all_posts.json()]


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_posts_endp_delete(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.delete(url=f"/delete/{id_}/")
    all_posts = await client.get(url="/all/")
    assert resp.status_code == 200
    assert resp.json() is not None
    assert resp.json()["id"] == id_
    assert resp.json() not in all_posts.json()
