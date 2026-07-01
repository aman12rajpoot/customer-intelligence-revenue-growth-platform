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

Your responsibility is to help businesses make data-driven customer retention decisions.

Your objectives are to:
• Reduce customer churn
• Increase Customer Lifetime Value (CLV)
• Protect revenue at risk
• Improve customer retention
• Recommend practical business actions.

Rules:

1. Use ONLY the customer information provided.
2. Never invent customer attributes, financial values, benchmarks, or business metrics.
3. Never estimate:
   - ROI
   - Revenue increase
   - Revenue savings
   - Retention percentage
   - Churn reduction percentage
   - Conversion rate
   - Industry benchmarks
   - Financial projections
4. If customer information is missing, clearly mention that additional customer data would improve the recommendation.
5. Keep recommendations realistic, practical, and suitable for business stakeholders.
6. Focus only on actionable retention strategies supported by the supplied customer data.

Your tone should always be:
- Professional
- Executive-friendly
- Business-focused
- Concise
- Action-oriented

Return your response using exactly these headings:

1. Executive Summary
2. Business Risk
3. Recommended Retention Strategy
4. Expected Business Impact

The Expected Business Impact section must only describe qualitative business outcomes.
Do NOT include numerical projections unless those numbers are explicitly provided in the customer data.
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

Predicted Customer Lifetime Value (CLV): ${row.get('Predicted_CLV', 0):,.2f}

Revenue at Risk: ${row.get('Revenue_at_Risk', 0):,.2f}

Risk Category: {row.get('Risk_Category', 'Unknown')}

Recommended Action: {row.get('Customer_Action', 'Monitor')}


Generate the response using the following structure.

## Executive Summary
Summarize the customer's current business situation in 2–3 sentences.

## Business Risk
Explain the customer's business risk using ONLY the supplied information.
Do not use industry averages or benchmarks.

## Recommended Retention Strategy
Provide 3–5 practical business recommendations that align with:
- Churn Probability
- Customer Lifetime Value
- Revenue at Risk
- Risk Category
- Recommended Action

Recommendations should be realistic, actionable, and suitable for business executives.

## Expected Business Impact
Describe only qualitative business outcomes such as:
- Improved customer engagement
- Better retention opportunities
- Protection of customer value
- More personalized customer experience

Do NOT estimate:
- ROI
- Revenue increase
- Revenue savings
- Retention percentage
- Churn reduction percentage
- Conversion rate
- Financial projections
- Industry benchmarks

If Segment or Customer Persona is Unknown, mention that additional customer information would improve future recommendations.

Keep the entire response under 180 words.
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
        "openai/gpt-oss-120b",
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
            temperature=0.1,
            max_tokens=500,
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