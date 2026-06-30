import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


def get_dashboard():
    response = requests.get(f"{API_URL}/dashboard")
    response.raise_for_status()
    return response.json()


def get_customers():
    response = requests.get(f"{API_URL}/customers")
    response.raise_for_status()
    return response.json()


def get_customer(customer_id):
    response = requests.get(f"{API_URL}/customers/{customer_id}")
    response.raise_for_status()
    return response.json()


def predict_customer(transactions):

    response = requests.post(
        f"{API_URL}/predict-json",
        json=transactions,
    )

    response.raise_for_status()

    return response.json()[0]


def get_recommendation(customer_id):

    response = requests.post(
        f"{API_URL}/recommendation/{customer_id}",
    )

    response.raise_for_status()

    return response.json()["recommendation"]


def get_prediction_recommendation(prediction):

    response = requests.post(
        f"{API_URL}/recommendation-json",
        json=prediction,
    )

    response.raise_for_status()

    return response.json()["recommendation"]


def get_executive_summary():
    response = requests.get(f"{API_URL}/executive-summary")
    response.raise_for_status()
    return response.json()
