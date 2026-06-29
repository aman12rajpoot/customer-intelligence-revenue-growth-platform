"""
Predictor Module

Real-Time Customer Intelligence Engine

Pipeline

Raw Transaction Data
        │
        ▼
Data Cleaning
        │
        ▼
RFM Feature Engineering
        │
        ▼
Customer Persona Prediction
        │
        ▼
Churn Prediction
        │
        ▼
CLV Prediction
        │
        ▼
Revenue-at-Risk
        │
        ▼
Business Output

Author : Aman Rajpoot
"""

from pathlib import Path
from typing import Dict, Any

import logging
import joblib
import pandas as pd

from utils.data_cleaning import clean_transaction_data
from utils.feature_engineering import calculate_rfm

# ==========================================================
# Logging Configuration
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==========================================================
# Project Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT_DIR / "models"

# ==========================================================
# Model Paths
# ==========================================================

CHURN_MODEL_PATH = MODEL_DIR / "churn_prediction_pipeline.pkl"

CLV_MODEL_PATH = MODEL_DIR / "clv_prediction_pipeline.pkl"

PERSONA_MODEL_PATH = MODEL_DIR / "customer_persona_model.pkl"

PERSONA_SCALER_PATH = MODEL_DIR / "persona_scaler.pkl"

# ==========================================================
# Persona Mapping
# ==========================================================

PERSONA_MAPPING = {
    0: "Dormant Customers",
    1: "Active Customers",
    2: "VIP Customers",
}

# ==========================================================
# Verify Model Files
# ==========================================================

required_models = [
    CHURN_MODEL_PATH,
    CLV_MODEL_PATH,
    PERSONA_MODEL_PATH,
    PERSONA_SCALER_PATH,
]

for model_path in required_models:

    if not model_path.exists():

        raise FileNotFoundError(
            f"Model file not found:\n{model_path}"
        )

# ==========================================================
# Load Models
# ==========================================================

logger.info("Loading trained ML models...")

try:

    churn_pipeline = joblib.load(CHURN_MODEL_PATH)

    clv_pipeline = joblib.load(CLV_MODEL_PATH)

    persona_model = joblib.load(PERSONA_MODEL_PATH)

    persona_scaler = joblib.load(PERSONA_SCALER_PATH)

    logger.info("All models loaded successfully.")

except Exception as e:

    logger.exception("Failed to load models.")

    raise RuntimeError(
        f"Unable to load ML models.\n{e}"
    )

# ==========================================================
# Revenue-at-Risk Thresholds
# ==========================================================

HIGH_RISK_THRESHOLD = 0.70

MEDIUM_RISK_THRESHOLD = 0.40




# ==========================================================
# Customer Persona Prediction
# ==========================================================

def predict_persona(rfm_row: pd.DataFrame) -> str:
    """
    Predict Customer Persona using the trained
    KMeans clustering model.
    """

    required_columns = [
        "Recency",
        "Frequency",
        "Monetary",
    ]

    missing = [
        col for col in required_columns
        if col not in rfm_row.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns for Persona Prediction: {missing}"
        )

    features = rfm_row[required_columns]

    scaled_features = persona_scaler.transform(features)

    cluster = int(
        persona_model.predict(scaled_features)[0]
    )

    return PERSONA_MAPPING.get(
        cluster,
        "Unknown Customer"
    )


# ==========================================================
# Churn Prediction
# ==========================================================

