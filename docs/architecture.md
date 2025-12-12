# Architecture Document: LangChain-Based Content System

## Overview
This project implements a **multi-agent automation system** to generate structured marketing content (FAQ, Product Pages, Comparisons) from raw product data. It utilizes **LangChain** for orchestration and agent logic, ensuring a robust, scalable, and model-driven approach.

## Core Design Principles
1.  **Framework-First**: Orchestration and agent interactions are managed via **LangChain** and **LCEL** (LangChain Expression Language), replacing custom imperative code.
2.  **Strict Structured Output**: All agents use `PydanticOutputParser` to guarantee valid JSON output that matches predefined schemas (`FAQPage`, `ProductPage`, `ComparisonPage`).
3.  **Model-Driven Content**: Content generation (copywriting, question generation, comparative analysis) is performed by LLMs (`gpt-4-turbo`), not hardcoded templates.

## System Components

### 1. Product Analyzer Agent
*   **Role**: Ingests raw, unstructured input data and converts it into a standardized internal model (`ProductData`).
*   **Mechanism**: Uses a LangChain Chain with a `PydanticOutputParser` to strictly extract fields like price, ingredients, and usage.

### 2. Content Generator Agent
*   **Role**: Creates user-facing content based on the analyzed product data.
*   **Capabilities**:
    *   **FAQ Generation**: Generates relevant questions and answers categorized by topic.
    *   **Product Page Copy**: Writes marketing copy, short descriptions, and safety warnings.

### 3. Comparison Generator Agent
*   **Role**: Conducts competitive analysis.
*   **Mechanism**: uses an LLM to generate a realistic competitor (if none provided) and identifies key differences (Ingredients, Benefits) and recommendations.

### 4. Orchestrator (LCEL Pipeline)
*   **Role**: Manages the flow of data between agents.
*   **Flow**:
    1.  **Parse**: Raw Data → `ProductAnalyzer` → `ProductData`
    2.  **Parallel Execution**: `ProductData` is broadcast to:
        *   `ContentGenerator` (FAQ)
        *   `ContentGenerator` (Product Page)
        *   `ComparisonGenerator` (Comparison Page)
    3.  **Aggregation**: Results are collected into a final dictionary.

## Data Flow Diagram

```mermaid
graph TD
    Input[Raw Input Data] --> Analyzer[Product Analyzer Agent]
    Analyzer -->|ProductData| Split((Parallel Execution))
    
    Split --> FAQ[Content Generator<br>(FAQ Chain)]
    Split --> Prod[Content Generator<br>(Product Page Chain)]
    Split --> Comp[Comparison Generator<br>(Comparison Chain)]
    
    FAQ --> OutputFAQ[FAQPage JSON]
    Prod --> OutputProd[ProductPage JSON]
    Comp --> OutputComp[ComparisonPage JSON]
```

## Technology Stack
*   **Language**: Python 3.10+
*   **Framework**: LangChain, LangChain-Groq
*   **Models**: Groq (Llama-3.1 8B Instant)
*   **Validation**: Pydantic v2
