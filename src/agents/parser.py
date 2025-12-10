from typing import Dict, List, Any
from src.models import ProductData

class ParserAgent:
    """Agent responsible for cleaning and parsing raw input into ProductData."""

    def parse(self, raw_data: Dict[str, Any]) -> ProductData:
        """
        Parses raw dictionary into ProductData model.
        """
        
        def parse_list(key: str) -> List[str]:
            val = raw_data.get(key, [])
            if isinstance(val, str):
                return [item.strip() for item in val.split(",")]
            return val

        return ProductData(
            name=raw_data.get("name", "").strip(),
            concentration=raw_data.get("concentration", "").strip(),
            skin_type=parse_list("skin_type"), # NOW A LIST
            key_ingredients=parse_list("key_ingredients"),
            benefits=parse_list("benefits"),
            how_to_use=raw_data.get("how_to_use", "").strip(),
            side_effects=raw_data.get("side_effects", "").strip(),
            price=str(raw_data.get("price", "")).strip()
        )