def predict_churn(
    prediction_df: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Predict churn probability and churn class.
    """

    required_columns = [
        "Recency",
        "Frequency",
        "Monetary",
        "Average_Order_Value",
        "Customer_Persona",
    ]

    missing = [
        col for col in required_columns
        if col not in prediction_df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns for Churn Prediction: {missing}"
        )

    churn_probability = float(
        churn_pipeline.predict_proba(
            prediction_df
        )[0][1]
    )

    churn_prediction = int(
        churn_pipeline.predict(
            prediction_df
        )[0]
    )

    return {
        "Churn_Probability": round(
            churn_probability,
            4,
        ),
        "Churn_Prediction": churn_prediction,
    }


# ==========================================================
# CLV Prediction
# ==========================================================

# Change to True if your CLV model was trained using np.log1p(y)
CLV_LOG_TRANSFORM = True


def predict_clv(
    prediction_df: pd.DataFrame,
) -> float:
    """
    Predict Customer Lifetime Value.
    """

    required_columns = [
        "Recency",
        "Frequency",
        "Monetary",
        "Average_Order_Value",
        "Customer_Persona",
    ]

    missing = [
        col for col in required_columns
        if col not in prediction_df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns for CLV Prediction: {missing}"
        )

    clv = float(
        clv_pipeline.predict(
            prediction_df
        )[0]
    )

    if CLV_LOG_TRANSFORM:
        import numpy as np
        clv = np.expm1(clv)

    return round(clv, 2)





# ==========================================================
# Revenue-at-Risk Calculation
# ==========================================================

def calculate_revenue_at_risk(
    churn_probability: float,
    predicted_clv: float,
) -> float:
    """
    Calculate Revenue at Risk.

    Revenue at Risk = Churn Probability × Predicted CLV
    """

    revenue_at_risk = (
        churn_probability * predicted_clv
    )

    return round(
        revenue_at_risk,
        2,
    )


# ==========================================================
# Risk Category
# ==========================================================

def assign_risk_category(
    churn_probability: float,
) -> str:
    """
    Assign Risk Category.
    """

    if churn_probability >= HIGH_RISK_THRESHOLD:
        return "High Risk"

    elif churn_probability >= MEDIUM_RISK_THRESHOLD:
        return "Medium Risk"

    return "Low Risk"


# ==========================================================
# Customer Action
# ==========================================================

def assign_customer_action(
    risk_category: str,
) -> str:
    """
    Business recommendation based on risk.
    """

    actions = {

        "High Risk":
            "Immediate retention campaign and personal follow-up.",

        "Medium Risk":
            "Offer personalized discounts and engagement campaign.",

        "Low Risk":
            "Maintain loyalty program and explore upsell opportunities.",

    }

    return actions.get(
        risk_category,
        "Monitor customer behaviour."
    )


# ==========================================================
# Complete Prediction Pipeline
# ==========================================================

def predict_customer(
    transaction_df: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Complete end-to-end prediction pipeline.

    Parameters
    ----------
    transaction_df : pd.DataFrame

    Returns
    -------
    Dictionary containing prediction results.
    """

    logger.info(
        "Starting prediction pipeline..."
    )

    # ------------------------------------------------------
    # Data Cleaning
    # ------------------------------------------------------

    cleaned_df = clean_transaction_data(
        transaction_df
    )

    if cleaned_df.empty:

        raise ValueError(
            "No valid transactions found after data cleaning."
        )

    # ------------------------------------------------------
    # Feature Engineering
    # ------------------------------------------------------

    rfm_df = calculate_rfm(
        cleaned_df
    )

    if rfm_df.empty:

        raise ValueError(
            "No valid customer records found after feature engineering."
        )

    if len(rfm_df) > 1:

        raise ValueError(
            "Please upload transactions for one customer only."
        )

    # ------------------------------------------------------
    # Persona Prediction
    # ------------------------------------------------------

    persona = predict_persona(
        rfm_df
    )

    rfm_df["Customer_Persona"] = persona

    # ------------------------------------------------------
    # Prediction Features
    # ------------------------------------------------------

    prediction_features = rfm_df[
        [
            "Recency",
            "Frequency",
            "Monetary",
            "Average_Order_Value",
            "Customer_Persona",
        ]
    ]

    # ------------------------------------------------------
    # Churn Prediction
    # ------------------------------------------------------

    churn_results = predict_churn(
        prediction_features
    )

    # ------------------------------------------------------
    # CLV Prediction
    # ------------------------------------------------------

    predicted_clv = predict_clv(
        prediction_features
    )

    # ------------------------------------------------------
    # Revenue-at-Risk
    # ------------------------------------------------------

    revenue_at_risk = calculate_revenue_at_risk(

        churn_results["Churn_Probability"],

        predicted_clv,

    )

    # ------------------------------------------------------
    # Risk Category
    # ------------------------------------------------------

    risk_category = assign_risk_category(

        churn_results["Churn_Probability"]

    )

    # ------------------------------------------------------
    # Business Action
    # ------------------------------------------------------

    customer_action = assign_customer_action(

        risk_category

    )

    # ------------------------------------------------------
    # Final Result
    # ------------------------------------------------------

    result = {

        "CustomerID":
            int(
                rfm_df.iloc[0]["CustomerID"]
            ),

        "Recency":
            int(
                rfm_df.iloc[0]["Recency"]
            ),

        "Frequency":
            int(
                rfm_df.iloc[0]["Frequency"]
            ),

        "Monetary":
            round(
                float(
                    rfm_df.iloc[0]["Monetary"]
                ),
                2,
            ),

        "Average_Order_Value":
            round(
                float(
                    rfm_df.iloc[0]["Average_Order_Value"]
                ),
                2,
            ),

        "Customer_Persona":
            persona,

        "Churn_Probability":
            churn_results[
                "Churn_Probability"
            ],

        "Churn_Prediction":
            churn_results[
                "Churn_Prediction"
            ],

        "Predicted_CLV":
            predicted_clv,

        "Revenue_at_Risk":
            revenue_at_risk,

        "Risk_Category":
            risk_category,

        "Customer_Action":
            customer_action,

    }

    logger.info(
        "Prediction completed successfully."
    )

    logger.info(result)

    return result






# ==========================================================
# Load Transaction File
# ==========================================================

def load_transaction_file(file_path) -> pd.DataFrame:
    """
    Load transaction data from CSV or Excel.
    """

    file_path = Path(file_path)

    suffix = file_path.suffix.lower()

    if suffix == ".csv":

        return pd.read_csv(file_path)

    elif suffix in [".xlsx", ".xls"]:

        return pd.read_excel(file_path)

    raise ValueError(
        "Only CSV and Excel files are supported."
    )


# ==========================================================
# Batch Prediction
# ==========================================================

def predict_customers(
    transaction_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Predict multiple customers from one transaction dataset.
    """

    logger.info("Starting batch prediction...")

    cleaned_df = clean_transaction_data(
        transaction_df
    )

    if cleaned_df.empty:

        raise ValueError(
            "No valid transactions found after cleaning."
        )

    customer_ids = cleaned_df["CustomerID"].unique()

    results = []

    for customer_id in customer_ids:

        customer_transactions = cleaned_df[
            cleaned_df["CustomerID"] == customer_id
        ]

        try:

            prediction = predict_customer(
                customer_transactions
            )

            results.append(prediction)

        except Exception as e:

            logger.warning(
                f"Skipping Customer {customer_id}: {e}"
            )

    logger.info(
        "Completed prediction for %d customers.",
        len(results),
    )

    return pd.DataFrame(results)


# ==========================================================
# Export Predictions
# ==========================================================

def export_predictions(
    prediction_df: pd.DataFrame,
    output_path,
):
    """
    Export prediction results to CSV.
    """

    output_path = Path(output_path)

    prediction_df.to_csv(
        output_path,
        index=False,
    )

    logger.info(
        "Prediction file saved to %s",
        output_path,
    )


# ==========================================================
# Local Testing
# ==========================================================

if __name__ == "__main__":

    TEST_DATA = (
        ROOT_DIR
        / "data"
        / "raw"
        / "Online Retail.xlsx"
    )

    if TEST_DATA.exists():

        logger.info(
            "Running Predictor Module..."
        )

        df = load_transaction_file(
            TEST_DATA
        )

        predictions = predict_customers(
            df
        )

        logger.info(
            "Total Customers Predicted : %d",
            len(predictions),
        )

        logger.info(
            "\n%s",
            predictions.head(),
        )

        OUTPUT_FILE = (
            ROOT_DIR
            / "data"
            / "processed"
            / "real_time_predictions.csv"
        )

        export_predictions(
            predictions,
            OUTPUT_FILE,
        )

        logger.info(
            "Prediction completed successfully."
        )

    else:

        logger.warning(
            "Test dataset not found:\n%s",
            TEST_DATA,
        )