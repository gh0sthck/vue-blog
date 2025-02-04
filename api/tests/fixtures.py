import datetime
import pytest

from posts.schemas import SPostService
from users.schemas import SUser


@pytest.fixture
def get_user_list() -> list[dict]:
    return [
        SUser(
            id=cnt,
            username=f"test_user-{cnt}",
            birthday=datetime.date.today(),
            password="testpassword",
            email=f"testmailuser-{cnt}@mail.com",
            bio="testbio", 
        ).model_dump()
        for cnt in range(10)
    ] 


@pytest.fixture
def get_posts_list() -> list[dict]:
    return [
        SPostService(
            id=cnt,
            title=f"test_post-{cnt}",
            text="test",
            author=cnt,
            created_date=datetime.datetime.now(datetime.timezone.utc),
            update_date=datetime.datetime.now(datetime.timezone.utc) 
        ).model_dump()
        for cnt in range(10)
    ]
