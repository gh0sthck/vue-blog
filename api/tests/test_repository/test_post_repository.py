import datetime
import pytest
from posts.models import Post
from posts.schemas import SPost
from repository import Repository


repo = Repository(model=Post, schema=SPost)


@pytest.mark.asyncio
async def test_all_posts(pre_db_posts):
    all_posts = await repo.get()
    assert isinstance(all_posts, list)
    assert isinstance(all_posts[0], SPost)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_specific_post(id_, pre_db_posts):
    specific_post = await repo.get(id_=id_)
    assert isinstance(specific_post, SPost)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(20, 30)])
async def test_insert_post(id_, pre_db_posts):
    result = await repo.post(
        schema=SPost(
            id=id_,
            title=f"post_test-insert{id_}",
            text="test",
            created_date=datetime.datetime.now(datetime.timezone.utc),
            update_date=datetime.datetime.now(datetime.timezone.utc),
            author=id_-20,
        ),
        commit=True,
    )

    assert isinstance(result, SPost)
    assert result in await repo.get()
    assert result == await repo.get(id_=id_)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_update_post(id_, pre_db_posts):
    new_post = SPost(
        id=id_,
        title=f"post_test-insert{id_}",
        text="test",
        created_date=datetime.datetime.now(datetime.timezone.utc),
        update_date=datetime.datetime.now(datetime.timezone.utc),
        author=id_,
    )

    r = await repo.update(id_=new_post.id, schema=new_post, commit=True)

    assert isinstance(r, SPost)
    assert r == new_post
    assert new_post == await repo.get(id_=new_post.id)
    assert new_post in await repo.get()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_delete_post(id_, pre_db_posts):
    r = await repo.delete(id_=id_, commit=True)

    assert isinstance(r, SPost)
    assert r not in await repo.get()
    assert None == await repo.get(id_=r.id)
