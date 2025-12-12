# Project Documentation: Agentic Content Generation System

## 1. System Overview
This project is a modular, agentic system designed to automate the creation of high-quality marketing assets (Product Pages, FAQs, and Comparison Pages) from raw product data. It leverages **LangChain** and **Groq (Llama-3)** to understand semi-structured input and generate strictly compliant JSON outputs.

## 2. Architecture Design
The system follows a linear **LCEL (LangChain Expression Language)** pipeline architecture:

1.  **Ingestion & Analysis**: Raw data is parsed by the **Product Analyzer Agent** into a strict internal schema (`ProductData`).
2.  **Parallel Generation**: The structured data is broadcast to three specialized agents running in parallel:
    *   **Content Generator (FAQ)**: Generates categorized questions and detailed Q&A pairs.
    *   **Content Generator (Product Page)**: Generates marketing copy and structured usage instructions.
    *   **Comparison Generator**: Generates a fictional competitor (Product B) based on rule-based prompts and performs a feature-by-feature comparison.
3.  **Output**: JSON files are persisted to the `/out` directory.

## 3. Component Details

### 3.1 Data Models (`src/models.py`)
-   **`ProductData`**: The single source of truth for product information.
-   **`Usage`**: Structured step-by-step usage instructions.
-   **`FAQObject`**: Contains both `categorized_questions` (list of 15) and `faq_page` (top 5 Q&A).
-   **`ComparisonPage`**: Contains full data for Product A vs. Product B, differences, and recommendations.

### 3.2 Agents
-   **Product Analyzer**: Uses `ChatGroq` to extract entities without hallucination. strict schema enforcement via `PydanticOutputParser`.
-   **Content Generator**: 
    -   *FAQ Mode*: Generates 15 questions across specific categories (Usage, Safety, etc.).
    -   *Product Page Mode*: Focuses on copywriting and structuring instructions.
-   **Comparison Generator**: 
    -   Implements "Product B" generation logic (price +20%, distinct ingredients) via prompt engineering.

### 3.3 Orchestration (`src/orchestrator.py`)
-   Uses `RunnableSequence` (`|`) to pipe analysis results to generation.
-   Uses `RunnableParallel` to execute the three generation tasks concurrently.

## 4. Setup & Usage
1.  **Environment**: Ensure `GROQ_API_KEY` is set in `.env`.
2.  **Run**: `python src/main.py`
3.  **Output**: Check `out/faq.json`, `out/product_page.json`, `out/comparison_page.json`.
