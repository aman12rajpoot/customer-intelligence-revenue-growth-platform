from fastapi import UploadFile, File

from utils.predictor import (
    load_transaction_file,
    predict_customers,
)





from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from utils.groq_utils import generate_business_recommendation


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data()
    yield


app = FastAPI(
    title="Customer Intelligence & Revenue Growth API",
    description="""REST API for the Customer Intelligence Platform.

Features:
- Customer Analytics
- Churn Prediction Results
- CLV Prediction Results
- Revenue-at-Risk Analysis
- AI Business Recommendations
""",
    version="1.0.0",
    contact={"name": "Aman Rajpoot"},
    lifespan=lifespan,
)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "processed"
DATA_PATH = DATA_DIR / "revenue_at_risk_analysis.csv"


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Revenue-at-risk data not found")

    df = pd.read_csv(DATA_PATH)
    df = df.copy()
    df["CustomerID"] = df["CustomerID"].astype(int)
    df["Churn_Probability"] = pd.to_numeric(df["Churn_Probability"], errors="coerce").fillna(0)
    df["Predicted_CLV"] = pd.to_numeric(df["Predicted_CLV"], errors="coerce").fillna(0)
    df["Revenue_at_Risk"] = pd.to_numeric(df["Revenue_at_Risk"], errors="coerce").fillna(0)
    df["Risk_Category"] = df["Risk_Category"].fillna("Unknown")
    df["Customer_Action"] = df["Customer_Action"].fillna("Monitor")
    if "Segment" not in df.columns:
        df["Segment"] = "Unknown"
    if "Customer_Persona" not in df.columns:
        df["Customer_Persona"] = "Unknown"
    return df


class CustomerSummary(BaseModel):
    CustomerID: int
    Segment: str
    Customer_Persona: str
    Churn_Probability: float
    Predicted_CLV: float
    Revenue_at_Risk: float
    Risk_Category: str
    Customer_Action: str


@app.get("/", tags=["General"])
def root() -> Dict[str, str]:
    return {"message": "Customer Intelligence API is running"}


@app.get("/health", tags=["General"])
def health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "api": "Customer Intelligence API",
        "version": "1.0.0",
    }


@app.get(
    "/dashboard",
    tags=["Dashboard"],
    summary="Dashboard KPIs",
    description="Returns executive KPIs for the customer intelligence dashboard.",
)
def dashboard() -> Dict[str, Any]:
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "total_customers": len(df),
        "high_risk": int(df["Risk_Category"].str.contains("High|Critical", case=False, na=False).sum()),
        "critical": int(df["Risk_Category"].str.contains("Critical", case=False, na=False).sum()),
        "average_clv": round(float(df["Predicted_CLV"].mean()), 2),
        "total_revenue_at_risk": round(float(df["Revenue_at_Risk"].sum()), 2),
        "average_churn": round(float(df["Churn_Probability"].mean()), 3),
    }


@app.get("/customers", tags=["Customers"], response_model=List[CustomerSummary])
def get_customers(
    limit: int = Query(100, ge=1, le=500, description="Maximum customers to return")
) -> List[Dict[str, Any]]:
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    limited_df = df.head(limit)
    return limited_df[
        [
            "CustomerID",
            "Segment",
            "Customer_Persona",
            "Churn_Probability",
            "Predicted_CLV",
            "Revenue_at_Risk",
            "Risk_Category",
            "Customer_Action",
        ]
    ].to_dict(orient="records")


@app.get("/customers/{customer_id}", tags=["Customers"])
def get_customer(customer_id: int) -> Dict[str, Any]:
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    match = df[df["CustomerID"] == customer_id]
    if match.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    return match.iloc[0].to_dict()


@app.get("/top-risk", tags=["Analytics"])
def top_risk() -> List[Dict[str, Any]]:
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return df.sort_values("Revenue_at_Risk", ascending=False).head(10).to_dict(orient="records")


@app.post("/recommendation/{customer_id}", tags=["AI"])
def recommendation(customer_id: int) -> Dict[str, Any]:
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    row = df[df["CustomerID"] == customer_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    recommendation = generate_business_recommendation(row.iloc[0].to_dict())
    return {
        "customer_id": customer_id,
        "risk_category": row.iloc[0]["Risk_Category"],
        "customer_action": row.iloc[0]["Customer_Action"],
        "recommendation": recommendation,
    }


@app.get("/executive-summary", tags=["AI"])
def get_summary() -> Dict[str, str]:
    path = DATA_DIR / "executive_summary.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Executive summary not found")
    return {"summary": path.read_text(encoding="utf-8")}







@app.post(
    "/predict",
    tags=["Prediction"],
    summary="Real-Time Customer Prediction",
)
async def predict(file: UploadFile = File(...)):
    """
    Upload a CSV or Excel transaction file
    and generate real-time predictions.
    """

    try:

        suffix = Path(file.filename).suffix.lower()

        if suffix not in [".csv", ".xlsx", ".xls"]:

            raise HTTPException(
                status_code=400,
                detail="Only CSV and Excel files are supported.",
            )

        temp_path = DATA_DIR / file.filename

        with open(temp_path, "wb") as f:

            f.write(await file.read())

        transaction_df = load_transaction_file(
            temp_path
        )

        prediction_df = predict_customers(
            transaction_df
        )

        temp_path.unlink(missing_ok=True)

        return prediction_df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )