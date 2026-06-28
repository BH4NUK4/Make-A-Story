import uuid
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response ,BackgroundTasks
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.db.database import get_db , SessionLocal
from backend.models.story import Story , StoryNode
from backend.models.job import StoryJob
from backend.schemas.story import (
    CompleteStoryResponse , CompleteStoryNodeResponse , CreateStoryRequest 
)

from backend.schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/stories",
    tags=["stories"])


def get_session_id(session_id : Optional[str]= Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post(path="/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest, 
    response: Response,
    background_tasks: BackgroundTasks, 
    session_id: str = Depends(get_session_id), 
    db: Session = Depends(get_db)
):
  
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    job_id = str(uuid.uuid4())
    
    job = StoryJob(
        job_id=job,
        session_id=session_id,
        theme=request.theme,
        status="pending",
    )
    db.add(job)
    db.commit()
    
    
    return job


