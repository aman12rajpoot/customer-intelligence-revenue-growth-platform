import logging
import os
from typing import Any, Dict

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a Senior Customer Intelligence and Revenue Growth Consultant.

Your role is to help businesses:

• Reduce customer churn
• Increase customer lifetime value (CLV)
• Protect revenue at risk
• Improve customer retention
• Recommend actionable business strategies

Your recommendations should be:

- Professional
- Concise
- Business focused
- Actionable
- Executive friendly

Do not invent customer information.
Base every recommendation only on the supplied customer data.
"""


def build_business_prompt(row: Dict[str, Any]) -> str:
    """
    Creates the business prompt sent to the LLM.
    """

    return f"""
Analyze the following customer profile and provide an executive business recommendation.

Customer Information
--------------------

Customer ID: {int(row['CustomerID'])}

Segment: {row.get('Segment', 'Unknown')}

Customer Persona: {row.get('Customer_Persona', 'Unknown')}

Churn Probability: {row.get('Churn_Probability', 0):.2%}

Predicted Customer Lifetime Value: ${row.get('Predicted_CLV', 0):,.2f}

Revenue at Risk: ${row.get('Revenue_at_Risk', 0):,.2f}

Risk Category: {row.get('Risk_Category', 'Unknown')}

Recommended Action: {row.get('Customer_Action', 'Monitor')}


Generate:

1. Executive Summary

2. Business Risk

3. Recommended Retention Strategy

4. Expected Business Impact

Keep the response under 200 words.
"""


def generate_business_recommendation(row: Dict[str, Any]) -> str:
    """
    Generates an AI-powered business recommendation using Groq.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    model_name = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile",
    )

    prompt = build_business_prompt(row)

    try:

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=300,
        )

        recommendation = response.choices[0].message.content.strip()

        logger.info(
            "Recommendation generated successfully for Customer %s",
            row.get("CustomerID"),
        )

        return recommendation

    except Exception as e:

        logger.error("Groq API Error: %s", e)

        raise RuntimeError(
            f"Unable to generate AI recommendation.\n{e}"
        )