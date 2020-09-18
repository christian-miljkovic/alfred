from fastapi import APIRouter
from .user_endpoint import router as user_endpoint
from .admin_endpoint import router as admin_endpoint

router = APIRouter()

router.include_router(user_endpoint, prefix="/user")
router.include_router(admin_endpoint, prefix="/admin")
