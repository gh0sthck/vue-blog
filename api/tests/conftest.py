import asyncio
from typing import Iterable
import pytest
import pytest_asyncio
from sqlalchemy import Insert, Delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from comments.models import Comment, Review
from users.models import User
from posts.models import Post
from database import Model
from settings import config
from .fixtures import get_user_list, get_posts_list, get_review_list, get_comments_list

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


async def delete_tables(table: Model):
    async with test_async_session() as session:
        await session.execute(Delete(table))
        await session.commit()


async def create_tables(table: Model, values: Iterable):
    await delete_tables(table)
    async with test_async_session() as session:
        await session.execute(Insert(table).values(values))
        await session.commit()


@pytest_asyncio.fixture
async def pre_db_users(get_user_list):
    await create_tables(User, get_user_list)
    yield
    await delete_tables(User)


@pytest_asyncio.fixture
async def pre_db_posts(pre_db_users, get_posts_list):
    await create_tables(Post, get_posts_list)
    yield
    await delete_tables(Post)


@pytest_asyncio.fixture
async def pre_db_reviews(pre_db_posts, get_review_list):
    await create_tables(Review, get_review_list)
    yield
    await delete_tables(Review)


@pytest_asyncio.fixture
async def pre_db_comments(pre_db_reviews, get_comments_list):
    await create_tables(Comment, get_comments_list)
    yield
    await delete_tables(Comment)
