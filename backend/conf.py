from pydantic import BaseSettings
from functools import lru_cache
import typing as t


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: t.Optional[int] = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        if self.TEST:
            return "sqlite://:memory:"

        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    DEBUG: t.Optional[bool] = False
    TEST: t.Optional[bool] = False
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRES: t.Optional[int] = 3600 * 24  # 1 day
    REFRESH_TOKEN_EXPIRES: t.Optional[int] = 3600 * 24 * 7  # 7 days

    PASSWORD_MIN_LENGTH: t.Optional[int] = 8

    class Config:
        case_sensitive = True


@lru_cache()
def settings() -> Settings:
    return Settings()
