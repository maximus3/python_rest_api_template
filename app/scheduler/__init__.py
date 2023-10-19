# Code generated automatically.

from app.schemas import scheduler as scheduler_schemas

from .db_dump import job as db_dump
from .ping import job as ping


list_of_jobs: list[scheduler_schemas.JobInfo] = [
    scheduler_schemas.JobInfo(
        **{
            'trigger': 'interval',
            'minutes': 1,
            'config': {'send_logs': False},
        },
        func=ping,
        name='ping',
    ),
    scheduler_schemas.JobInfo(
        **{'trigger': 'cron', 'hour': 3, 'config': {'send_logs': True}},
        func=db_dump,
        name='db_dump',
    ),
]


__all__ = [
    'list_of_jobs',
]
