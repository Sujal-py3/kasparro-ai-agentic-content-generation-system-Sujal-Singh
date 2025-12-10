# Kasparro Multi-Agent Content Generation System - Documentation

## Problem Statement
The goal is to design and implement a modular agentic automation system that accepts raw product data (e.g., "GlowBoost Vitamin C Serum") and autonomously generates structured, machine-readable content pages: an FAQ page, a Product Description page, and a Comparison page. The system must use a multi-agent workflow, ensuring separation of concerns, modularity, and reusable logic.

## Solution Overview
The solution is a Python-based multi-agent pipeline orchestrated as a Directed Acyclic Graph (DAG). It uses a "Model-View-Controller" inspired approach but for Agents:
- **Models**: Pydantic data structures defining the strict schema for Input and Output.
- **Agents (Controllers)**: Specialized workers that perform specific cognitive tasks (Parsing, Question Generation, Comparison).
- **Templates (Views)**: Structured definitions that the Agents fill to produce the final output.

The system is designed to be extensible. Adding a new page type (e.g., "Blog Post") only requires adding a new Template and potentially a new specialized Agent, without modifying the core orchestrator or existing agents.

## Scopes & Assumptions
- **Scope**:
    - Input: A specific JSON-like product dataset.
    - Output: 3 JSON files (FAQ, Product, Comparison).
    - Agents: Parser, Question Generator, Comparison, Assembler.
    - No external research triggers (Agents work with provided logic/knowledge or simulated expansion).
- **Assumptions**:
    - The environment has access to an LLM (OpenAI style) or a Mock LLM for testing.
    - The input format is consistent (key-value pairs).
    - "Product B" for comparison is generated creatively by the agent based on the input product's category.

## System Design

### Architecture Diagram (Textual)
```mermaid
graph TD
    Input[Raw Product Data] --> ParserAgent
    ParserAgent -->|ProductData Model| Orchestrator
    
    Orchestrator --> QuestionAgent
    Orchestrator --> ComparisonAgent
    Orchestrator --> AssemblerAgent
    
    ProductData Model -.-> QuestionAgent
    ProductData Model -.-> ComparisonAgent
    
    QuestionAgent -->|List[FAQItem]| AssemblerAgent
    ComparisonAgent -->|ComparisonData| AssemblerAgent
    
    AssemblerAgent -->|Templates + Logic| OutputFiles
    
    subgraph OutputFiles
        FAQ[faq.json]
        Product[product_page.json]
        Comparison[comparison_page.json]
    end
```

### Core Components
1.  **Orchestrator**: The central nervous system. It initializes agents, passes data between them, and handles the execution flow.
2.  **Shared Models (`src/models.py`)**: Defines `ProductData`, `FAQItem`, `ComparisonPoint`, ensuring type safety across agent boundaries.
3.  **Content Logic Blocks (`src/blocks.py`)**: Pure functions that encapsulate business logic (e.g., `calculate_discount`, `format_ingredients`). These are used by agents to "ground" their seemingly creative work.
4.  **Agents**:
    - `ParserAgent`: Cleans input.
    - `QuestionGeneratorAgent`: Uses LLM to brainstorm relevant questions based on user persona and product attributes.
    - `ComparisonAgent`: Hallucinates a competitor and creates a feature-by-feature comparison.
    - `AssemblerAgent`: Takes the structured partial results and the original data, applies templates, and renders the final JSON.

### Data Flow
1.  **Ingestion**: Raw text -> `ParserAgent` -> `ProductData` object.
2.  **Expansion**:
    - `ProductData` -> `QuestionGeneratorAgent` -> `[FAQItem]`
    - `ProductData` -> `ComparisonAgent` -> `ComparisonObject`
3.  **Assembly**:
    - `ProductData` + `[FAQItem]` -> `Assembler` (FAQ Template) -> `faq.json`
    - `ProductData` -> `Assembler` (Product Template) -> `product_page.json`
    - `ProductData` + `ComparisonObject` -> `Assembler` (Comparison Template) -> `comparison_page.json`

## Agent Responsibilities
- **Parser Agent**: robustly handle messy inputs, normalize units (e.g., "10%" -> 0.10 if needed).
- **Question Generator**: Focus on user intent (Safety, Efficacy, Value).
- **Comparison Agent**: Focus on differentiation.
- **Assembler**: Focus on formatting and structure compliance.
