import json

from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from src.models import ProductData
from src.prompts import PRODUCT_ANALYSIS_PROMPT

class ProductAnalyzerAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant")
        self.parser = PydanticOutputParser(pydantic_object=ProductData)

    def analyze(self, raw_dict):
        schema = self.parser.get_format_instructions()

        prompt = PRODUCT_ANALYSIS_PROMPT.format(
            raw_data=json.dumps(raw_dict, indent=2),
            format_instructions=schema   # ← REQUIRED
        )

        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)
