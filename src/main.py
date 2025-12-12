import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Ensure src is in python path
sys.path.append(os.getcwd())

from src.orchestrator import Orchestrator

# EXACT DATASET FROM ASSIGNMENT — NO EXTRA FIELDS
SAMPLE_INPUT = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": ["Oily", "Combination"],
    "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
    "benefits": ["Brightening", "Fades dark spots"],
    "usage": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}

def main():
    print("Starting Multi-Agent Content System...")
    orchestrator = Orchestrator()

    try:
        results = orchestrator.run(SAMPLE_INPUT)
        orchestrator.save_results(results)
        print("Success! Check the 'out' directory.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
