import json

from app.config import settings
from app.services.fallback import fallback


try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None


def generate(
    planner,
    data,
    image_bytes=None,
    mime_type="image/jpeg"
):
    fallback_result = fallback(
        planner,
        data
    )

    if (
        not settings.gemini_api_key
        or genai is None
    ):
        return fallback_result

    prompt = f"""
You are PocketSmart AI.

Create a practical budget plan in Indian Rupees.

Planner:
{planner}

User input:
{json.dumps(data, ensure_ascii=False)}

Requirements:

1. Keep recommendations budget-aware.
2. Keep total_estimate within the budget when possible.
3. Give realistic estimated prices.
4. Use platform labels such as:
   Amazon, Flipkart, IKEA, Swiggy,
   Zomato or OYO where relevant.
5. Do not claim that you actually queried
   those platforms.
6. Provide platform search URLs.
7. Return only JSON.

Required JSON keys:

planner
budget
total_estimate
remaining_budget
summary
allocations
recommendations

Each recommendation must contain:

name
category
estimated_price
platform
url
reason
"""

    try:

        contents = [prompt]

        if image_bytes and types:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                )
            )

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.35,
            ),
        )

        result = json.loads(response.text)

        result["source"] = "gemini"
        result["request"] = data

        if image_bytes:
            result["image_analysis"] = (
                "Gemini analyzed the uploaded "
                "outfit image."
            )

        return result

    except Exception as error:

        fallback_result["warning"] = (
            "Gemini request failed. "
            f"Fallback mode used: "
            f"{type(error).__name__}"
        )

        return fallback_result