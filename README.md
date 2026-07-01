# 🚀 Customer Intelligence & Revenue Growth Platform

### 🔗 Live Demo

- 🌐 Frontend: https://customer-intelligence-revenue-growth-platform-ea5pjfaayrverxr5.streamlit.app
- ⚡ FastAPI Docs: https://customer-intelligence-system-api.onrender.com/docs
- 📂 GitHub Repository: https://github.com/aman12rajpoot/customer-intelligence-revenue-growth-platform

---

## 📌 Overview

The **Customer Intelligence & Revenue Growth Platform** is a full-stack AI-powered customer analytics application that helps businesses understand customer behavior, predict customer churn, estimate Customer Lifetime Value (CLV), quantify revenue at risk, and generate AI-powered business recommendations.

The project combines **Machine Learning**, **Customer Analytics**, **FastAPI**, **Streamlit**, and **GPT-OSS (via Groq API)** into a unified end-to-end customer intelligence platform.

The application supports both:

- Historical Customer Analytics
- Real-Time Prediction for New Customers

---

# 🎯 Business Problem

Customer retention is one of the biggest challenges faced by modern businesses.

Most organizations know:

- Who purchased
- How much they spent
- When they purchased

However, they often lack answers to critical business questions such as:

- Which customers are most likely to churn?
- Which customers generate the highest lifetime value?
- How much future revenue is currently at risk?
- Which customers should be prioritized for retention?
- What actions should be taken to maximize customer retention?

This platform addresses these challenges by combining machine learning and generative AI to transform customer transaction data into actionable business insights.

---

# ⭐ Key Features

## Customer Analytics

- RFM Segmentation
- Customer Persona Prediction
- Customer Churn Prediction
- Customer Lifetime Value (CLV) Prediction
- Revenue-at-Risk Analysis

---

## Machine Learning

- Feature Engineering
- Classification Models
- Regression Models
- Cross Validation
- Hyperparameter Tuning
- Model Evaluation

---

## Business Intelligence

- Executive Dashboard
- Customer Explorer
- Revenue-at-Risk Dashboard
- Executive Summary
- Business KPIs

---

## Artificial Intelligence

- AI-Powered Business Recommendations
- Executive Business Summary
- Customer Retention Strategies
- Revenue Growth Suggestions
- **GPT-OSS Integration via Groq API**

---

## ⚡ Real-Time Prediction

Supports prediction for completely **new customers**.

Users can:

- Enter customer transactions manually
- Paste customer transactions directly from Excel
- Generate real-time customer predictions
- Generate AI-powered business recommendations instantly

---

# 🏗 System Architecture

```text
                        FRONTEND

                    Streamlit Dashboard

        ┌────────────────────────────────────┐
        │            Home                    │
        │ Executive Dashboard               │
        │ Customer Explorer                 │
        │ AI Recommendation                 │
        │ Real-Time Prediction              │
        │ Executive Summary                 │
        │ About                             │
        └────────────────────────────────────┘
                        │
                        │ REST API
                        ▼

                    FastAPI Backend

        ┌────────────────────────────────────┐
        │ /dashboard                         │
        │ /customers                         │
        │ /customers/{id}                    │
        │ /top-risk                          │
        │ /predict-json                      │
        │ /recommendation/{id}               │
        │ /recommendation-json               │
        │ /executive-summary                 │
        └────────────────────────────────────┘
                        │
                        ▼

               Machine Learning Models

        Persona Prediction

        Churn Prediction

        CLV Prediction

        Revenue-at-Risk Analysis
                        │
                        ▼

              GPT-OSS (Groq API)

                        │
                        ▼

         AI Business Recommendation
```

---

# 📊 Historical Analytics Pipeline

```
Raw Transaction Data

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

Feature Engineering

        │

        ▼

Customer Segmentation

        │

        ▼

Persona Prediction

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

Executive Dashboard

        │

        ▼

AI Business Recommendation
```

---

# ⚡ Real-Time Prediction Pipeline

```
Manual Customer Transactions

                OR

Paste Transactions from Excel

                │

                ▼

Transaction Validation

                │

                ▼

Feature Engineering

                │

                ▼

Persona Prediction

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

Prediction Summary

                │

                ▼

AI Business Recommendation
```

---

# 💻 Technology Stack

## Programming

- Python

---

## Data Analysis

- Pandas
- NumPy

---

## Data Visualization

- Plotly
- Matplotlib

---

## Machine Learning

- Scikit-learn
- XGBoost

---

## Backend

- FastAPI
- Uvicorn

---

## Frontend

- Streamlit

---

## AI

- Groq API
-GPT-OSS 120B

---

## Database & Analytics

- SQL

---

# 📁 Project Structure

