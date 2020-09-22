from fastapi import APIRouter
from .user_endpoint import router as user_endpoint

router = APIRouter()
router.include_router(user_endpoint, prefix="/user")
