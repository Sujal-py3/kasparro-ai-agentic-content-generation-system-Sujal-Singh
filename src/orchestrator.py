import os
from typing import Dict, Any
from src.agents.parser import ParserAgent
from src.agents.question import QuestionGeneratorAgent
from src.agents.comparison import ComparisonAgent
from src.agents.assembler import AssemblerAgent

class Orchestrator:
    """
    Coordinates the multi-agent workflow.
    """
    def __init__(self):
        self.parser = ParserAgent()
        self.question_gen = QuestionGeneratorAgent()
        self.comparison_gen = ComparisonAgent()
        self.assembler = AssemblerAgent()

    def run(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the full pipeline.
        Returns a dictionary containing the generated page models.
        """
        # Step 1: Parse
        print("[Orchestrator] Parsing input data...")
        product = self.parser.parse(raw_data)

        # Step 2: Generate Content (Conceptually Parallel)
        print("[Orchestrator] Generating questions...")
        faq_items = self.question_gen.generate(product)
        
        print("[Orchestrator] Generating comparison..." )
        product_b, differences, recommendation = self.comparison_gen.compare(product)

        # Step 3: Assemble
        print("[Orchestrator] Assembling pages...")
        faq_page = self.assembler.assemble_faq(faq_items, product.name)
        product_page = self.assembler.assemble_product_page(product)
        comparison_page = self.assembler.assemble_comparison_page(
            product, product_b, differences, recommendation
        )

        return {
            "faq": faq_page,
            "product": product_page,
            "comparison": comparison_page
        }

    def save_results(self, results: Dict[str, Any], output_dir: str = "output"):
        """Helper to save results to JSON files."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save FAQ
        with open(os.path.join(output_dir, "faq.json"), "w", encoding="utf-8") as f:
            f.write(results["faq"].model_dump_json(indent=2))
            
        # Save Product Page
        with open(os.path.join(output_dir, "product_page.json"), "w", encoding="utf-8") as f:
            f.write(results["product"].model_dump_json(indent=2))

        # Save Comparison Page
        with open(os.path.join(output_dir, "comparison_page.json"), "w", encoding="utf-8") as f:
            f.write(results["comparison"].model_dump_json(indent=2))
        
        print(f"[Orchestrator] Results saved to {output_dir}/")
