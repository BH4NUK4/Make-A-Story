from sqlalchemy.orm import Session
from core.config import Settings #??

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story


class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-4-turbo")