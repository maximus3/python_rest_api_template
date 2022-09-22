from fastapi import APIRouter

from .ping import api_router as ping_router


prefix = '/v1'
router = APIRouter(
    prefix=prefix,
)

router.include_router(ping_router)


__all__ = [
    'prefix',
    'router',
]
