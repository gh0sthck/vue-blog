from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import config

engine = create_async_engine(url=config.db.dsn)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
