from sqlalchemy import Column, Integer, String, Boolean, ForeignKey , DateTime , JSON

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Story(Base):
    __tablename__ = "stories" #table name in the database

    #columns in the table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False , index=True)
    session_id = Column(String, nullable=False , index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    #relationships between tables
    node = relationship("StoryNode", back_populates="story")

class StoryNode(Base):
    __tablename__ = "story_nodes"

    #columns in the table
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False , index=True)
    content = Column(String, nullable=False)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, nullable=True ,default=list)
    
    story = relationship("Story", back_populates="node")