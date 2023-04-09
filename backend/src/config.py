import pathlib

from pydantic import BaseSettings, Field

BASE_DIRECTORY = pathlib.Path(__file__).absolute().parent.parent


class AdvancedBaseSettings(BaseSettings):
    class Config:
        allow_mutation = False
        env_file = BASE_DIRECTORY / ".env"
        env_file_encoding = "utf-8"


class ProjSettings(AdvancedBaseSettings):
    DEBUG: str = Field(..., env="DEBUG")
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: str = Field(..., env="REDIS_PORT")
    BACKEND_CORS_ORIGINS: str = Field(..., env='BACKEND_CORS_ORIGINS')
    ALLOW_METHODS: str = Field(..., env='BACKEND_CORS_ORIGINS')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')

    @property
    def allowed_methods(self):
        return self.ALLOW_METHODS.split(', ')

    @property
    def allowed_cors(self):
        return self.BACKEND_CORS_ORIGINS.split(', ')


class PostgresSettings(AdvancedBaseSettings):
    PORT: str = Field(default="5432")
    USERNAME: str = Field(default="postgres")
    PASSWORD: str = Field(default="postgres")
    DATABASE: str = Field(default="postgres")
    HOST: str = Field(default="localhost")

    class Config:
        env_prefix = "DB_"


class EmailSettings(AdvancedBaseSettings):
    EMAIL_HOST: str = Field(..., env="EMAIL_HOST")
    EMAIL_PORT: int = Field(..., env="EMAIL_PORT")
    EMAIL_USERNAME:  str = Field(..., env="EMAIL_USERNAME")
    EMAIL_PASSWORD:  str = Field(..., env="EMAIL_PASSWORD")
    FROM:  str = Field(default='konstantin.saratovsky@yandex.ru')
    BASE_URL: str = Field(default='http://127.0.0.1:8000/')

    class Config:
        env_prefix = "EMAIL_"


class Settings(ProjSettings, PostgresSettings, EmailSettings):
    @property
    def DATABASE_URL(self) -> str:
        if self.DEBUG:
            return 'postgresql://postgres:12345678@localhost:5432/online_school'
        return f'postgresql://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}'

    @property
    def REDIS_HOST(self) -> str:
        if self.DEBUG:
            return 'localhost'
        return self.HOST


settings = Settings()


class AdminData(AdvancedBaseSettings):
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)

    class Config:
        env_prefix = "ADMIN_"


admin_data = AdminData()
