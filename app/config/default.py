from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import Field
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments:
    for development, testing and production.
    But in this situation, we only have
    standard settings for local development.
    """

    ENV: str = Field('local', env='ENV')
    PROJECT_NAME: str = Field('PROJECT_NAME', env='PROJECT_NAME')
    PATH_PREFIX: str = Field('/api', env='PATH_PREFIX')
    APP_HOST: str = Field('http://127.0.0.1', env='APP_HOST')
    APP_PORT: int = Field(8090, env='APP_PORT')
    NGINX_EXTERNAL_PORT: int = Field(80, env='NGINX_EXTERNAL_PORT')
    DEBUG: bool = Field(True, env='DEBUG')

    POSTGRES_DB: str = Field('data', env='POSTGRES_DB')
    POSTGRES_HOST: str = Field('localhost', env='POSTGRES_HOST')
    POSTGRES_USER: str = Field('pguser', env='POSTGRES_USER')
    POSTGRES_PORT: int = Field(5432, env='POSTGRES_PORT')
    POSTGRES_PASSWORD: str = Field('pgpswd', env='POSTGRES_PASSWORD')

    LOGGING_FORMAT: str = (
        '%(filename)s %(funcName)s [%(thread)d] '
        '[LINE:%(lineno)d]# %(levelname)-8s '
        '[%(asctime)s.%(msecs)03d] %(name)s: '
        '%(message)s'
    )
    LOGGING_FILE_DIR: Path = Path('logs')
    LOGGING_APP_FILE: Path = LOGGING_FILE_DIR / 'logfile.log'
    LOGGING_SCHEDULER_FILE: Path = LOGGING_FILE_DIR / 'scheduler_logfile.log'
    LOGGING_WORKER_FILE: Path = LOGGING_FILE_DIR / 'worker_logfile.log'

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    CONFIG_FILENAME: str = 'config.yaml'

    JWT_SECRET: str = Field('', env='JWT_SECRET')

    # to get a string like this run: "openssl rand -hex 32"
    SECRET_KEY: str = Field('', env='SECRET_KEY')
    ALGORITHM: str = Field('HS256', env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        1440, env='ACCESS_TOKEN_EXPIRE_MINUTES'
    )

    PWD_CONTEXT: CryptContext = CryptContext(
        schemes=['bcrypt'], deprecated='auto'
    )

    AUTH_URL: str = '/api/v1/user/authentication'
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl=AUTH_URL
    )

    TG_HELPER_BOT_TOKEN: str = Field('', env='TG_HELPER_BOT_TOKEN')
    TG_ERROR_CHAT_ID: str = Field('', env='TG_ERROR_CHAT_ID')
    TG_DB_DUMP_CHAT_ID: str = Field('', env='TG_DB_DUMP_CHAT_ID')
    TG_LOG_SEND_CHAT_ID: str = Field('', env='TG_LOG_SEND_CHAT_ID')

    CELERY_BROKER_URL: str = Field(
        'redis://localhost:6379', env='CELERY_BROKER_URL'
    )
    CELERY_RESULT_BACKEND: str = Field(
        'redis://localhost:6379', env='CELERY_RESULT_BACKEND'
    )
    CELERY_USER: str = Field('', env='CELERY_USER')
    CELERY_PASSWORD: str = Field('', env='CELERY_PASSWORD')

    @property
    def database_settings(self) -> dict[str, str | int]:
        """
        Get all settings for connection with database.
        """
        return {
            'database': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return (
            'postgresql+asyncpg://{user}:{password}@'
            '{host}:{port}/{database}'.format(
                **self.database_settings,
            )
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return (
            'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
                **self.database_settings,
            )
        )

    class Config:
        env_file: Path | str = '.env'
        env_file_encoding = 'utf-8'
