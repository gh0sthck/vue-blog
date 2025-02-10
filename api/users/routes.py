from fastapi.routing import APIRouter

from users.models import User
from users.schemas import SUser, SUserService
from repository import Repository

users_router = APIRouter(prefix="/users", tags=["Users"])
users_repo = Repository(model=User, schema=SUserService)


@users_router.get("/all")
async def users_all() -> None | list[SUserService]:
    return await users_repo.get()


@users_router.get("/{id}")
async def users_by_id(id: int) -> None | SUserService:
    return await users_repo.get(id_=id)


@users_router.post("/register")
async def users_register(schema: SUser) -> SUserService:
    return await users_repo.post(schema, commit=True)
