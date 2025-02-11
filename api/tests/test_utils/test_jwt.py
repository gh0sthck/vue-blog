import jwt
import pytest

from users.utils import encode_jwt, decode_jwt
from tests.fixtures import get_jwt_payloads, get_jwt_tokens
from settings import config


@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
def test_jwt_encode(cnt, get_jwt_payloads):
    r = encode_jwt(get_jwt_payloads[cnt - 10])
    assert isinstance(r, bytes)
    assert (
        r
        == jwt.encode(
            get_jwt_payloads[cnt - 10].model_dump(),
            key=config.auth.SECRET_KEY,
            algorithm=config.auth.ALGORITHM,
        ).encode()
    )


@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
def test_jwt_decode(cnt, get_jwt_tokens, get_jwt_payloads):
    token = get_jwt_tokens[cnt - 10]
    r = decode_jwt(
        jwt_token=token, secret=config.auth.SECRET_KEY, algorithm=config.auth.ALGORITHM
    )
    assert isinstance(r, dict)
    assert r == get_jwt_payloads[cnt - 10].model_dump()
