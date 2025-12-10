import sys
import os

# Ensure src is in python path if running from root
sys.path.append(os.getcwd())

from src.orchestrator import Orchestrator

# EXACT DATASET FROM USER FEEDBACK with EN-DASH
SAMPLE_INPUT = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": "Oily, Combination",
    "key_ingredients": "Vitamin C, Hyaluronic Acid",
    "benefits": "Brightening, Fades dark spots",
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen", # En-dash used here
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699", 
    "currency": "INR"
}

def main():
    print("Starting Multi-Agent Content System...")
    orchestrator = Orchestrator()
    try:
        results = orchestrator.run(SAMPLE_INPUT)
        orchestrator.save_results(results)
        print("Success! Check the 'output' directory.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
