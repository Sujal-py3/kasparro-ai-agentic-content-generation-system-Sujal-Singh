from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain.output_parsers import PydanticOutputParser
from src.models import ProductData, ComparisonPage, ComparisonDifferences
from src.prompts import COMPARISON_PROMPT
import os

# Intermediate model to capture the complex LLM output
class ComparisonGenerationResult(BaseModel):
    product_b: ProductData
    differences: ComparisonDifferences
    recommendation: List[str]

class ComparisonGeneratorAgent:
    """
    Agent responsible for generating comprehensive comparison pages.
    Generates fictional 'Product B' based on rules if not provided.
    """
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(temperature=0.7, model="llama-3.1-8b-instant", api_key=api_key)
        self.parser = PydanticOutputParser(pydantic_object=ComparisonGenerationResult)
        self.chain = COMPARISON_PROMPT | self.llm | self.parser

    def generate_comparison(self, product_a: ProductData, product_b_context: str = "Generate a fictional competitor following the rules") -> ComparisonPage:
        print(f"[ComparisonGenerator] Generating comparison against: '{product_b_context}'...")
        
        result: ComparisonGenerationResult = self.chain.invoke({
            "product_a_json": product_a.model_dump_json(),
            "product_b_context": product_b_context,
            "format_instructions": self.parser.get_format_instructions()
        })

        return ComparisonPage(
            title=f"Comparison: {product_a.name} vs {result.product_b.name}",
            product_a=product_a,
            product_b=result.product_b,
            differences=result.differences,
            recommendation=result.recommendation
        )
