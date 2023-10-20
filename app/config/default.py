from pathlib import Path

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments:
    for development, testing and production.
    But in this situation, we only have
    standard settings for local development.
    """

    ENV: str = Field('local')
    PROJECT_NAME: str = Field('PROJECT_NAME')
    PATH_PREFIX: str = Field('/api')
    APP_HOST: str = Field('http://127.0.0.1')
    APP_PORT: int = Field(8090)
    NGINX_EXTERNAL_PORT: int = Field(80)
    DEBUG: bool = Field(True)

    POSTGRES_DB: str = Field('data1')
    POSTGRES_HOST: str = Field('localhost')
    POSTGRES_USER: str = Field('pguser')
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_PASSWORD: str = Field('pgpswd')

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

    JWT_SECRET: str = Field('')

    # to get a string like this run: "openssl rand -hex 32"
    SECRET_KEY: str = Field('')
    ALGORITHM: str = Field('HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(1440)

    PWD_CONTEXT: CryptContext = CryptContext(
        schemes=['bcrypt'], deprecated='auto'
    )

    AUTH_URL: str = '/api/v1/user/authentication'
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl=AUTH_URL
    )

    TG_HELPER_BOT_TOKEN: str = Field('')
    TG_ERROR_CHAT_ID: str = Field('')
    TG_DB_DUMP_CHAT_ID: str = Field('')
    TG_LOG_SEND_CHAT_ID: str = Field('')

    CELERY_BROKER_URL: str = Field('redis://localhost:6379')
    CELERY_RESULT_BACKEND: str = Field('redis://localhost:6379')
    CELERY_USER: str = Field('')
    CELERY_PASSWORD: str = Field('')

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

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
