import pytest
from posts.post_repository import PostRepository
from posts.schemas import SPost, SPostService


repo = PostRepository()

RETURN_SCHEMA = SPostService


@pytest.mark.asyncio
async def test_all_posts(pre_db_posts):
    all_posts = await repo.get()
    assert isinstance(all_posts, list)
    assert isinstance(all_posts[0], RETURN_SCHEMA)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_specific_post(id_, pre_db_posts):
    specific_post = await repo.get(id_=id_)
    assert isinstance(specific_post, RETURN_SCHEMA)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_insert_post(id_, pre_db_posts):
    result = await repo.post(
        schema=SPost(
            title=f"post_test-insert{id_}",
            text="test",
            author=id_ + 10,
        ),
        commit=True,
    )
    assert isinstance(result, RETURN_SCHEMA)
    assert result.title in [m.title for m in await repo.get()]
    assert SPost.model_validate(result.model_dump()) == SPost.model_validate(
        (await repo.get(id_=id_)).model_dump()
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_update_post(id_, pre_db_posts):
    new_post = SPost(
        title=f"post_test-insert{id_}",
        text="test",
        author=id_,
    )

    r = await repo.update(id_=id_, schema=new_post, commit=True)

    assert isinstance(r, SPost)
    assert r == new_post


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_delete_post(id_, pre_db_posts):
    r = await repo.delete(id_=id_, commit=True)

    assert isinstance(r, RETURN_SCHEMA)
    assert r not in await repo.get()
    assert None == await repo.get(id_=r.id)
