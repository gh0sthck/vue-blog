import asyncio
import datetime
import pytest
import pytest_asyncio
from sqlalchemy import Insert, Delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from users.models import User
from users.schemas import SUser
from posts.schemas import SPost
from posts.models import Post
from database import async_session


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest_asyncio.fixture(scope="function")
async def get_session() -> AsyncSession:
    async with async_session() as session:
        return session


@pytest_asyncio.fixture(scope="function")
async def pre_db_posts(get_session):
    session: AsyncSession = get_session
    q_u = Insert(User).values(
        SUser(
            id=0,
            username="testuser",
            email="testmail@gmail.com",
            password="123",
            bio="test",
            birthday=datetime.date.today(),
        ).model_dump()
    )
    await session.execute(q_u)
    q = Insert(Post).values(
        SPost(
            id=0,
            title="testpost",
            text="test",
            created_date=datetime.datetime.now(datetime.timezone.utc),
            update_date=datetime.datetime.now(datetime.timezone.utc),
            author=0,
        ).model_dump()
    )
    await session.execute(q)
    await session.commit()
    
    yield
    
    d = Delete(Post).where(Post.id == 0)
    u = Delete(User).where(User.id == 0)
    await session.execute(d)
    await session.execute(u)
    await session.commit()
