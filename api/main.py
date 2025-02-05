from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import config
from posts import posts_router
from users import users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title=config.app_name, docs_url=config.docs_url, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts_router)
app.include_router(users_router)
