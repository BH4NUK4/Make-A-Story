from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import Settings

from routers import job, story
from db.database import create_tables


create_tables()  # Create tables if they don't exist
settings = Settings()

app = FastAPI(
    title="Write Your Own Story",
    description="A web application that allows users to create and share their own stories.",
    docs_url="/docs",
    redoc_url="/redoc",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story.router, prefix = settings.API_PREFIX )

app.include_router(job.router, prefix = settings.API_PREFIX )

 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000 ,reload=True)