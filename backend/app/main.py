from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.seed import init_db
from backend.app.api.auth import router as auth_router
from backend.app.api.courses import router as courses_router
from backend.app.api.leads import router as leads_router
from backend.app.api.students import router as students_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and seed roles & test data
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS configuration for Nuxt 4 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication, Courses, Leads, and Students routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(courses_router, prefix=settings.API_V1_STR)
app.include_router(leads_router, prefix=settings.API_V1_STR)
app.include_router(students_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "database": "sqlite",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
