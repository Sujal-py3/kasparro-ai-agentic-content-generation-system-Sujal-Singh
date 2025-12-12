from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain.output_parsers import PydanticOutputParser
from src.models import ProductData
from src.prompts import PRODUCT_ANALYSIS_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

class ProductAnalyzerAgent:
    """
    Agent responsible for analyzing raw input and extracting structured ProductData
    using an LLM and strict Pydantic parsing.
    """
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in environment.")
        
        # Using Llama 3 70B for high quality extraction
        self.llm = ChatGroq(temperature=0, model="llama-3.1-8b-instant", api_key=api_key) 
        self.parser = PydanticOutputParser(pydantic_object=ProductData)
        self.chain = PRODUCT_ANALYSIS_PROMPT | self.llm | self.parser

    def analyze(self, raw_data: Dict[str, Any]) -> ProductData:
        """
        Analyzes raw data dict and returns a structured ProductData object.
        """
        # Convert raw dict to string for the prompt
        raw_string = "\n".join([f"{k}: {v}" for k, v in raw_data.items()])
        
        print(f"[ProductAnalyzer] Extracting data with LLM...")
        try:
            result = self.chain.invoke({
                "raw_data": raw_string,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"[ProductAnalyzer] Error during extraction: {e}")
            raise e
