from typing import optional
from pydantic import BaseModel
from datetime import datetime


class StoryJobBase(BaseModel):
    theme: str
    
class StoryJobResponse(BaseModel):
    job_id : int
    status: str
    created_at: datetime
    story_id:optional[int] = None
    completed_at:optional[datetime] = None
    error:optional[str] = None
    class Config:
        from_attributes = True
        
class StoryJobCreate(StoryJobBase):
    pass  