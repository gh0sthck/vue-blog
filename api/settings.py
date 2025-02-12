from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresData(BaseSettings):
    NAME: str
    USER: str
    HOST: str
    PASSWORD: str
    PORT: str

    model_config = SettingsConfigDict(env_file=".env")


class DatabaseSettings(BaseSettings):
    pg_data: PostgresData = PostgresData()

    postgres_dsn: PostgresDsn = (
        f"postgresql+asyncpg://{pg_data.USER}:{pg_data.PASSWORD}@{pg_data.HOST}:{pg_data.PORT}/{pg_data.NAME}"
    )

    @property
    def dsn(self) -> str:
        return self.postgres_dsn.unicode_string()


class AuthSettings(BaseSettings):
    SECRET_KEY: str = "mysecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MIN: int = 4


class DatabaseTestingSettings(BaseSettings):
    pg_data: PostgresData = PostgresData()

    postgres_dsn: PostgresDsn = (
        f"postgresql+asyncpg://{pg_data.USER}:{pg_data.PASSWORD}@{pg_data.HOST}:{pg_data.PORT}/{pg_data.NAME}"
    )

    @property
    def dsn(self) -> str:
        return self.postgres_dsn.unicode_string()


class Settings(BaseSettings):
    debug: bool = True
    app_name: str = "Blogg"
    docs_url: str = "/docs/"

    db: DatabaseSettings = DatabaseSettings()
    db_tests: DatabaseTestingSettings = DatabaseTestingSettings()
    auth: AuthSettings = AuthSettings()

config = Settings()
