from langchain.prompts import PromptTemplate


# --------------------------
# 1. PRODUCT ANALYSIS PROMPT
# --------------------------
PRODUCT_ANALYSIS_TEMPLATE = """
You are a strict structured-data extraction agent.

Your task:
- Parse ONLY the product fields given in the input.
- Do NOT infer or hallucinate.
- Do NOT add new ingredients, benefits, steps, or usage lines.
- Convert the product data into a structured, normalized internal model.

Use only these fields:
- name
- concentration
- skin_type
- key_ingredients
- benefits
- usage
- side_effects
- price

Input Product Data:
{raw_data}

Return a JSON object following EXACTLY this structure:

{format_instructions}
"""

PRODUCT_ANALYSIS_PROMPT = PromptTemplate(
    template=PRODUCT_ANALYSIS_TEMPLATE,
    input_variables=["raw_data"],
    partial_variables={"format_instructions": ""},
)



# --------------------------
# 2. FAQ GENERATION PROMPT
# --------------------------
FAQ_GENERATION_TEMPLATE = """
You are a content generation agent.

Your job:
1. Generate **at least 15 user questions**, grouped into categories.
2. Categories can include: Usage, Safety, Ingredients, Benefits, Purchase, Comparison.
3. Generate **5 Q&A pairs** for the FAQ page.
4. Use ONLY the provided product data — no external facts.

Product Name: {product_name}
Product Data:
{product_data_json}

RETURN STRUCTURED JSON ONLY:

{format_instructions}
"""

FAQ_GENERATION_PROMPT = PromptTemplate(
    template=FAQ_GENERATION_TEMPLATE,
    input_variables=["product_name", "product_data_json"],
    partial_variables={"format_instructions": ""},
)



# --------------------------
# 3. PRODUCT PAGE PROMPT
# --------------------------
PRODUCT_PAGE_TEMPLATE = """
You are a content assembly agent.

Task:
- Build a structured product page.
- Use ONLY the given product data.
- Do NOT add claims or ingredients.
- Format usage as a STRING, not a list.
- Ensure machine-readable JSON.

Product Data:
{product_data_json}

Return JSON matching this schema:

{format_instructions}
"""

PRODUCT_PAGE_PROMPT = PromptTemplate(
    template=PRODUCT_PAGE_TEMPLATE,
    input_variables=["product_data_json"],
    partial_variables={"format_instructions": ""},
)



# --------------------------
# 4. COMPARISON PAGE PROMPT
# --------------------------
COMPARISON_TEMPLATE = """
You are a comparison agent.

Task:
- Compare Product A with a fictional Product B.
- Product B must:
  - be fully fictional
  - follow same field structure as Product A
  - NOT include any externally researched facts
  - be logically consistent and simple
- Return:
  1. Product B (structured JSON)
  2. Differences (ingredients, benefits)
  3. Recommendations list

Product A:
{product_a_json}

Competitor Context:
{product_b_context}

Return ONLY structured JSON:

{format_instructions}
"""

COMPARISON_PROMPT = PromptTemplate(
    template=COMPARISON_TEMPLATE,
    input_variables=["product_a_json", "product_b_context"],
    partial_variables={"format_instructions": ""},
)
