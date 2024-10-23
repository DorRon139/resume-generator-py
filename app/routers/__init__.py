from fastapi import APIRouter
from .health import router as health_router
from .build_user_info import router as build_user_info_router
from .update_resume_content import router as update_resume_content_router

router = APIRouter()
router.include_router(health_router)
router.include_router(build_user_info_router, prefix='/ai')
router.include_router(update_resume_content_router, prefix='/ai')
