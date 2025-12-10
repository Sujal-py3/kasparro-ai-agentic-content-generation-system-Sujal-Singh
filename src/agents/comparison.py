from typing import List, Tuple
from src.models import (
    ProductData, ComparisonDifferences, DifferenceSet
)

class ComparisonAgent:
    """
    Generates ComparisonPage data strictly using rule-based derivation.
    """

    def compare(self, product_a: ProductData) -> Tuple[ProductData, ComparisonDifferences, List[str]]:
        # 1. Derive Product B strictly from A (No hallucination)
        # It represents a "Standard" version.
        
        # Price derivation
        try:
            price_val = float(''.join(filter(str.isdigit, product_a.price)))
            price_b_val = int(price_val * 0.5)
            price_b = f"₹{price_b_val}"
        except:
            price_b = "₹300" 

        product_b = ProductData(
            name=f"Generic {product_a.name.split()[-1]}", # "Generic Serum"
            concentration="Standard Concentration", # Neutral factual statement
            skin_type=["All Skin Types"], # Standard generic claim
            key_ingredients=[product_a.key_ingredients[0]], # Helper: "Contains primary ingredient only"
            benefits=[product_a.benefits[0]], # "Primary benefit only"
            how_to_use="Apply daily.", # Standard generic usage
            side_effects="None listed", # Standard generic safety
            price=price_b
        )

        # 2. Logic: A Only, B Only, Common
        def get_diff_set(list_a: List[str], list_b: List[str]) -> DifferenceSet:
            set_a = set(list_a)
            set_b = set(list_b)
            return DifferenceSet(
                a_only=list(set_a - set_b),
                b_only=list(set_b - set_a),
                common=list(set_a.intersection(set_b))
            )

        diff_ingredients = get_diff_set(product_a.key_ingredients, product_b.key_ingredients)
        diff_benefits = get_diff_set(product_a.benefits, product_b.benefits)

        differences = ComparisonDifferences(
            ingredients=diff_ingredients,
            benefits=diff_benefits
        )

        # 3. Recommendations
        recommendation = []
        
        # Skin Type Logic
        if "All Skin Types" in product_b.skin_type:
             recommendation.append(f"Product A is targeted for {', '.join(product_a.skin_type)}, while Product B is for All Skin Types.")
        
        # Price Logic
        recommendation.append(f"Product B is cheaper at {product_b.price}.")

        return product_b, differences, recommendation
