import json


from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from src.models import FAQObject, ProductPage
from src.prompts import FAQ_GENERATION_PROMPT, PRODUCT_PAGE_PROMPT

class ContentGeneratorAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant")

        # Parsers
        self.faq_parser = PydanticOutputParser(pydantic_object=FAQObject)
        self.page_parser = PydanticOutputParser(pydantic_object=ProductPage)

    def generate_faq(self, product):
        schema = self.faq_parser.get_format_instructions()

        prompt = FAQ_GENERATION_PROMPT.format(
            product_name=product.name,
            product_data_json=product.model_dump_json(indent=2),
            format_instructions=schema
        )

        response = self.llm.invoke(prompt)
        return self.faq_parser.parse(response.content)

    def generate_product_page(self, product: dict) -> ProductPage:
        schema = self.page_parser.get_format_instructions()

        prompt = PRODUCT_PAGE_PROMPT.format(
            product_name=product.name,
            product_data_json=product.model_dump_json(indent=2),
            format_instructions=schema   # ← REQUIRED
        )

        response = self.llm.invoke(prompt)
        return self.page_parser.parse(response.content)
