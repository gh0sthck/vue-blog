from contextlib import asynccontextmanager
from fastapi import FastAPI

from settings import config
from posts import posts_router
from users import users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title=config.app_name, docs_url=config.docs_url, lifespan=lifespan)
app.include_router(posts_router)
app.include_router(users_router)
