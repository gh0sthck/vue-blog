import bcrypt
from fastapi import HTTPException
import jwt

from users.schemas import SJWTPayload
from settings import config


def encode_jwt(
    jwt_payload: SJWTPayload,
    secret: str = config.auth.SECRET_KEY,
    algorithm: str = config.auth.ALGORITHM,
) -> bytes:
    return jwt.encode(
        payload=jwt_payload.model_dump(),
        key=secret,
        algorithm=algorithm,
    ).encode()


def decode_jwt(
    jwt_token: bytes,
    secret: str = config.auth.SECRET_KEY,
    algorithm: str = config.auth.ALGORITHM,
) -> dict:
    try:
        decoded_jwt = jwt.decode(jwt_token, key=secret, algorithms=[algorithm])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalid")
    return decoded_jwt


def hash_password(password: bytes, salt: bytes | None = None) -> bytes:
    if not salt:
        salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password, salt=salt)


def validate_password(password: str, password_hash: bytes):
    return bcrypt.checkpw(password.encode(), password_hash)
