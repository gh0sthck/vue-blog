import datetime
import bcrypt
import jwt
import pytest

from comments.schemas import SReviewView, SCommentView
from posts.schemas import SLikeService, SPostTest
from users.schemas import SJWTPayload, SUserTest
from settings import config

GENERATING_RANGE = range(10, 20)


@pytest.fixture
def get_user_list() -> list[dict]:
    return [
        SUserTest(
            id=cnt,
            username=f"test_user-{cnt}",
            birthday=datetime.date.today(),
            password=(bcrypt.hashpw(f"testpassword-{cnt}".encode(), bcrypt.gensalt())).decode(),
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


@pytest.fixture()
def get_review_list() -> list[dict]:
    return [
        SReviewView(
            id=cnt,
            text=f"text-for-review-{cnt}",
            author=cnt,
            create_date=datetime.datetime.now(),
        ).model_dump()
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_comments_list() -> list[dict]:
    return [
        SCommentView(
            id=cnt,
            post_id=cnt,
            review_id=cnt,
        ).model_dump()
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_likes_list() -> list[dict]:
    return [
        SLikeService(id=cnt, user_id=cnt, post_id=cnt).model_dump()
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_passwords() -> tuple[list[dict], bytes]:
    password_mock: str = "test-password-"
    salt: bytes = bcrypt.gensalt()
    return [
        {f"{password_mock}{cnt}": bcrypt.hashpw(f"{password_mock}{cnt}".encode(), salt)}
        for cnt in GENERATING_RANGE
    ], salt


@pytest.fixture
def get_jwt_payloads() -> list[SJWTPayload]:
    return [
        SJWTPayload(username=f"test_username-{cnt}", email=f"testemail{cnt}@testm.com")
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_jwt_tokens(get_jwt_payloads) -> list[bytes]:
    return [
        jwt.encode(
            payload.model_dump(),
            key=config.auth.SECRET_KEY,
            algorithm=config.auth.ALGORITHM,
        ).encode()
        for payload in get_jwt_payloads
    ]
