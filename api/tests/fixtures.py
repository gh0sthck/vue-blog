import datetime
import pytest

from posts.schemas import SPostService, SPostTest
from users.schemas import SUser, SUserTest

GENERATING_RANGE = range(10, 20)


@pytest.fixture
def get_user_list() -> list[dict]:
    return [
        SUserTest(
            id=cnt,
            username=f"test_user-{cnt}",
            birthday=datetime.date.today(),
            password="testpassword",
            email=f"testmailuser-{cnt}@mail.com",
            bio="testbio",
        ).model_dump()
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_posts_list() -> list[dict]:
    return [
        SPostTest(
            id=cnt,
            title=f"test_post-{cnt}",
            text="test",
            author=cnt,
            created_date=datetime.datetime.now(),
            update_date=datetime.datetime.now(),
        ).model_dump()
        for cnt in GENERATING_RANGE
    ]
