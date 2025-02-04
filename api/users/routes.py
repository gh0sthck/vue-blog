from fastapi.routing import APIRouter

from users.models import User
from users.schemas import SUser, SUserView
from repository import Repository

users_router = APIRouter(prefix="/users", tags=["Users"])
users_repo = Repository(model=User, schema=SUser)


@users_router.get("/all/")
async def users_all() -> None | list[SUserView]:
    r: list[SUser] | None = await users_repo.get()
    if r:
        return [SUserView.model_validate(m.model_dump()) for m in r]


@users_router.get("/{id}/")
async def users_by_id(id: int) -> None | SUserView:
    raw: SUser | None = await users_repo.get(id_=id)
    if raw:
        return SUserView.model_validate(raw.model_dump())


@users_router.post("/register/")
async def users_register(schema: SUser) -> SUserView:
    raw: SUser = await users_repo.post(schema, commit=True)
    return SUserView.model_validate(raw.model_dump())
