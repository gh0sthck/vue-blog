import asyncio
import datetime
from typing import Iterable
import pytest
import pytest_asyncio
from sqlalchemy import Insert, Delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from users.models import User
from users.schemas import SUser
from posts.schemas import SPost
from posts.models import Post
from database import Model
from settings import config


test_engine = create_async_engine(url=config.db_tests.dsn)
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)
Model.metadata.bind = test_engine


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def create_tables(table: Model, values: Iterable):
    async with test_async_session() as session:
        await session.execute(Delete(table))
        await session.commit()
        stmt = Insert(table).values(values)
        await session.execute(stmt)
        await session.commit()


async def delete_tables(table):
    async with test_async_session() as session:
        await session.execute(Delete(table))
        await session.commit()


@pytest_asyncio.fixture
async def pre_db_users():
    await create_tables(
        User,
        SUser(
            id=0,
            username="testuser",
            password="test",
            email="test@mail.com",
            birthday=datetime.date.today(),
            bio="test",
        ).model_dump(),
    )
    yield
    await delete_tables(User)


@pytest_asyncio.fixture
async def pre_db_posts(pre_db_users):
    posts = [
        SPost(
            id=i,
            title=f"test-post-{i}",
            text=f"post-desc-{i}",
            created_date=datetime.datetime.now(datetime.timezone.utc),
            update_date=datetime.datetime.now(datetime.timezone.utc),
            author=0,
        ).model_dump()
        for i in range(10)
    ]
    await create_tables(Post, posts)
    yield
    await delete_tables(Post)
