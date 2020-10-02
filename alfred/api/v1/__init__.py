from fastapi import APIRouter
from .client_endpoint import router as client_endpoint

router = APIRouter()
router.include_router(client_endpoint, prefix="/client")
