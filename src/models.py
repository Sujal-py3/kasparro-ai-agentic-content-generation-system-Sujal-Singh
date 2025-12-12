from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# -----------------------------
# 1. INTERNAL PRODUCT MODEL
# -----------------------------
class ProductData(BaseModel):
    name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    usage: str
    side_effects: str
    price: str


# -----------------------------
# 2. FAQ STRUCTURES
# -----------------------------

class FAQPair(BaseModel):
    question: str
    answer: str


class FAQObject(BaseModel):
    title: str = Field(..., description="Page title")
    categorized_questions: Dict[str, List[str]] = Field(
        ..., description="15+ questions grouped by category"
    )
    faq_page: List[FAQPair] = Field(
        ..., description="Top 5 Q&A pairs used for the public FAQ page"
    )


# -----------------------------
# 3. PRODUCT PAGE STRUCTURE
# -----------------------------
class ProductPage(BaseModel):
    page_type: str = Field(..., description="Should always be 'product_page'")
    title: str
    short_description: str
    benefits: List[str]
    ingredients: List[str]
    usage: str  # must be a string (important fix)
    safety: List[str]
    price: str


# -----------------------------
# 4. COMPARISON STRUCTURES
# -----------------------------
class ComparisonProduct(BaseModel):
    name: str
    key_ingredients: List[str]
    benefits: List[str]
    price: str


class ComparisonPage(BaseModel):
    page_type: str = Field(..., description="Should always be 'comparison_page'")
    product_a: ProductData
    product_b: ComparisonProduct
    differences: Dict[str, List[str]]
    recommendations: List[str]
