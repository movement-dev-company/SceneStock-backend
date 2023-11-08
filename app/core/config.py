import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    DB_NAME: str
    DB_HOST: str
    POSTGRES_HOSTNAME: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    SECRET_KEY: str

    # CLIENT_ORIGIN: str

    class Config:
        if os.path.exists('./.env'):
            env_file = './.env'
        else:
            env_prefix = ''


settings = Settings()
