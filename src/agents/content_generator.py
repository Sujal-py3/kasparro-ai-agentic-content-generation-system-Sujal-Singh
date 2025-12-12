from langchain_groq import ChatGroq
from langchain.output_parsers import PydanticOutputParser
from src.models import ProductData, FAQObject, ProductPage
from src.prompts import FAQ_GENERATION_PROMPT, PRODUCT_PAGE_PROMPT
import os

class ContentGeneratorAgent:
    """
    Agent responsible for generating content pages (FAQ, Product Page)
    using LLMs with strict adherence to Kasparro requirements.
    """
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant", api_key=api_key) # Moderate temp for creative but structured output
        self.faq_parser = PydanticOutputParser(pydantic_object=FAQObject)
        self.product_parser = PydanticOutputParser(pydantic_object=ProductPage)

        self.faq_chain = FAQ_GENERATION_PROMPT | self.llm | self.faq_parser
        self.product_chain = PRODUCT_PAGE_PROMPT | self.llm | self.product_parser

    def generate_faq(self, product: ProductData) -> FAQObject:
        print(f"[ContentGenerator] Generating grouped FAQs and Top 5 Q&A...")
        return self.faq_chain.invoke({
            "product_data_json": product.model_dump_json(),
            "format_instructions": self.faq_parser.get_format_instructions()
        })

    def generate_product_page(self, product: ProductData) -> ProductPage:
        print(f"[ContentGenerator] Generating Product Page with structured Usage...")
        return self.product_chain.invoke({
            "product_data_json": product.model_dump_json(),
            "format_instructions": self.product_parser.get_format_instructions()
        })
