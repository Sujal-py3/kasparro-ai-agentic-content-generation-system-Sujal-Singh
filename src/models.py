from typing import List, Dict, Any
from pydantic import BaseModel

# --- Internal Data Models ---

class ProductData(BaseModel):
    """Internal model for the product data."""
    name: str
    concentration: str
    skin_type: List[str] # Changed to LIST per feedback
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: str 

class DifferenceSet(BaseModel):
    """Set of differences for a specific feature category."""
    a_only: List[str]
    b_only: List[str]
    common: List[str]

class ComparisonDifferences(BaseModel):
    """Strict structure for comparison differences."""
    ingredients: DifferenceSet
    benefits: DifferenceSet

# --- Output Models ---

class FAQEntry(BaseModel):
    question: str
    answer: str
    category: str 

class FAQPage(BaseModel):
    page_type: str = "faq"
    title: str
    entries: List[FAQEntry]

class ProductPage(BaseModel):
    page_type: str = "product_page"
    title: str
    short_description: str
    benefits: List[str]
    ingredients: List[str]
    usage: str
    safety: List[str]
    price: str

class ComparisonPage(BaseModel):
    page_type: str = "comparison_page"
    title: str
    product_a: ProductData
    product_b: ProductData
    differences: ComparisonDifferences
    recommendation: List[str]
