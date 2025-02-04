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
async def test_users_endp_all(pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get("/all/")
    assert resp.status_code == 200
    assert resp.json()  # Not null check: get(/all/) -> [] != None
    assert isinstance(resp.json(), list)
    assert isinstance(SUserView.model_validate(resp.json()[0]), SUserView)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(20, 30)])
async def test_users_endp_reg(id_, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    us = SUser(
        id=id_, 
        username=f"test_user-reg{id_}",
        birthday=datetime.date.today(),
        password="testpass",
        email=f"testmaillll_{id_}@mail.com",
        bio="test",
    )
    us.birthday = us.birthday.isoformat()
    resp = await client.post(url="/register/", json=us.model_dump())
    assert resp.status_code == 200
    assert resp.json() is not None
    assert isinstance(SUserView.model_validate(resp.json()), SUserView)
    assert resp.json()["id"] == id_ 
    assert us.username in tuple(
        u["username"] for u in (await client.get("/all/")).json()
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_users_endp_specific(id_, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp_specific = await client.get(f"/{id_}/")
    assert resp_specific.status_code == 200
    assert resp_specific.json() is not None
    assert resp_specific.json()["id"] == id_
    assert isinstance(SUserView.model_validate(resp_specific.json()), SUserView)
