
## 📌 Overview

The **Customer Intelligence & Revenue Growth Platform** is a full-stack AI-powered customer analytics application that helps businesses understand customer behavior, predict churn, estimate Customer Lifetime Value (CLV), quantify revenue at risk, and generate AI-powered retention strategies.

The project combines **Machine Learning**, **Customer Analytics**, **FastAPI**, **Streamlit**, and **Large Language Models (Groq Llama 3.3)** into one end-to-end business intelligence platform.

The application supports both:

- Historical Customer Analytics
- Real-Time Prediction for New Customers

---

# 🎯 Business Problem

Customer retention is one of the biggest challenges faced by businesses.

Most organizations know:

- who purchased,
- how much they spent,
- when they purchased,

but they do not know:

- Which customers are likely to churn?
- Which customers generate the highest value?
- How much future revenue is currently at risk?
- Which customers should be targeted first?
- What actions should be taken to retain them?

This platform answers all of these questions using data-driven machine learning and AI.

---

# ⭐ Key Features

## Customer Analytics

- RFM Segmentation
- Customer Persona Prediction
- Customer Churn Prediction
- Customer Lifetime Value Prediction
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

- AI Business Recommendations
- Executive Business Summary
- Customer Retention Strategies
- Revenue Growth Suggestions
- Groq Llama 3.3 Integration

---

## Real-Time Prediction

Supports prediction for completely **new customers**.

Users can:

- Enter customer transactions manually
- Paste transactions directly from Excel
- Generate predictions
- Generate AI recommendations instantly

---

# 🏗 System Architecture

```
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

                 Groq Llama 3.3 LLM

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
- Llama 3.3 70B Versatile

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

The Streamlit dashboard consists of:

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
| POST | `/recommendation/{customer_id}` | Existing Customer AI Recommendation |
| POST | `/predict-json` | Real-Time Prediction |
| POST | `/recommendation-json` | AI Recommendation for New Customer |
| GET | `/executive-summary` | Executive Summary |

---



# 🤖 Machine Learning Pipeline

The platform integrates multiple machine learning models to generate business insights.

## 1. Customer Persona Prediction

- Customer feature engineering
- RFM-based behavioral features
- Persona classification
- Customer segmentation

---

## 2. Customer Churn Prediction

The churn prediction pipeline includes:

- Data preprocessing
- Feature engineering
- Classification model
- Hyperparameter tuning
- Cross validation
- Churn probability prediction

Output:

- Churn Probability
- Churn Label

---

## 3. Customer Lifetime Value (CLV)

The CLV prediction model estimates the future value of every customer.

Pipeline:

- Feature Engineering
- Regression Model
- Future Revenue Prediction

Output:

- Predicted Customer Lifetime Value

---

## 4. Revenue-at-Risk Analysis

The project combines CLV with churn probability to estimate financial risk.

```text
Revenue-at-Risk = Predicted CLV × Churn Probability
```

This allows businesses to prioritize customers based on both:

- Customer value
- Churn likelihood

---

# 🤖 AI Business Recommendation Engine

The project integrates **Groq Llama 3.3 70B Versatile** to transform predictive analytics into actionable business recommendations.

The AI layer generates:

- Personalized Retention Strategies
- Revenue Growth Suggestions
- Customer Engagement Plans
- Executive Business Insights
- Strategic Recommendations

The recommendation engine works for both:

- Existing historical customers
- Newly predicted customers (Real-Time Prediction)

---

# 📸 Dashboard Preview

> Add screenshots after deployment.

Suggested screenshots:

```
Home Page

Executive Dashboard

Customer Explorer

AI Recommendation

Real-Time Prediction

Executive Summary

Swagger API Documentation
```

Example:

```markdown
## Home

![Home](screenshots/home.png)

## Executive Dashboard

![Dashboard](screenshots/dashboard.png)

## Customer Explorer

![Customer Explorer](screenshots/customer_explorer.png)

## Real-Time Prediction

![Prediction](screenshots/prediction.png)

## AI Recommendation

![Recommendation](screenshots/recommendation.png)
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/aman12rajpoot/Customer-Intelligence-Revenue-Growth.git
```

Navigate to project

```bash
cd Customer-Intelligence-Revenue-Growth
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

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
GROQ_MODEL=llama-3.3-70b-versatile
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

Deploy FastAPI using:

- Render


Example:

```
https://customer-intelligence-api.onrender.com
```

---

## Frontend

Deploy Streamlit using:

- Streamlit Community Cloud

Update the backend URL in:

```text
utils/api_client.py
```

Replace

```python
API_URL = "http://127.0.0.1:8000"
```

with

```python
API_URL = "https://your-fastapi-url.onrender.com"
```

---

# 📈 Results

The platform enables organizations to:

- Identify high-risk customers
- Predict customer churn
- Estimate Customer Lifetime Value
- Quantify Revenue-at-Risk
- Prioritize retention campaigns
- Generate AI-assisted business recommendations
- Support executive decision making
- Perform real-time customer prediction

---

# 🎯 Skills Demonstrated

This project demonstrates practical experience in:

### Data Analytics

- Data Cleaning
- Exploratory Data Analysis
- SQL Analytics
- RFM Analysis

---

### Machine Learning

- Feature Engineering
- Classification
- Regression
- Customer Segmentation
- Model Evaluation
- Hyperparameter Tuning
- Cross Validation

---

### Backend Development

- FastAPI
- REST APIs
- Swagger Documentation
- Pydantic Models
- API Integration

---

### Frontend Development

- Streamlit
- Interactive Dashboards
- Data Visualization
- User Experience Design

---

### Artificial Intelligence

- Prompt Engineering
- LLM Integration
- Groq API
- Business Recommendation Generation

---

### Software Engineering

- Modular Project Structure
- Frontend–Backend Separation
- Version Control (Git/GitHub)
- Deployment Ready Architecture

---

# 🔮 Future Improvements

- User Authentication
- Role-Based Access Control
- PostgreSQL/MySQL Integration
- Docker Containerization
- CI/CD Pipeline
- Cloud Storage
- Automated Model Retraining
- Scheduled Batch Predictions
- Email Notification System
- Customer Communication Automation
- Multi-language AI Recommendations



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
- Llama 3.3 70B Versatile

Special thanks to the open-source community for providing the tools and libraries that made this project possible.



> **Customer Intelligence & Revenue Growth Platform** demonstrates an end-to-end customer analytics workflow—from raw transaction data and feature engineering to machine learning predictions, AI-powered business recommendations, and an interactive web application—using a modern **Streamlit + FastAPI** architecture.