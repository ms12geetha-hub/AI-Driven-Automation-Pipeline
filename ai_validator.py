import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def ai_validate_invoice(extracted_data, corrected_text):
    """
    AI layer for semantic validation & reasoning.

    Uses cleaned/corrected invoice fields to avoid reporting OCR mistakes.
    """
    prompt = f"""
You are an enterprise invoice verification AI.

Corrected invoice data:
{json.dumps(extracted_data, indent=2)}

Corrected invoice text for reasoning:
{corrected_text}

Tasks:
1. Check if this document is a valid invoice
2. Identify any potential risks
3. Provide confidence score (0-100)
4. Recommend one action: Approved / Needs Review / Rejected

Respond ONLY in JSON format:
{{
    "ai_reasoning": "...",
    "ai_recommendation": "...",
    "ai_confidence": number
}}
"""

    response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,
    messages=[
        {"role": "system", "content": "You are a financial compliance and document verification expert."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

    # Corrected access
    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"ai_reasoning": content, "ai_recommendation": "Needs Review", "ai_confidence": 50}


