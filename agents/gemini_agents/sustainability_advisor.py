from app.utils import init_gemini_model
from agents.gemini_agents.prompts import SUSTAINABILITY_SUGGESTIONS_PROMPT_TEMPLATE
import json
import re

model = init_gemini_model()

def suggest_sustainable_alternatives(items: list) -> dict:
    """
    Takes a list of consumed items and returns sustainable alternatives.

    Args:
        items (list): List of item names.

    Returns:
        dict: Recommendations with alternative, reason, and impact score
    """

    formatted_items = "\n- " + "\n- ".join(items)
    prompt = SUSTAINABILITY_SUGGESTIONS_PROMPT_TEMPLATE.format(items=formatted_items)

    try:
        response = model.generate_content(prompt, stream=False)
        raw = response.text.strip()
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
        parsed = json.loads(cleaned)
        if "recommendations" not in parsed:
            return {
                "error": "Response parsed, but 'recommendations' key missing.",
                "raw_output": raw
            }

        return parsed

    except Exception as e:
        return {
            "error": "Failed to parse Gemini response.",
            "raw_output": getattr(response, "text", "No response"),
            "exception": str(e)
        }
