import pytest

from users.utils import hash_password, validate_password
from tests.fixtures import get_passwords


@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
def test_hashpassword(cnt, get_passwords):
    salt = get_passwords[1]
    passwd = get_passwords[0][cnt - 10]
    assert (
        hash_password(tuple(passwd.keys())[0].encode(), salt)
        == tuple(passwd.values())[0]
    )
    assert hash_password(tuple(passwd.keys())[0].encode()) != tuple(passwd.values())[0]


@pytest.mark.parametrize("cnt", [i for i in range(10, 20)])
def test_validatepassword(cnt, get_passwords):
    passwd = get_passwords[0][cnt - 10]
    assert validate_password(
        password=tuple(passwd.keys())[0],
        password_hash=tuple(passwd.values())[0]
    )