```text
Customer-Intelligence-Revenue-Growth/

├── assets/
│   └── hero.png
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── notebooks/
│
├── reports/
│   └── executive_summary.md
│
├── utils/
│   ├── api_client.py
│   ├── predictor.py
│   ├── feature_engineering.py
│   ├── groq_utils.py
│   └── data_cleaning.py
│
├── app.py                 # Streamlit Frontend
├── api.py                 # FastAPI Backend
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🖥 Dashboard Pages

The Streamlit dashboard includes:

- 🏠 Home
- 📊 Executive Dashboard
- 👤 Customer Explorer
- 🤖 AI Recommendation
- ⚡ Real-Time Prediction
- 📄 Executive Summary
- ℹ️ About

---

# 🌐 FastAPI Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API Status |
| GET | `/health` | Health Check |
| GET | `/dashboard` | Executive KPIs |
| GET | `/customers` | Customer List |
| GET | `/customers/{customer_id}` | Customer Details |
| GET | `/top-risk` | Top Revenue-at-Risk Customers |
| POST | `/recommendation/{customer_id}` | AI Recommendation for Existing Customer |
| POST | `/predict-json` | Real-Time Customer Prediction |
| POST | `/recommendation-json` | AI Recommendation for New Customer |
| GET | `/executive-summary` | Executive Summary |

---

# 🤖 Machine Learning Pipeline

The platform integrates multiple machine learning models to generate business insights.

## 1. Customer Persona Prediction

- Customer Feature Engineering
- RFM-Based Behavioral Features
- Persona Classification
- Customer Segmentation

---

## 2. Customer Churn Prediction

The churn prediction pipeline includes:

- Data Preprocessing
- Feature Engineering
- Classification Model
- Hyperparameter Tuning
- Cross Validation
- Churn Probability Prediction

**Outputs**

- Churn Probability
- Churn Label

---

## 3. Customer Lifetime Value (CLV)

The CLV prediction model estimates the future value of every customer.

Pipeline:

- Feature Engineering
- Regression Model
- Future Revenue Prediction

**Output**

- Predicted Customer Lifetime Value

---

## 4. Revenue-at-Risk Analysis

The platform combines predicted CLV with churn probability to estimate financial risk.

```text
Revenue-at-Risk = Predicted CLV × Churn Probability
```

This enables businesses to prioritize customers based on:

- Customer Value
- Churn Risk

---

# 🤖 AI Business Recommendation Engine

The platform integrates **GPT-OSS 120B** through the **Groq API** to transform machine learning predictions into actionable business recommendations.

The AI engine generates:

- Personalized Customer Retention Strategies
- Executive Business Summaries
- Customer Engagement Recommendations
- Revenue Growth Suggestions
- Strategic Business Insights

The recommendation engine supports both:

- Existing Historical Customers
- New Customers through the Real-Time Prediction Pipeline

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/aman12rajpoot/customer-intelligence-revenue-growth-platform.git
```

Navigate to the project

```bash
cd customer-intelligence-revenue-growth-platform
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

---

# ▶ Running the Project

## Start FastAPI Backend

```bash
uvicorn api:app --reload
```

Backend API

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Start Streamlit Frontend

```bash
streamlit run app.py
```

Frontend

```
http://localhost:8501
```

---

# ☁ Deployment

## Backend

**Platform:** Render

https://customer-intelligence-system-api.onrender.com

---

## Frontend

**Platform:** Streamlit Community Cloud

https://customer-intelligence-revenue-growth-platform-ea5pjfaayrverxr5.streamlit.app

---

# 📈 Results

The platform enables organizations to:

- Identify High-Risk Customers
- Predict Customer Churn
- Estimate Customer Lifetime Value
- Quantify Revenue-at-Risk
- Prioritize Customer Retention Campaigns
- Generate AI-Powered Business Recommendations
- Support Executive Decision-Making
- Perform Real-Time Customer Prediction

---

# 🎯 Skills Demonstrated

## Data Analytics

- Data Cleaning
- Exploratory Data Analysis (EDA)
- SQL Analytics
- RFM Analysis

---

## Machine Learning

- Feature Engineering
- Customer Segmentation
- Classification
- Regression
- Model Evaluation
- Hyperparameter Tuning
- Cross Validation

---

## Backend Development

- FastAPI
- REST API Development
- Swagger Documentation
- Pydantic
- API Integration

---

## Frontend Development

- Streamlit
- Interactive Dashboards
- Data Visualization
- User Experience Design

---

## Artificial Intelligence

- Prompt Engineering
- GPT-OSS Integration
- Groq API
- AI-Powered Business Recommendation Generation

---

## Software Engineering

- Modular Project Structure
- Frontend–Backend Architecture
- Version Control (Git/GitHub)
- Cloud Deployment

---

# 🔮 Future Improvements

- User Authentication
- Role-Based Access Control
- PostgreSQL/MySQL Integration
- Docker Containerization
- CI/CD Pipeline
- Automated Model Retraining
- Scheduled Batch Predictions
- Customer Communication Automation
- Multi-language AI Recommendations

---

# 🙏 Acknowledgements

This project uses:

- Streamlit
- FastAPI
- Scikit-learn
- XGBoost
- Plotly
- Pandas
- NumPy
- Groq API
- GPT-OSS 120B

Special thanks to the open-source community for providing the tools and libraries that made this project possible.

---

> **Customer Intelligence & Revenue Growth Platform** demonstrates a complete end-to-end customer analytics workflow—from raw transaction data and feature engineering to machine learning predictions, AI-powered business recommendations, and real-time decision support—using a modern **Streamlit + FastAPI** architecture powered by **GPT-OSS** through the **Groq API**.