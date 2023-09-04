import typing as t
from functools import lru_cache

from pydantic import BaseSettings


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

    REDIS_HOST: str
    REDIS_PORT: t.Optional[int] = 6379
    REDIS_PASSWORD: str
    REDIS_DB: t.Optional[int] = 0
    RESET_CODE_EXPIRES: t.Optional[int] = 600  # 10 min.

    DEFAULT_PAGE_SIZE: t.Optional[int] = 20
    MAX_PAGE_SIZE: t.Optional[int] = 50

    TRANSLATION_LOCALES: t.List[str] = ["uk", "en"]
    TRANSLATION_DEFAULT_LOCALE: t.Optional[str] = "uk"
    TRANSLATION_DIR: t.Optional[str] = "/backend/translations/locales"

    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True


@lru_cache()
def settings() -> Settings:
    return Settings()

