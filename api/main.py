from contextlib import asynccontextmanager
from fastapi import FastAPI

from settings import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title=config.app_name, docs_url=config.docs_url, lifespan=lifespan)
