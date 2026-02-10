"""Main application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, courses, modules, tasks

from app.db import Base, engine
import app.models  # IMPORTANT: charge les modèles (User, Course, ...)

app = FastAPI(title="StudyFlow API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(modules.router, prefix="/api/modules", tags=["modules"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Welcome to StudyFlow API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
