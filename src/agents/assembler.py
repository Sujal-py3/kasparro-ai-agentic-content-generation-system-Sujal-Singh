from typing import List
from src.models import (
    ProductData, FAQEntry, FAQPage, 
    ProductPage, ComparisonPage, ComparisonDifferences
)
from src.blocks import (
    generate_short_description_block,
    generate_safety_block
)

class AssemblerAgent:
    """
    Assembles final pages strictly.
    """

    def assemble_faq(self, items: List[FAQEntry], product_name: str) -> FAQPage:
        return FAQPage(
            title=f"FAQ - {product_name}",
            entries=items
        )

    def assemble_product_page(self, product: ProductData) -> ProductPage:
        return ProductPage(
            title=product.name,
            short_description=generate_short_description_block(
                product.name, product.concentration, product.skin_type, product.benefits
            ),
            benefits=product.benefits,
            ingredients=product.key_ingredients,
            usage=product.how_to_use,
            safety=generate_safety_block(product.side_effects),
            price=product.price
        )

    def assemble_comparison_page(
        self, 
        product_a: ProductData, 
        product_b: ProductData, 
        differences: ComparisonDifferences,
        recommendation: List[str]
    ) -> ComparisonPage:
        
        return ComparisonPage(
            title=f"Comparison: {product_a.name} vs {product_b.name}",
            product_a=product_a,
            product_b=product_b,
            differences=differences,
            recommendation=recommendation
        )
