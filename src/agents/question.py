from typing import List
from src.models import ProductData, FAQEntry
from src.blocks import determine_category

class QuestionGeneratorAgent:
    """
    Generates 15+ structured questions by granularizing strictly available data.
    """

    def generate(self, product: ProductData) -> List[FAQEntry]:
        questions: List[FAQEntry] = []

        def add_q(q_text: str, ans_text: str):
            questions.append(FAQEntry(
                question=q_text,
                answer=ans_text,
                category=determine_category(q_text)
            ))

        # 1. Name & Concentration
        add_q(f"What is the name of this product?", product.name)
        add_q(f"What is the concentration?", product.concentration)

        # 2. Ingredients (Granular)
        add_q("What are the key ingredients?", ", ".join(product.key_ingredients))
        for i, ingredient in enumerate(product.key_ingredients):
             add_q(f"Does it contain {ingredient}?", f"Yes, it contains {ingredient}.")
        
        # 3. Use of Ingredients (Logic derivation)
        if "Vitamin C" in product.key_ingredients:
             add_q("Is Vitamin C a key ingredient?", "Yes, Vitamin C is a key ingredient.")

        # 4. Benefits (Granular)
        add_q("What are the main benefits?", ", ".join(product.benefits))
        for benefit in product.benefits:
             add_q(f"Does it help with {benefit}?", f"Yes, it helps with {benefit}.")

        # 5. Skin Type (Granular)
        add_q("Which skin types is this suitable for?", ", ".join(product.skin_type))
        for st in product.skin_type:
            add_q(f"Is it suitable for {st} skin?", f"Yes, it is suitable for {st}.")

        # 6. Usage (Granular split of "Apply 2–3 drops in the morning before sunscreen")
        add_q("How should I use this product?", product.how_to_use)
        if "2–3 drops" in product.how_to_use:
             add_q("How many drops should I apply?", "Apply 2–3 drops.")
        if "morning" in product.how_to_use.lower():
             add_q("When should I apply this?", "Apply in the morning.")
        if "sunscreen" in product.how_to_use.lower():
             add_q("Should I use sunscreen after?", "Yes, apply before sunscreen.")

        # 7. Safety / Side Effects
        add_q("Are there any side effects?", product.side_effects)
        if "tingling" in product.side_effects.lower():
             add_q("Is tingling normal?", product.side_effects)
        
        # 8. Price
        add_q("How much does it cost?", product.price)

        return questions
