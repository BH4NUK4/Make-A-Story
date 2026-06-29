from typing import List, Optional,Dict , Any
from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    text : str = Field(description="the text of the optiom show to the user")
    nextNode : Dict[str , Any] = Field(description= "the next node content and its options")
    
class StoryNodeLLM(BaseModel):
    content: str = Field(description="the main content of the story node")
    isEnding : bool = Field(description="weather this is ending node")
    isWinningEnding :bool = Field(description="weather this is a winning node")
    options : Optional[List[StoryOptionLLM]] = Field(default=None , description="the option for this node")
    
    
class StoryLLMResponse(BaseModel):
    title: str = Field(description="the title of the story")
    rootNode : StoryNodeLLM = Field( description= " The root node of the story")