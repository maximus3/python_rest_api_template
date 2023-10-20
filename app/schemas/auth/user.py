from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class User(BaseModel):
    username: str
    dt_created: datetime
    dt_updated: datetime

    model_config = SettingsConfigDict(
        from_attributes=True,
    )
