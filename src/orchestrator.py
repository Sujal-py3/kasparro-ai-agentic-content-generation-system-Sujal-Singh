from typing import Dict, Any
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from src.agents.product_analyzer import ProductAnalyzerAgent
from src.agents.content_generator import ContentGeneratorAgent
from src.agents.comparison_generator import ComparisonGeneratorAgent
from src.models import ProductData

class Orchestrator:
    """
    Coordinates the multi-agent workflow using LangChain LCEL.
    Replaces imperative glue code with a direct Runnable pipeline.
    """
    def __init__(self):
        # Initialize Agents
        self.analyzer = ProductAnalyzerAgent()
        self.content_gen = ContentGeneratorAgent()
        self.comparison_gen = ComparisonGeneratorAgent()

    def run(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the full pipeline using LCEL.
        """
        print("[Orchestrator] Starting LCEL Pipeline...")

        # 1. Parsing Chain: Raw Dict -> ProductData
        # Explicitly wrapping the agent call as a RunnableLambda to fit into LCEL
        parse_step = RunnableLambda(self.analyzer.analyze)

        # 2. Parallel Generation Step
        # Accepts ProductData from previous step, runs 3 independent branches
        generation_step = RunnableParallel({
            "faq_output": RunnableLambda(lambda p: self.content_gen.generate_faq(p)), # Returns FAQObject
            "product_page": RunnableLambda(lambda p: self.content_gen.generate_product_page(p)), # Returns ProductPage
            "comparison_page": RunnableLambda(lambda p: self.comparison_gen.generate_comparison(p)) # Returns ComparisonPage
        })

        # 3. Overall Chain
        pipeline = parse_step | generation_step

        # Execute
        results = pipeline.invoke(raw_data)
        
        return results

    def save_results(self, results: Dict[str, Any], output_dir: str = "out"):
        """Helper to save results to JSON files in the specified directory."""
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save FAQ (handling the complex object)
        with open(os.path.join(output_dir, "faq.json"), "w", encoding="utf-8") as f:
            f.write(results["faq_output"].model_dump_json(indent=2))
            
        # Save Product Page
        with open(os.path.join(output_dir, "product_page.json"), "w", encoding="utf-8") as f:
            f.write(results["product_page"].model_dump_json(indent=2))

        # Save Comparison Page
        with open(os.path.join(output_dir, "comparison_page.json"), "w", encoding="utf-8") as f:
            f.write(results["comparison_page"].model_dump_json(indent=2))
        
        print(f"[Orchestrator] Results saved to {output_dir}/")
