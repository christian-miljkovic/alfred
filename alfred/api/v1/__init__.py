from fastapi import APIRouter
from .client_endpoint import router as client_endpoint
from .friend_endpoint import router as friend_endpoint
from .scheduler_endpoint import router as scheduler_endpoint

router = APIRouter()
router.include_router(client_endpoint, prefix="/client")
router.include_router(friend_endpoint, prefix="/friend")
router.include_router(scheduler_endpoint, prefix="/scheduler")
