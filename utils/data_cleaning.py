"""
Data Cleaning Module

This module performs the same cleaning operations
used during Exploratory Data Analysis (EDA).

Author : Aman Rajpoot
"""

import pandas as pd


def clean_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw transaction data.

    Parameters
    ----------
    df : pd.DataFrame
        Raw transaction dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned transaction dataset.
    """

    df = df.copy()

    # -------------------------
    # Remove duplicate records
    # -------------------------
    df.drop_duplicates(inplace=True)

    # -------------------------
    # Remove missing CustomerID
    # -------------------------
    df.dropna(subset=["CustomerID"], inplace=True)

    # -------------------------
    # Correct data types
    # -------------------------

    # -------------------------
    # Correct data types
    # -------------------------
    df["CustomerID"] = df["CustomerID"].astype(int)

    # Convert InvoiceDate safely
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce",
    )

    # Remove rows where InvoiceDate could not be converted
    df.dropna(subset=["InvoiceDate"], inplace=True)

    # -------------------------
    # Remove invalid quantity
    # -------------------------
    df = df[df["Quantity"] > 0]

    # -------------------------
    # Remove invalid price
    # -------------------------
    df = df[df["UnitPrice"] > 0]

    # -------------------------
    # Revenue Feature
    # -------------------------
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    return df
