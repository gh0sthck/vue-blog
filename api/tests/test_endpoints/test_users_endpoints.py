import datetime
from re import S
import pytest_asyncio
import httpx
import pytest

from users.schemas import SUser, SUserView
from main import app

URL = "http://localhost:8000/users"


@pytest_asyncio.fixture
async def get_client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=URL
    ) as cli:
        yield cli


@pytest.mark.asyncio
async def test_users_endp_get(pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get("/all/")
    assert resp.status_code == 200
    assert resp.json()  # Not null check: get(/all/) -> [] != None
    assert isinstance(resp.json(), list)
    assert isinstance(SUserView.model_validate(resp.json()[0]), SUserView)


@pytest.mark.asyncio
async def test_users_endp_reg(pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    us = SUser(
        id=123, 
        username="newuser",
        birthday=datetime.date.today(),
        password="testpass",
        email="testmaillll@mail.com",
        bio="test",
    )
    us.birthday = us.birthday.isoformat()
    resp = await client.post(url="/register/", json=us.model_dump())
    assert resp.status_code == 200
    assert resp.json() is not None
    assert isinstance(SUserView.model_validate(resp.json()), SUserView)
    assert us.username in tuple(
        u["username"] for u in (await client.get("/all/")).json()
    )


@pytest.mark.asyncio
async def test_users_endp_specific(pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp_specific = await client.get("/0/")
    assert resp_specific.status_code == 200
    assert resp_specific.json() is not None
    assert isinstance(SUserView.model_validate(resp_specific.json()), SUserView)
