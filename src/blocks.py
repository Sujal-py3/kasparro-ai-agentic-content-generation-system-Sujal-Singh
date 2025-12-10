from typing import List

def generate_short_description_block(name: str, concentration: str, skin_types: List[str], benefits: List[str]) -> str:
    """
    Generates short description strictly matching template:
    {product_name} — {concentration} formulation for {skin types}. Key benefits: {benefits}.
    """
    skin_types_str = ", ".join(skin_types)
    benefits_str = ", ".join(benefits)
    return f"{name} — {concentration} formulation for {skin_types_str}. Key benefits: {benefits_str}."

def generate_safety_block(side_effects: str) -> List[str]:
    """Generates safety block including required patch test recommendation."""
    notes = []
    if side_effects:
        notes.append(side_effects)
    # STRICT EXACT MATCH as per feedback
    notes.append("Patch test recommended for sensitive skin.")
    return notes

def determine_category(question_text: str) -> str:
    """
    Categorizes questions strictly.
    """
    q = question_text.lower()
    if any(x in q for x in ["safe", "reaction", "tingl", "harm", "effect", "patch"]):
        return "Safety"
    if any(x in q for x in ["use", "apply", "routine", "morning", "night", "trouble", "mix", "drops"]):
        return "Usage"
    if any(x in q for x in ["price", "cost", "buy", "purchase", "available"]):
        return "Purchase"
    if any(x in q for x in ["compare", "better", "difference", "vs", "other"]):
        return "Comparison"
    return "Informational"

def format_usage_block(usage_text: str) -> str:
    return usage_text

def format_price_block(price_text: str) -> str:
    return price_text
