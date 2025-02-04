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
async def test_specific_user(pre_db_users):
    user = await repo.get(id_=0)
    assert isinstance(user, SUser)
    assert user in await repo.get()
    assert user.id == 0


@pytest.mark.asyncio
async def test_insert_user(pre_db_users):
    new_user = SUser(
        id=2,
        username="testuser2",
        password="testpass",
        email="testmaill@gmail.com",
        birthday=datetime.date.today(),
        bio="non",
    )
    assert new_user not in await repo.get()
    await repo.post(schema=new_user, commit=True)
    assert new_user in await repo.get()
    assert new_user == await repo.get(id_=new_user.id)


@pytest.mark.asyncio
async def test_update_user(pre_db_users):
    new_user = SUser(
        id=0,
        username="testuser2",
        password="testpass",
        email="testmaill@gmail.com",
        birthday=datetime.date.today(),
        bio="non",
    )
    assert new_user != await repo.get(id_=new_user.id)
    await repo.update(id_=new_user.id, schema=new_user, commit=True)
    assert new_user == await repo.get(id_=new_user.id)
    assert new_user in await repo.get()


@pytest.mark.asyncio
async def test_delete_user(pre_db_users):
    r = await repo.delete(id_=0, commit=True)
    assert r not in await repo.get()
    assert None == await repo.get(id_=r.id)
