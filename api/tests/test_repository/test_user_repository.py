import datetime
import pytest

from users.users_repository import UsersRepository
from users.schemas import SUser, SUserService
from tests.fixtures import get_user_list


repo = UsersRepository()

RETURN_SCHEMA = SUserService


@pytest.mark.asyncio
async def test_all_users(pre_db_users):
    users = await repo.get()
    assert isinstance(users, list)
    assert isinstance(users[0], RETURN_SCHEMA)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_specific_user(id_, pre_db_users):
    user = await repo.get(id_=id_)
    assert isinstance(user, RETURN_SCHEMA)
    assert user in await repo.get()
    assert user.id == id_


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_insert_user(id_, pre_db_users):
    new_user = SUser(
        username=f"user_test-insert{id_}",
        password="testpass",
        email=f"testmaill{id_}@gmail.com",
        birthday=datetime.date.today(),
        bio="non",
    )
    nu = new_user.model_dump()
    nu["id"] = id_
    assert SUserService.model_validate(nu) not in await repo.get()
    await repo.post(schema=new_user, commit=True)
    assert SUserService.model_validate(nu) in await repo.get()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_update_user(id_, pre_db_users):
    new_user = SUser(
        username=f"user_test-update{id_}",
        password="testpass",
        email=f"testmaill{id_}@gmail.com",
        birthday=datetime.date.today(),
        bio="non",
    )
    assert new_user != await repo.get(id_=id_)
    await repo.update(id_=id_, schema=new_user, commit=True)
    nu = new_user.model_dump()
    nu["id"] = id_
    assert SUserService.model_validate(nu) == await repo.get(id_=id_)
    assert SUserService.model_validate(nu) in await repo.get()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_delete_user(id_, pre_db_users):
    r = await repo.delete(id_=id_, commit=True)
    assert r not in await repo.get()
    assert None == await repo.get(id_=r.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
async def test_get_by_username_user(cnt, get_user_list, pre_db_users):
    r = await repo.get_by_usernmae(username=get_user_list[cnt - 10]["username"])
    assert isinstance(r, RETURN_SCHEMA)
    assert r == await repo.get(id_=r.id)
    r2 = await repo.get_by_usernmae(username=get_user_list[cnt-10]["username"], withpass=True)
    assert isinstance(r2, SUser)
    assert r.username == r2.username
