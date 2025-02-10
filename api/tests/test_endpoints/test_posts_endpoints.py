import pytest
import httpx
import pytest_asyncio

from posts.schemas import SLike, SLikeService, SPost, SPostService
from main import app

URL = "http://localhost:8000/posts"


@pytest_asyncio.fixture
async def get_client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=URL
    ) as cli:
        yield cli

RETURN_SCHEMA = SPostService


@pytest.mark.asyncio
async def test_posts_endp_all(pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get("/all")
    assert resp.status_code == 200
    print(resp.json())
    assert isinstance(resp.json(), list)
    assert isinstance(RETURN_SCHEMA.model_validate(resp.json()[0]), RETURN_SCHEMA)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_posts_endp_specific(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp_specific = await client.get(f"/{id_}")
    assert resp_specific.status_code == 200
    assert resp_specific.json() is not None
    assert resp_specific.json()["id"] == id_
    assert isinstance(RETURN_SCHEMA.model_validate(resp_specific.json()), RETURN_SCHEMA)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_posts_endp_insert(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    model = SPost(
        title=f"post_test-{id_}",
        text="test-post2",
        author=id_ + 10,
    )
    resp = await client.post(url="/add", json=model.model_dump())
    all_posts = await client.get("/all")
    assert resp.status_code == 200
    assert resp.json()["id"] == id_
    assert model.title in [p["title"] for p in all_posts.json()]


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_posts_endp_update(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    new_model = SPost(
        title=f"post_test-update{id_}",
        text="text-updatedmodel",
        author=id_,
    )
    resp = await client.put(url=f"/update/{id_}", json=new_model.model_dump())
    all_posts = await client.get(url="/all")
    assert resp.status_code == 200
    assert resp.json() is not None
    assert resp.json()["title"] == new_model.title
    assert new_model.title in [p["title"] for p in all_posts.json()]


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_posts_endp_delete(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.delete(url=f"/delete/{id_}")
    all_posts = await client.get(url="/all")
    assert resp.status_code == 200
    assert resp.json() is not None
    assert resp.json()["id"] == id_
    assert resp.json() not in all_posts.json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_posts_endp_like(id_, pre_db_posts, get_client):
    client: httpx.AsyncClient = get_client
    payload = SLike(
        user_id=id_+10,
        post_id=id_+10
    ).model_dump()
    resp = await client.post(url=f"/like", json=payload)
    assert resp.status_code == 200
    assert isinstance(SLikeService.model_validate(resp.json()), SLikeService)


@pytest.mark.asyncio
@pytest.mark.parametrize("post_id", [i for i in range(10, 20)])
async def test_posts_endp_like_get(post_id, pre_db_likes, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get(f"/likes/{post_id}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert post_id in resp.json()  # In that case, post_id = user_id (fixtures.py) 
