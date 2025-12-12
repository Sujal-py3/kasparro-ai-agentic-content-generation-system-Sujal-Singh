from langchain.prompts import PromptTemplate


# ============================
# 1. PRODUCT ANALYSIS PROMPT
# ============================
PRODUCT_ANALYSIS_TEMPLATE = """
You are a strict structured-data extraction agent.

Rules:
- Parse ONLY the provided fields.
- Do NOT infer or add new information.
- Use values exactly as they appear.
- Output JSON only.

Input Product Data:
{raw_data}

Return JSON matching this schema:
{format_instructions}

Return ONLY valid JSON.
"""

PRODUCT_ANALYSIS_PROMPT = PromptTemplate(
    template=PRODUCT_ANALYSIS_TEMPLATE,
    input_variables=["raw_data"],
    partial_variables={"format_instructions": ""}
)



# ============================
# 2. FAQ GENERATION PROMPT
# ============================
FAQ_GENERATION_TEMPLATE = """
You are a structured FAQ generation agent.

Your tasks:
1. Generate AT LEAST 15 user questions grouped into categories.
2. Generate EXACTLY 5 Q&A pairs for the FAQ page.
3. Use ONLY the provided product data.
4. Return a JSON object strictly matching schema.

Product Name: {product_name}
Product Data:
{product_data_json}

You MUST output JSON matching EXACTLY this schema:

{format_instructions}

Return ONLY valid JSON.
"""



FAQ_GENERATION_PROMPT = PromptTemplate(
    template=FAQ_GENERATION_TEMPLATE,
    input_variables=["product_name", "product_data_json", "format_instructions"]
)




# ============================
# 3. PRODUCT PAGE PROMPT
# ============================
PRODUCT_PAGE_TEMPLATE = """
You are a structured product-page generation agent.

Rules:
- Use ONLY the provided product data.
- usage MUST be a STRING.
- No extra claims.
- No markdown.
- Output ONLY JSON.

Product Data:
{product_data_json}

Return JSON following EXACTLY this structure:

{format_instructions}
"""


PRODUCT_PAGE_PROMPT = PromptTemplate(
    template=PRODUCT_PAGE_TEMPLATE,
    input_variables=["product_data_json"],
    partial_variables={"format_instructions": ""}
)



# ============================
# 4. COMPARISON PAGE PROMPT
# ============================
COMPARISON_TEMPLATE = """
You are a structured product comparison agent.

Rules:
- Product B must be fictional.
- Must follow SAME structure as ProductData.
- No external facts.
- Differences must be a dict of lists.
- Return JSON only.

Product A:
{product_a_json}

Context for generating Product B:
{product_b_context}

Return ONLY JSON that matches exactly this format:

{format_instructions}
"""


COMPARISON_PROMPT = PromptTemplate(
    template=COMPARISON_TEMPLATE,
    input_variables=["product_a_json", "product_b_context"],
    partial_variables={"format_instructions": ""}
)
