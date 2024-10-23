from fastapi import APIRouter
from .health import router as health_router
from .build_user_info import router as build_user_info_router

router = APIRouter()
router.include_router(health_router)
router.include_router(build_user_info_router, prefix='/ai')