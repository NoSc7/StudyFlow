from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, courses, modules, tasks

app = FastAPI(title="StudyFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ IMPORTANT : include routers avec les bons prefixes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(modules.router, prefix="/api/modules", tags=["modules"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/health")
def health():
    return {"status": "healthy"}
