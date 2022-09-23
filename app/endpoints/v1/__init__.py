from fastapi import APIRouter

from .ping import api_router as ping_router
from .auth import api_router as auth_router


prefix = '/v1'
router = APIRouter(
    prefix=prefix,
)

router.include_router(ping_router)
router.include_router(auth_router)


__all__ = [
    'prefix',
    'router',
]
