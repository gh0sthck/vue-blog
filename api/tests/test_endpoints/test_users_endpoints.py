import datetime
import pytest_asyncio
import httpx
import pytest

from users.utils import encode_jwt
from users.schemas import SJWTPayload, SJWTToken, SUser, SUserService, SUserView
from tests.fixtures import get_user_list
from main import app

URL = "http://localhost:8000/users"


@pytest_asyncio.fixture
async def get_client():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=URL
    ) as cli:
        yield cli


RETURN_SCHEMA = SUserView


@pytest.mark.asyncio
async def test_users_endp_all(pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.get("/all")
    assert resp.status_code == 200
    assert resp.json()  # Not null check: get(/all/) -> [] != None
    assert isinstance(resp.json(), list)
    assert isinstance(SUserView.model_validate(resp.json()[0]), SUserView)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_users_endp_reg(id_, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    us = SUser(
        username=f"test_user-reg{id_}",
        birthday=datetime.date.today(),
        password="testpass",
        email=f"testmaillll_{id_}@mail.com",
        bio="test",
    )
    us.birthday = us.birthday.isoformat()
    resp = await client.post(url="/register", json=us.model_dump())
    assert resp.status_code == 200
    assert resp.json() is not None
    assert isinstance(RETURN_SCHEMA.model_validate(resp.json()), RETURN_SCHEMA)
    assert resp.json()["id"] == id_
    assert us.username in tuple(
        u["username"] for u in (await client.get("/all")).json()
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_users_endp_specific(id_, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp_specific = await client.get(f"/{id_}")
    assert resp_specific.status_code == 200
    assert resp_specific.json() is not None
    assert resp_specific.json()["id"] == id_
    assert isinstance(RETURN_SCHEMA.model_validate(resp_specific.json()), RETURN_SCHEMA)


@pytest.mark.asyncio
@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
async def test_users_endp_login(cnt, get_user_list, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    resp = await client.post(
        "/login",
        data={"username": get_user_list[cnt - 10]["username"], "password": f"testpassword-{cnt}"},
    )
    assert resp.status_code == 200
    assert SJWTToken.model_validate(resp.json())
    assert resp.cookies.get("access_token")


@pytest.mark.asyncio
@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
async def test_users_endp_logout(cnt, get_user_list, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    client.cookies.set("access_token", encode_jwt(
        SJWTPayload(
            username=get_user_list[cnt-10]["username"],
            email=get_user_list[cnt-10]["email"],
        )
    ).decode())
    resp = await client.post("/logout")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)
    assert not resp.cookies.get("access_token") 


@pytest.mark.asyncio
@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
async def test_users_endp_me(cnt, get_user_list, pre_db_users, get_client):
    client: httpx.AsyncClient = get_client
    client.cookies.set("access_token", encode_jwt(
        SJWTPayload(
            username=get_user_list[cnt-10]["username"],
            email=get_user_list[cnt-10]["email"],
        )
    ).decode())
    resp = await client.get("/me")
    assert resp.status_code == 200
    assert SUserService.model_validate(resp.json()) 
