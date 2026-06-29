````markdown
# 🚀 Customer Intelligence & Revenue Growth Platform

The **Customer Intelligence & Revenue Growth Platform** is an end-to-end AI-powered analytics solution that combines customer analytics, machine learning, predictive modeling, and Large Language Models (LLMs) to help organizations identify high-value customers, predict churn, estimate Customer Lifetime Value (CLV), quantify revenue at risk, and generate AI-powered retention strategies.

---

# Overview

This project demonstrates a complete analytics workflow from raw transaction data to actionable business recommendations. It integrates data cleaning, exploratory data analysis, SQL analytics, machine learning, FastAPI, Streamlit, and Generative AI into a single intelligent customer analytics platform.

---

# Business Problem

Businesses often lose valuable customers because they cannot identify customers who are both likely to churn and financially important.

This platform answers questions such as:

- Which customers are most likely to churn?
- Which customers have the highest future value?
- How much revenue is currently at risk?
- Which customers should be prioritized for retention?
- What business actions should be taken to maximize customer retention?

---

# ⭐ Key Highlights

- End-to-End Customer Intelligence Platform
- Real-Time Customer Prediction Pipeline
- RFM-based Customer Segmentation
- Customer Churn Prediction
- Customer Lifetime Value (CLV) Prediction
- Revenue-at-Risk Analysis
- AI-powered Business Recommendations using Groq Llama 3.3
- Interactive Streamlit Dashboard
- FastAPI REST API with Swagger Documentation
- Modular and Production-Ready Project Structure

---

# Project Architecture

```text
                    Historical Analytics

              Raw Customer Transaction Data
                          │
                          ▼
                   Data Cleaning
                          │
                          ▼
             Exploratory Data Analysis
                          │
                          ▼
                SQL Business Analytics
                          │
                          ▼
                 Machine Learning Models
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
 Customer Personas   Churn Prediction   CLV Prediction
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                Revenue-at-Risk Analysis
                          │
                          ▼
               Executive Dashboard
                          │
                          ▼
             AI Business Recommendations


────────────────────────────────────────────────────────────


                 Real-Time Prediction Pipeline

            Manual Customer Transactions
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
               Revenue-at-Risk Analysis
                          │
                          ▼
              AI Business Recommendation
```

---

# Features

## Customer Analytics

- Customer Segmentation
- Customer Personas
- RFM Analysis
- Customer Lifetime Value Prediction
- Customer Churn Prediction
- Revenue-at-Risk Analysis

## Machine Learning

- Classification Models
- Regression Models
- Feature Engineering
- Cross Validation
- Hyperparameter Tuning
- Model Evaluation

## Business Intelligence

- Executive Dashboard
- Revenue-at-Risk Dashboard
- Customer Explorer
- Executive Summary
- Business KPIs

## Generative AI

- AI-powered Customer Recommendations
- Executive Business Summaries
- Customer Retention Strategies
- Revenue Growth Suggestions

## Deployment

- Interactive Streamlit Dashboard
- FastAPI REST API
- Swagger Documentation
- Real-Time Prediction Engine

---

# Technology Stack

### Programming Language

- Python

### Data Analysis

- Pandas
- NumPy

### Data Visualization

- Plotly
- Matplotlib

### Machine Learning

- Scikit-learn
- XGBoost

### AI

- Groq API
- Llama 3.3 70B Versatile

### Backend

- FastAPI
- Uvicorn

### Frontend

- Streamlit

### Database & Analytics

- SQL

---

# Project Structure

```text
Customer-Intelligence-Revenue-Growth/
│
├── assets/
│   └── hero.png
│
├── data/
│   ├── raw/
│   │   └── Online Retail.xlsx
│   │
│   └── processed/
│       ├── cleaned_data.csv
│       ├── customer_ai_recommendations.csv
│       ├── customer_churn_predictions.csv
│       ├── customer_clv_predictions.csv
│       ├── customer_personas.csv
│       ├── future_transactions.csv
│       ├── real_time_predictions.csv
│       ├── recommendation_prompt.json
│       ├── revenue_at_risk_analysis.csv
│       └── rfm_table.csv
│
├── models/
│   ├── churn_prediction_pipeline.pkl
│   ├── clv_prediction_pipeline.pkl
│   ├── customer_persona_model.pkl
│   └── persona_scaler.pkl
│
├── notebooks/
│   ├── EDA.ipynb
│   ├── sql_analytics.ipynb
│   ├── RFM_segmentation.ipynb
│   ├── 04_KMeans_Customer_Segmentation.ipynb
│   ├── Churn_Prediction.ipynb
│   ├── Customer_Lifetime_Value_Prediction.ipynb
│   ├── Revenue_at_Risk_Analysis.ipynb
│   └── AI_layer.ipynb
│
├── reports/
│   └── executive_summary.md
│
├── utils/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── groq_utils.py
│   └── predictor.py
│
├── app.py
├── api.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Dashboard

The Streamlit dashboard provides:

- Executive Dashboard
- Customer Explorer
- Revenue-at-Risk Analytics
- AI Recommendation Generator
- Executive Summary
- Real-Time Customer Prediction
- Interactive Visualizations

---

# FastAPI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API Status |
| GET | `/health` | Health Check |
| GET | `/dashboard` | Executive Dashboard KPIs |
| GET | `/customers` | Retrieve Customer List |
| GET | `/customers/{customer_id}` | Retrieve Customer Details |
| GET | `/top-risk` | Top Revenue-at-Risk Customers |
| POST | `/recommendation/{customer_id}` | Generate AI Business Recommendation |
| POST | `/predict` | Real-Time Customer Prediction |
| GET | `/executive-summary` | Executive Business Summary |

---

# Machine Learning Pipeline

## Customer Churn Prediction

- Data Preprocessing
- Feature Engineering
- Model Training
- Cross Validation
- Churn Probability Prediction

## Customer Lifetime Value Prediction

- Feature Engineering
- Regression Modeling
- Future Revenue Estimation

## Revenue-at-Risk

```text
Revenue-at-Risk = Predicted CLV × Churn Probability
```

This metric helps prioritize customers based on both financial value and churn risk.

---

# AI Business Advisor

The platform integrates a Large Language Model (LLM) using the Groq API to generate:

- Personalized Customer Retention Strategies
- Revenue Optimization Recommendations
- Executive Business Summaries
- AI-powered Business Insights

The AI layer transforms predictive analytics into clear, actionable business decisions.

---

# Installation

### 1. Clone the repository

```bash
git clone https://github.com/aman12rajpoot/Customer-Intelligence-Revenue-Growth.git
```

### 2. Navigate to the project

```bash
cd Customer-Intelligence-Revenue-Growth
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

# Running the Project

## Start FastAPI

```bash
uvicorn api:app --reload
```

API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Start Streamlit

```bash
streamlit run app.py
```

---

# Results

The platform enables organizations to:

- Identify high-risk customers
- Estimate Customer Lifetime Value
- Quantify Revenue-at-Risk
- Prioritize customer retention
- Generate AI-assisted business recommendations
- Support executive decision-making using interactive dashboards

---

# Future Improvements

- Real-Time Database Integration
- Authentication & Role-Based Access Control
- Cloud Deployment
- Automated Model Retraining
- Customer Communication Automation
- Multi-language AI Recommendations

