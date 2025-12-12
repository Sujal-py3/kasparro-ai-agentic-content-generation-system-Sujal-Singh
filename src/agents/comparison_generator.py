import json
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from src.models import ComparisonPage
from src.prompts import COMPARISON_PROMPT


class ComparisonGeneratorAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant")
        self.parser = PydanticOutputParser(pydantic_object=ComparisonPage)

    def generate_comparison(self, product):
        schema = self.parser.get_format_instructions()

        prompt = COMPARISON_PROMPT.format(
            product_a_json=product.model_dump_json(indent=2),
            product_b_context="Generate a fictional competitor following the rules.",
            format_instructions=schema
        )

        response = self.llm.invoke(prompt)
        return self.parser.parse(response.content)
