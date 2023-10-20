from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.sql import func

from app.database import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc='Unique index of element (type UUID)',
    )
    dt_created = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),  # pylint: disable=not-callable
        nullable=False,
        doc='Date and time of create (type TIMESTAMP)',
    )
    dt_updated = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),  # pylint: disable=not-callable
        onupdate=func.current_timestamp(),  # pylint: disable=not-callable
        nullable=False,
        doc='Date and time of last update (type TIMESTAMP)',
    )

    def __repr__(self) -> str:
        columns = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns  # type: ignore
        }
        return (
            f'<{self.__tablename__}: '  # type: ignore
            f'{", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
        )
