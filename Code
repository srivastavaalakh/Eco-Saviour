# Prompt for receipt analysis
RECEIPT_PARSING_PROMPT = """
You are an expert in sustainable product tracking. Analyze this receipt image and extract a structured list of purchased items.

For each item, return:
- Item name
- Quantity (if mentioned)
- Category (e.g., food, clothing, electronics)
- Packaging type (e.g., plastic, cardboard, cloth, unknown)

Respond in the following JSON format:

{
  "items": [
    {
      "name": "Milk",
      "quantity": 1,
      "category": "food",
      "packaging": "plastic"
    }
  ]
}
"""

# Prompt for trash classification
TRASH_ANALYSIS_PROMPT = """
You are an expert in waste management. Given a photo, identify all visible items
and for each one, return:

- Name of item
- Type of material (plastic, paper, metal, organic, glass, etc.)
- Recyclability: Yes / No / Unknown
- Brief reason

Respond in JSON format:

{
  "items": [
    {
      "name": "Plastic bottle",
      "material": "plastic",
      "recyclable": "Yes",
      "reason": "PET bottles are commonly recycled"
    }
  ]
}
"""

# Prompt for sustainability suggestions
SUSTAINABILITY_SUGGESTIONS_PROMPT_TEMPLATE = """
You are an AI sustainability advisor. A user has recently consumed or used the following items:

{items}

For each item, suggest:
- A more eco-friendly alternative (e.g., reusable, lower-impact version)
- A short reason why it's more sustainable
- Impact score (1 to 5, where 5 = high environmental benefit)

Respond in this format:

{{
  "recommendations": [
    {{
      "original": "Plastic water bottle",
      "alternative": "Stainless steel bottle",
      "reason": "Reusable and reduces single-use plastic",
      "impact_score": 5
    }}
  ]
}}
"""
