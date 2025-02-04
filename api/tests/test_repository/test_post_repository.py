import datetime
import pytest
from posts.models import Post
from posts.schemas import SPost
from repository import Repository


repo = Repository(model=Post, schema=SPost)


@pytest.mark.asyncio
async def test_get_all(pre_db_posts):
    all_posts = await repo.get()
    assert isinstance(all_posts, list)
    if len(all_posts) > 0:
        assert isinstance(all_posts[0], SPost)


@pytest.mark.asyncio
async def test_get_specific(pre_db_posts):
    specific_post = await repo.get(id_=0)
    assert isinstance(specific_post, SPost)


@pytest.mark.asyncio
async def test_insert(pre_db_posts):
    result = await repo.post(
        schema=SPost(
            id=20,
            title="testpost",
            text="test",
            created_date=datetime.datetime.now(datetime.timezone.utc),
            update_date=datetime.datetime.now(datetime.timezone.utc),
            author=0,
        ),
        commit=True,
    )

    assert isinstance(result, SPost)
    assert result in await repo.get()
    assert result == await repo.get(id_=20)


@pytest.mark.asyncio
async def test_update(pre_db_posts):
    new_post = SPost(
        id=2,
        title="testpost",
        text="test",
        created_date=datetime.datetime.now(datetime.timezone.utc),
        update_date=datetime.datetime.now(datetime.timezone.utc),
        author=0,
    )

    r = await repo.update(id_=new_post.id, schema=new_post, commit=True)

    assert isinstance(r, SPost)
    assert r == new_post
    assert new_post == await repo.get(id_=new_post.id)
    assert new_post in await repo.get()


@pytest.mark.asyncio
async def test_delete(pre_db_posts):
    r = await repo.delete(id_=1, commit=True)

    assert isinstance(r, SPost)
    assert r not in await repo.get()
    assert None == await repo.get(id_=r.id)
