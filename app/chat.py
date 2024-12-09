import google.generativeai as genai
import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto


class QueryContext(Enum):
    """Enum to represent different query contexts more robustly"""
    CODE_HELP = auto()
    LATEST_TECH = auto()
    PROJECT_GUIDANCE = auto()
    COURSE_INFO = auto()
    GENERAL_INQUIRY = auto()
    

@dataclass
class AIAssistantConfig:
    """Enhanced configuration class for the AI Assistant"""
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    max_output_tokens: int = 2048  # Increased token limit
    top_k: int =  40 # Additional parameter for response diversity
    top_p: float = 0.7  # Nucleus sampling for more controlled responses
    safety_settings: Dict[str, str] = field(default_factory=lambda: {
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_MEDIUM_AND_ABOVE'
    })
    response_formats: List[str] = field(default_factory=lambda: [
        'markdown',
        'structured_text',
        'bulleted_list',
        'code_explanation'
    ])


class PromptEngineeringStrategy:
    """Advanced prompt engineering with more sophisticated context detection and response structuring"""
    
    @staticmethod
    def detect_query_context(query: str) -> QueryContext:
        """
        Detect the context of the user's query with more nuanced classification
        
        :param query: User's input query
        :return: Detected QueryContext
        """
        query = query.lower()
        context_mapping = {
            QueryContext.CODE_HELP: [
                'code', 'function', 'debug', 'algorithm', 
                'programming', 'script', 'implementation'
            ],
            QueryContext.LATEST_TECH: [
                'ai', 'machine learning', 'trend', 'technology', 
                'innovation', 'research', 'breakthrough'
            ],
            QueryContext.PROJECT_GUIDANCE: [
                'project', 'help', 'guidance', 'approach', 
                'methodology', 'workflow', 'strategy'
            ],
            QueryContext.COURSE_INFO: [
                'course', 'semester', 'syllabus', 'curriculum', 
                'class', 'lecture', 'module'
            ]
        }
        
        # Prioritize context detection with multiple keyword matching
        for context, keywords in context_mapping.items():
            if any(keyword in query for keyword in keywords):
                return context
        
        return QueryContext.GENERAL_INQUIRY
    
    @classmethod
    def engineer_prompt(cls, query: str, context: QueryContext) -> str:

        context_prefixes = {
            QueryContext.CODE_HELP: "Expert AI and Data Science Mentor Mode",
            QueryContext.LATEST_TECH: "AI & Technology Insights Specialist Mode",
            QueryContext.PROJECT_GUIDANCE: "AI Project Mentorship Mode",
            QueryContext.COURSE_INFO: "Academic Course Advisory Mode",
            QueryContext.GENERAL_INQUIRY: "Comprehensive Knowledge Assistant Mode"
        }
        
        response_guidelines = {
            QueryContext.CODE_HELP: """
            Guidelines for Response:
            - Provide clear, modular code explanations
            - Include best practices and potential optimizations
            - Offer context about design choices
            - Suggest potential edge cases and error handling
            """,
            QueryContext.LATEST_TECH: """
            Guidelines for Response:
            - Emphasize practical applications
            - Provide recent research references
            - Explain complex concepts simply
            - Highlight potential industry impacts
            """,
            QueryContext.PROJECT_GUIDANCE: """
            Guidelines for Response:
            - Break down steps comprehensively
            - Suggest architectural approaches
            - Provide risk mitigation strategies
            - Recommend relevant tools and technologies
            """,
            QueryContext.COURSE_INFO: """
            Guidelines for Response:
            - Provide structured, detailed information
            - Include learning objectives
            - Suggest supplementary resources
            - Offer insights into practical applications
            """,
            QueryContext.GENERAL_INQUIRY: """
            Guidelines for Response:
            - Maintain clarity and depth
            - Provide multi-perspective insights
            - Use credible, recent sources
            - Encourage further exploration
            """
        }
        
        return f"""
        Mode: {context_prefixes[context]}
        
        Context Details:
        - Query: {query}
        - Detection Timestamp: {datetime.now().isoformat()}
        - Target Audience: Data Science and AI Engineering Professionals/Students

        {response_guidelines[context]}

        Response Requirements:
        1. Be precise and educational
        2. Provide actionable insights
        3. Maintain an engaging, professional tone
        4. Adapt to the specific query context
        """


class AIThinkingAssistant:

    
    def __init__(self, config: AIAssistantConfig = None, 
                 logger: logging.Logger = None):

        self.config = config or AIAssistantConfig()
        self.logger = logger or self._setup_logger()

        # Initialize Gemini API with enhanced error handling
        self._initialize_model()
    
    def _setup_logger(self) -> logging.Logger:

        logger = logging.getLogger('AIThinkingAssistant')
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_model(self):

        try:
            
            # Configure API key
            genai.configure(api_key=self._get_api_key())
            
            # Create model with enhanced generation config
            self.model = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config={
                    'temperature': self.config.temperature,
                    'max_output_tokens': self.config.max_output_tokens,
                    'top_k': self.config.top_k,
                    'top_p': self.config.top_p
                },
                safety_settings=self.config.safety_settings
            )
            
            self.logger.info(f"Initialized AI Assistant with model: {self.config.model_name}")
        
        except Exception as e:
            self.logger.error(f"Failed to initialize AI model: {e}")
            raise
    
    def _get_api_key(self) -> str:

        try:
            with open('config.json', 'r') as f:
                api_key = json.load(f).get('GOOGLE_API_KEY')
                
            if not api_key:
                raise ValueError("No API key found in configuration")
            
            return api_key
        
        except FileNotFoundError:
            self.logger.error("API key configuration file not found")
            raise ValueError("Please create a config.json with your GOOGLE_API_KEY")
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON in config file")
            raise ValueError("Config file contains invalid JSON")
    
    async def generate_response(self, query: str) -> str:

        try:

            context = PromptEngineeringStrategy.detect_query_context(query)
            

            engineered_prompt = PromptEngineeringStrategy.engineer_prompt(query, context)
            

            response = await asyncio.to_thread(
                self.model.generate_content, 
                engineered_prompt
            )
            

            self.logger.info(f"Successfully generated response for context: {context.name}")
            
            return response.text
        
        except Exception as e:
            self.logger.error(f"Error generating response: {e}", exc_info=True)
            return (
                "Apologies, an error occurred while processing your request. "
                "SAMI IS RESPONSIBLE FOR THIS "
                f"Error details: {e}"
            )

