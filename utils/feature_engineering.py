"""
Feature Engineering Module

Calculates RFM features from cleaned
transaction data.

Author : Aman Rajpoot
"""

from typing import Optional

import pandas as pd


def calculate_rfm(
    df: pd.DataFrame,
    reference_date: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    """
    Calculate RFM metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Clean transaction dataframe.

    reference_date : pd.Timestamp, optional
        Date used for Recency calculation.
        If None, latest InvoiceDate is used.

    Returns
    -------
    pd.DataFrame
        Customer-level RFM dataframe.
    """

    df = df.copy()

    # --------------------------
    # Reference Date
    # --------------------------

    if reference_date is None:
        reference_date = df["InvoiceDate"].max()

    # --------------------------
    # Recency
    # --------------------------

    recency = (
        reference_date -
        df.groupby("CustomerID")["InvoiceDate"].max()
    ).dt.days

    # --------------------------
    # Frequency
    # --------------------------

    frequency = (
        df.groupby("CustomerID")["InvoiceNo"]
        .nunique()
    )

    # --------------------------
    # Monetary
    # --------------------------

    monetary = (
        df.groupby("CustomerID")["Revenue"]
        .sum()
    )

    # --------------------------
    # RFM Table
    # --------------------------

    rfm = pd.DataFrame(
        {
            "Recency": recency,
            "Frequency": frequency,
            "Monetary": monetary,
        }
    )

    # --------------------------
    # Average Order Value
    # --------------------------

    rfm["Average_Order_Value"] = (
        rfm["Monetary"] /
        rfm["Frequency"].replace(0, 1)
    ).round(2)


    rfm.reset_index(inplace=True)


    rfm.sort_values(
    by="CustomerID",
    inplace=True)


    rfm.reset_index(
        drop=True,
        inplace=True
    )

    return rfm