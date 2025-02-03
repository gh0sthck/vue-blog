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
