import pytest
from posts.models import Post
from posts.schemas import SPost
from repository import Repository


repo = Repository(model=Post, schema=SPost)


@pytest.mark.asyncio
async def test_get_all():
    all_posts = await repo.get()
    assert isinstance(all_posts, list)
    if len(all_posts) > 0:
        assert isinstance(all_posts[0], SPost)
