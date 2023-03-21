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
        return f"postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    DEBUG: t.Optional[bool] = False
    SECRET_KEY: str

    class Config:
        case_sensitive = True


@lru_cache()
def settings() -> Settings:
    return Settings()
