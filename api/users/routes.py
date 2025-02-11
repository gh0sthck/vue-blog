from urllib import response
from fastapi import Depends, Form, HTTPException, Request, Response
from fastapi.routing import APIRouter

from users.users_repository import UsersRepository
from users.utils import decode_jwt, encode_jwt, hash_password, validate_password
from users.schemas import SJWTPayload, SJWTToken, SUser, SUserService
from repository import Repository

users_router = APIRouter(prefix="/users", tags=["Users"])
# users_repo = Repository(model=User, schema=SUserService)
users_repo = UsersRepository()


async def validate_auth_user(username: str = Form(), password: str = Form()):
    user = await users_repo.get_by_usernmae(username=username, withpass=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if validate_password(password, user.password.encode()):
        return user
    raise HTTPException(status_code=401, detail="Invalid username or password")


async def get_token(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    if token:
        return decode_jwt(token.encode())
    raise HTTPException(status_code=401, detail="Unauthorized")


async def get_current_user(token: dict = Depends(get_token)):
    return await users_repo.get_by_usernmae(token.get("username"))


@users_router.get("/all")
async def users_all() -> None | list[SUserService]:
    return await users_repo.get()


@users_router.post("/register")
async def users_register(schema: SUser) -> SUserService:
    schema.password = (hash_password(schema.password.encode())).decode()
    print(schema)
    return await users_repo.post(schema, commit=True)


@users_router.post("/login")
async def users_login(response: Response, schema: SUser = Depends(validate_auth_user)) -> None:
    payload = SJWTPayload(
        username=schema.username,
        email=schema.email
    )
    token = encode_jwt(payload)
    response.set_cookie(
        key="access_token",
        value=token.decode(),
        httponly=True,
    )
    return SJWTToken(token=token)


@users_router.get("/me")
async def users_me(user: SUserService = Depends(get_current_user)) -> SUserService:
    return user


@users_router.post("/logout")
async def users_logout(request: Request, response: Response) -> dict[str, int]:
    token = request.cookies.get("access_token")
    if token:
        response.delete_cookie("access_token")
        return {"status": 200}
    raise HTTPException(status_code=401, detail="Unauthorized")


@users_router.get("/{id}")
async def users_by_id(id: int) -> None | SUserService:
    return await users_repo.get(id_=id)
