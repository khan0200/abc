from backend.app.api.auth import router as auth_router
from backend.app.api.courses import router as courses_router
from backend.app.api.leads import router as leads_router

__all__ = ["auth_router", "courses_router", "leads_router"]
