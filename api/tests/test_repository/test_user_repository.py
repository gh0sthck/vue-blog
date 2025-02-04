import datetime
import pytest
from users.models import User
from users.schemas import SUser
from repository import Repository


repo = Repository(model=User, schema=SUser)


@pytest.mark.asyncio
async def test_all_users(pre_db_users):
    users = await repo.get()
    assert isinstance(users, list)
    assert isinstance(users[0], SUser)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_specific_user(id_, pre_db_users):
    user = await repo.get(id_=id_)
    assert isinstance(user, SUser)
    assert user in await repo.get()
    assert user.id == id_


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(20, 30)])
async def test_insert_user(id_, pre_db_users):
    new_user = SUser(
        id=id_,
        username=f"user_test-insert{id_}",
        password="testpass",
        email=f"testmaill{id_}@gmail.com",
        birthday=datetime.date.today(),
        bio="non",
    )
    assert new_user not in await repo.get()
    await repo.post(schema=new_user, commit=True)
    assert new_user in await repo.get()
    assert new_user == await repo.get(id_=new_user.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_update_user(id_, pre_db_users):
    new_user = SUser(
        id=id_,
        username=f"user_test-update{id_}",
        password="testpass",
        email=f"testmaill{id_}@gmail.com",
        birthday=datetime.date.today(),
        bio="non",
    )
    assert new_user != await repo.get(id_=new_user.id)
    await repo.update(id_=new_user.id, schema=new_user, commit=True)
    assert new_user == await repo.get(id_=new_user.id)
    assert new_user in await repo.get()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_delete_user(id_, pre_db_users):
    r = await repo.delete(id_=id_, commit=True)
    assert r not in await repo.get()
    assert None == await repo.get(id_=r.id)
