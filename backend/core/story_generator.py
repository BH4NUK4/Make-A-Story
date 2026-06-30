from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified # <-- NEW IMPORT
from core.config import Settings 

from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM

class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        settings = Settings()
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.9
        )
     
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        
        promt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create the story with this theme : {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions())
         
        raw_response = llm.invoke(promt.invoke({}))
        
        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content
            
        # ==========================================
        # CLEAN UP THE AI'S RESPONSE
        # ==========================================
        if isinstance(response_text, list):
            response_text = response_text[0]
            if isinstance(response_text, dict) and "text" in response_text:
                response_text = response_text["text"]
                
        response_text = str(response_text).strip()
        
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "", 1)
            
        if response_text.endswith("```"):
            response_text = response_text.rsplit("```", 1)[0]
            
        response_text = response_text.strip()
        # ==========================================
            
        story_structure = story_parser.parse(response_text) 
        
        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()
        
        root_node_data = story_structure.rootNode 
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)
            
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        
        db.commit()
        return story_db
    
    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[] 
        )
        
        db.add(node)
        db.flush()
        
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            option_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode
                
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)
                
                child_node = cls._process_story_node(db, story_id, next_node, is_root=False) 
                
                option_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                }) 
                 
            # Assign the list to the node
            node.options = option_list
            
            # THE FIX: Force SQLAlchemy to save the array!
            flag_modified(node, "options")
               
        db.flush() 
        return node