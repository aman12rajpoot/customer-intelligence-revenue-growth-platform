import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from utils.api_client import (get_customer, get_customers, get_dashboard,
                              get_executive_summary,
                              get_prediction_recommendation,
                              get_recommendation, predict_customer)

load_dotenv()

st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), transparent 22%), linear-gradient(180deg, #07111f 0%, #0f172a 40%, #111827 100%); }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    [data-testid="stSidebar"] { background: #06111f; }
    .css-10trblm { background: transparent; }
    .stSidebar { padding-top: 0.5rem; }
    .sidebar-brand { background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 1rem 1rem 0.8rem 1rem; margin-bottom: 1rem; }
    .sidebar-brand h2 { color: #ffffff; margin: 0 0 0.4rem 0; font-size: 1.25rem; }
    .sidebar-brand p { color: #94a3b8; margin: 0; font-size: 0.9rem; line-height: 1.4; }
    .sidebar-menu { margin-top: 1rem; }
    .sidebar-menu .streamlit-expanderHeader { color: #ffffff; }
    .sidebar-menu label { color: #cbd5e1; font-size: 0.95rem; }
    .sidebar-menu div[role="radiogroup"] label { margin-bottom: 0.75rem; }
    .stButton > button { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); color: white; border: none; border-radius: 14px; padding: 0.8rem 1rem; font-size: 0.95rem; }
    .stButton > button:hover { background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%); }
    .hero-box { background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(147, 197, 253, 0.16); border-radius: 28px; padding: 2rem; margin-bottom: 1.5rem; }
    .hero-title { color: #f8fafc; font-size: 3.2rem; line-height: 1.05; margin-bottom: 0.75rem; }
    .hero-subtitle { color: #cbd5e1; font-size: 1.05rem; max-width: 680px; margin-bottom: 1.75rem; }
    .hero-cta { display: inline-flex; align-items:center; justify-content:center; background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%); color: white; border-radius: 14px; padding: 0.95rem 1.3rem; font-weight: 600; text-decoration: none; box-shadow: 0 12px 30px rgba(59, 130, 246, 0.24); margin-top: 1rem; }
    .hero-cta:hover { opacity: 0.95; }
    .hero-buttons { display:flex; gap:0.75rem; flex-wrap:wrap; margin-top:1.5rem; }
    .hero-buttons .button-container { border-radius: 14px; background: rgba(255,255,255,0.05); padding: 1rem 1.1rem; min-width: 180px; }
    .hero-buttons .button-container h3 { margin:0 0 0.5rem 0; color:#f8fafc; font-size:1rem; }
    .hero-buttons .button-container p { color:#94a3b8; margin:0; line-height:1.4; font-size:0.93rem; }
    .feature-card { background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 1.3rem; min-height: 155px; }
    .feature-card h4 { margin-bottom: 0.75rem; color: #f8fafc; }
    .feature-card p { color: #cbd5e1; margin: 0; line-height: 1.5; }
    .feature-grid { display:grid; gap:1rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
    .panel { background: rgba(15, 23, 42, 0.95); border-radius: 24px; padding: 1.25rem 1.4rem; border: 1px solid rgba(255,255,255,0.08); }
    .small-muted { color: #94a3b8; font-size: 0.95rem; }
    .capability-card { background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 1rem 1.2rem; }
    .capability-card h4 { margin: 0 0 0.5rem 0; color:#f8fafc; }
    .capability-card p { margin: 0; color: #cbd5e1; line-height:1.4; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: #f8fafc; }
    </style>
    """,
    unsafe_allow_html=True,
)


ROOT = Path(__file__).resolve().parent

ASSETS_DIR = ROOT / "assets"

hero_path = ASSETS_DIR / "hero.png"

HERO_IMAGE = Image.open(hero_path)


PAGES = [
    "🏠 Home",
    "📊 Executive Dashboard",
    "👤 Customer Explorer",
    "🤖 AI Recommendation",
    "⚡ Real-Time Prediction",  # NEW
    "📄 Executive Summary",
    "ℹ️ About",
]

st.sidebar.markdown(
    """
    <div class='sidebar-brand'>
      <h2>Customer Intelligence</h2>
      <p>Revenue Growth Platform</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='sidebar-menu'>", unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", PAGES, index=0)
st.sidebar.markdown("</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div class='sidebar-section'><h4>Our Mission</h4><p>Empowering businesses with data-driven insights to retain customers and accelerate revenue growth.</p></div>",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)
def load_backend_data():
    customer_df = pd.DataFrame(get_customers())
    executive_summary = get_executive_summary()["summary"]
    return customer_df, executive_summary


try:
    customer_df, executive_summary = load_backend_data()

except Exception as e:
    st.error(f"Backend connection failed.\n\n{e}")
    st.stop()


def render_footer():
    st.markdown("---")
    st.caption(
        "Developed by Aman Rajpoot | Customer Intelligence & Revenue Growth Platform"
    )


def render_kpi_card(title: str, value: str, subtitle: str):
    st.markdown(
        f"""
        <div class="panel">
            <div class="small-muted">{title}</div>
            <div style="
                font-size:1.45rem;
                font-weight:700;
                color:#f8fafc;
                margin-top:0.2rem;
            ">
                {value}
            </div>
            <div class="small-muted" style="margin-top:0.2rem;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "recommendation" not in st.session_state:
    st.session_state["recommendation"] = None


if "transactions" not in st.session_state:
    st.session_state["transactions"] = []


if page == "🏠 Home":

    st.markdown(
        """
    <div style="text-align:center; margin-bottom:25px;">

    <h1 style="
    font-size:48px;
    color:white;
    margin-bottom:8px;
    font-weight:700;">

    Customer Intelligence & Revenue Growth Platform

    </h1>

    <p style="
    font-size:20px;
    color:#cbd5e1;
    margin-top:0;">

    Transform Customer Data into Actionable Insights using
    Machine Learning, Customer Analytics and AI.

    </p>

    </div>
    """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([0.9, 6, 0.09])

    with center:

        st.image(
            HERO_IMAGE,
            width=750,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            """
        <div class="feature-card">

        <h2>📉</h2>

        <h4>Predict</h4>

        Predict customer churn using
        Machine Learning models.

        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
        <div class="feature-card">

        <h2>👥</h2>

        <h4>Understand</h4>

        Perform RFM Segmentation
        and Customer Persona Analysis.

        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
        <div class="feature-card">

        <h2>💰</h2>

        <h4>Maximize</h4>

        Estimate Customer Lifetime Value
        to improve business growth.

        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            """
        <div class="feature-card">

        <h2>🤖</h2>

        <h4>Act</h4>

        Generate AI-powered
        business recommendations.

        </div>
        """,
            unsafe_allow_html=True,
        )

    # st.markdown(
    #         "<div class='panel' style='margin-top:1.5rem;'>"
    #         "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1rem;'>"
    #         "<div class='feature-card'><h6>Predict</h6><p>Churn with ML models and identify at-risk customers early.</p></div>"
    #         "<div class='feature-card'><h6>Understand</h6><p>Analyze customer segments, personas, and behavior with RFM analytics.</p></div>"
    #         "<div class='feature-card'><h6>Maximize</h6><p>Estimate CLV and future revenue to prioritize your highest-value accounts.</p></div>"
    #         "<div class='feature-card'><h6>Act</h6><p>Generate retention strategies for customers with the highest revenue-at-risk.</p></div>"
    #         "</div>",
    #         unsafe_allow_html=True,
    #     )

    # st.markdown("<div class='panel' style='margin-top:1.5rem;'><h3 style='margin-top:0;'>Data. Insights. Growth.</h3><p class='small-muted'>From data to decisions — build stronger relationships, improve retention, and unlock long-term revenue.</p></div>", unsafe_allow_html=True)
    # with right:
    #     st.markdown(
    #         "<div class='panel' style='height:100%; display:flex; align-items:center; justify-content:center;'>"
    #         "<div style='text-align:center;'>"
    #         "<div style='font-size:1rem; font-weight:700; color:#5b93ff; margin-bottom:1rem;'>Dashboard Preview</div>"
    #         "<div style='background: linear-gradient(180deg, rgba(56, 189, 248, 0.12), rgba(168, 85, 247, 0.08)); border-radius:24px; padding:1rem;'>"
    #         "<div style='width:100%; height:260px; background: rgba(8, 25, 52, 0.95); border-radius:20px; border:1px solid rgba(148, 163, 184, 0.12); box-shadow: 0 18px 50px rgba(0,0,0,0.2);'>"
    #         "<div style='padding:1rem;'><div style='display:flex; justify-content:space-between; margin-bottom:1rem;'>"
    #         "<div style='width:40%; height:14px; background:rgba(255,255,255,0.25); border-radius:99px;'></div>"
    #         "<div style='width:18%; height:14px; background:rgba(255,255,255,0.17); border-radius:99px;'></div>"
    #         "</div>"
    #         "<div style='display:grid; grid-template-columns: 1fr 1fr; gap:0.75rem; margin-bottom:1rem;'>"
    #         "<div style='height:72px; background:rgba(255,255,255,0.08); border-radius:16px;'></div>"
    #         "<div style='height:72px; background:rgba(255,255,255,0.08); border-radius:16px;'></div>"
    #         "</div>"
    #         "<div style='display:flex; gap:0.75rem; margin-bottom:1rem;'><div style='flex:1; height:90px; background:rgba(255,255,255,0.08); border-radius:16px;'></div><div style='flex:1; height:90px; background:rgba(255,255,255,0.08); border-radius:16px;'></div></div>"
    #         "</div></div>"
    #         "</div>"
    #         "</div></div>",
    #         unsafe_allow_html=True,
    #     )

    # st.divider()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="panel" style="text-align:center;">

<h2 style="
color:white;
font-size:34px;
margin-bottom:18px;
">

🚀  Transform Customer Data into Business Growth

</h2>

<div style="
display:flex;
justify-content:center;
gap:18px;
flex-wrap:wrap;
margin-top:20px;
">

<div style="
background:#1e3a8a;
padding:12px 22px;
border-radius:30px;
color:white;
font-weight:600;
font-size:16px;
box-shadow:0 4px 12px rgba(0,0,0,0.3);
">
📉 Predict Churn
</div>

<div style="
background:#0f766e;
padding:12px 22px;
border-radius:30px;
color:white;
font-weight:600;
font-size:16px;
box-shadow:0 4px 12px rgba(0,0,0,0.3);
">
👥 Customer Insights
</div>

<div style="
background:#7c3aed;
padding:12px 22px;
border-radius:30px;
color:white;
font-weight:600;
font-size:16px;
box-shadow:0 4px 12px rgba(0,0,0,0.3);
">
💰 Maximize CLV
</div>

<div style="
background:#ea580c;
padding:12px 22px;
border-radius:30px;
color:white;
font-weight:600;
font-size:16px;
box-shadow:0 4px 12px rgba(0,0,0,0.3);
">
🤖 AI Recommendations
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


#     st.markdown(
# """
# <div class="panel" style="text-align:center;">

# <h2 style="
# color:white;
# font-size:36px;
# font-weight:700;
# margin-bottom:12px;
# ">

# 🚀 Transform Customer Data into Business Growth

# </h2>

# <p style="
# font-size:18px;
# color:#cbd5e1;
# margin-bottom:25px;
# ">

# Predict Churn • Understand Customers • Maximize Revenue • AI-Powered Decisions

# </p>

# </div>
# """,
# unsafe_allow_html=True,
# )


# st.markdown("<div class='panel' style='margin-top:1.5rem;'>"
#         "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1rem;'>"
#         "<div class='capability-card'><h6>Data Integration</h6><p>Seamlessly integrate and prepare customer data from multiple sources.</p></div>"
#         "<div class='capability-card'><h6>Machine Learning</h6><p>Advanced ML models to predict churn, CLV, and customer behavior.</p></div>"
#         "<div class='capability-card'><h6>Customer Insights</h6><p>RFM segmentation and persona analysis for deeper understanding.</p></div>"
#         "<div class='capability-card'><h6>Revenue Analytics</h6><p>Identify revenue-at-risk and growth opportunities with data.</p></div>"
#         "<div class='capability-card'><h6>AI Recommendations</h6><p>Get actionable, AI-powered recommendations to improve retention.</p></div>"
#         "</div></div>", unsafe_allow_html=True)


elif page == "👤 Customer Explorer":

    st.title("👤 Customer Explorer")

    customer_ids = sorted(customer_df["CustomerID"].astype(int).tolist())

    selected_customer = st.selectbox(
        "Select Customer",
        customer_ids,
    )

    try:
        customer = get_customer(selected_customer)

    except Exception as e:
        st.error(f"Unable to load customer.\n\n{e}")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:

        render_kpi_card(
            "Customer ID",
            str(customer["CustomerID"]),
            "Selected Customer",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        render_kpi_card(
            "Segment",
            customer["Segment"],
            "Customer Segment",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        render_kpi_card(
            "Persona",
            customer["Customer_Persona"],
            "Customer Persona",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        render_kpi_card(
            "Risk Category",
            customer["Risk_Category"],
            "Risk Level",
        )

    with col2:

        render_kpi_card(
            "Predicted CLV",
            f"${customer['Predicted_CLV']:,.2f}",
            "Customer Lifetime Value",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        render_kpi_card(
            "Revenue At Risk",
            f"${customer['Revenue_at_Risk']:,.2f}",
            "Potential Revenue Loss",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        render_kpi_card(
            "Churn Probability",
            f"{customer['Churn_Probability']:.2%}",
            "Likelihood of Churn",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        render_kpi_card(
            "Recommended Action",
            customer["Customer_Action"],
            "Business Action",
        )

    render_footer()


elif page == "📊 Executive Dashboard":

    st.title("📊 Executive Dashboard")

    try:

        dashboard = get_dashboard()

        total_customers = dashboard["total_customers"]
        high_risk_customers = dashboard["high_risk"]
        critical_risk_customers = dashboard["critical"]
        avg_clv = dashboard["average_clv"]
        total_revenue_at_risk = dashboard["total_revenue_at_risk"]
        avg_churn_rate = dashboard["average_churn"]

    except Exception as e:

        st.error(f"Unable to load dashboard.\n\n{e}")
        st.stop()

    top_segment = customer_df["Segment"].mode()[0]
    top_persona = customer_df["Customer_Persona"].mode()[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card(
            "👥 Total Customers",
            f"{total_customers:,}",
            "Active customer base",
        )

    with col2:
        render_kpi_card(
            "💰 Revenue at Risk",
            f"${total_revenue_at_risk:,.2f}",
            "Portfolio exposure",
        )

    with col3:

        render_kpi_card(
            "📈 Average CLV",
            f"${avg_clv:,.2f}",
            "Expected customer value",
        )

    with col4:
        render_kpi_card(
            "⚠️ High Risk",
            str(high_risk_customers),
            "Customers needing action",
        )

    st.markdown("---")

    col5, col6, col7 = st.columns(3)

    with col5:
        render_kpi_card(
            "📉 Avg Churn",
            f"{avg_churn_rate:.2%}",
            "Overall churn probability",
        )

    with col6:
        render_kpi_card(
            "🏷️ Top Segment",
            top_segment,
            "Largest segment",
        )

    with col7:
        render_kpi_card(
            "👤 Top Persona",
            top_persona,
            "Most common persona",
        )

    st.markdown("---")

    st.subheader("Top Revenue-at-Risk Customers")

    st.dataframe(
        customer_df.sort_values(
            "Revenue_at_Risk",
            ascending=False,
        ),
        use_container_width=True,
    )

    st.markdown("---")

    st.subheader("Customer Risk Distribution")

    risk_counts = customer_df["Risk_Category"].value_counts().reset_index()

    risk_counts.columns = [
        "Risk Category",
        "Customers",
    ]

    fig = px.pie(
        risk_counts,
        values="Customers",
        names="Risk Category",
        hole=0.45,
        title="Customer Risk Distribution",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("CLV vs Churn Probability")

    fig = px.scatter(
        customer_df,
        x="Predicted_CLV",
        y="Churn_Probability",
        size="Revenue_at_Risk",
        color="Risk_Category",
        hover_data=["CustomerID"],
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    render_footer()


elif page == "🤖 AI Recommendation":

    st.title("🤖 AI Business Recommendation")

    customer_ids = sorted(customer_df["CustomerID"].astype(int).tolist())

    selected_customer = st.selectbox(
        "Select Customer",
        customer_ids,
        key="recommendation_customer",
    )

    if st.button(
        "Generate Recommendation",
        use_container_width=True,
    ):

        with st.spinner("Generating recommendation..."):

            try:

                recommendation = get_recommendation(selected_customer)

                st.session_state["recommendation"] = recommendation

            except Exception as e:

                st.error(f"Error: {e}")

    if st.session_state.get("recommendation"):
        

        st.success("Recommendation Generated Successfully")

        st.markdown(st.session_state["ai_recommendation"])

    render_footer()


elif page == "⚡ Real-Time Prediction":

    st.title("⚡ Real-Time Customer Prediction")

    if "transactions" not in st.session_state:
        st.session_state.transactions = []

    st.subheader("Choose Input Method")

    input_method = st.radio(
        "Input Method",
        ["Manual Entry", "Paste Rows"],
        horizontal=True,
    )

    # ==========================================
    # MANUAL ENTRY
    # ==========================================

    if input_method == "Manual Entry":

        col1, col2 = st.columns(2)

        with col1:

            invoice_no = st.text_input("Invoice Number")

            stock_code = st.text_input("Stock Code")

            description = st.text_input("Description")

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
            )

        with col2:

            invoice_date = st.date_input("Invoice Date")

            unit_price = st.number_input(
                "Unit Price",
                min_value=0.0,
                value=1.0,
            )

            customer_id = st.number_input(
                "Customer ID",
                min_value=1,
                step=1,
            )

            country = st.text_input(
                "Country",
                value="United Kingdom",
            )

        if st.button(
            "➕ Add Transaction",
            use_container_width=True,
        ):

            transaction = {
                "InvoiceNo": invoice_no,
                "StockCode": stock_code,
                "Description": description,
                "Quantity": quantity,
                "InvoiceDate": str(invoice_date),
                "UnitPrice": unit_price,
                "CustomerID": int(customer_id),
                "Country": country,
            }

            if len(st.session_state.transactions) > 0:

                existing_customer = st.session_state.transactions[0]["CustomerID"]

                if int(customer_id) != existing_customer:

                    st.error(
                        f"All transactions must belong to Customer {existing_customer}"
                    )

                else:

                    st.session_state.transactions.append(transaction)

                    st.session_state.pop("prediction", None)

                    st.session_state.pop("ai_recommendation", None)

                    st.success("Transaction added.")

            else:

                st.session_state.transactions.append(transaction)

                st.session_state.pop("prediction", None)

                st.session_state.pop("ai_recommendation", None)

                st.success("Transaction added.")

        # ==========================================
    # PASTE ROWS
    # ==========================================

    elif input_method == "Paste Rows":

        import io

        st.subheader("Paste Customer Transactions")

        st.info(
            """
Copy rows directly from Excel.

Required columns:

InvoiceNo | StockCode | Description | Quantity |
InvoiceDate | UnitPrice | CustomerID | Country
"""
        )

        pasted_text = st.text_area(
            "Paste copied rows here",
            height=220,
        )

        if st.button(
            "📋 Parse Rows",
            use_container_width=True,
        ):

            try:

                df = pd.read_csv(
                    io.StringIO(pasted_text),
                    sep=r"\s{2,}",
                    engine="python",
                    header=None,
                )

                df.columns = [
                    "InvoiceNo",
                    "StockCode",
                    "Description",
                    "Quantity",
                    "InvoiceDate",
                    "UnitPrice",
                    "CustomerID",
                    "Country",
                ]

                # Only one customer allowed
                unique_customers = df["CustomerID"].unique()

                if len(unique_customers) != 1:

                    st.error("Please paste transactions of only ONE customer.")

                else:

                    pasted_customer = int(unique_customers[0])

                    # Match existing customer
                    if len(st.session_state.transactions) > 0:

                        existing_customer = st.session_state.transactions[0][
                            "CustomerID"
                        ]

                        if pasted_customer != existing_customer:

                            st.error(
                                f"""
Current customer is {existing_customer}

Pasted data belongs to {pasted_customer}
"""
                            )

                        else:

                            st.session_state.transactions.extend(
                                df.to_dict(orient="records")
                            )

                            st.session_state.pop("prediction", None)

                            st.session_state.pop("ai_recommendation", None)

                            st.success(f"{len(df)} transactions added.")

                    else:

                        st.session_state.transactions.extend(
                            df.to_dict(orient="records")
                        )

                        st.session_state.pop("prediction", None)

                        st.session_state.pop("ai_recommendation", None)

                        st.success(f"{len(df)} transactions added.")

            except Exception as e:

                st.error(str(e))

        # ==========================================================
    # CURRENT CUSTOMER TRANSACTIONS
    # ==========================================================

    st.markdown("---")

    st.subheader("📝 Current Customer Transactions")

    if len(st.session_state.transactions) == 0:

        st.info("No transactions added yet.")

    else:

        transaction_df = pd.DataFrame(st.session_state.transactions)

        customer_id = transaction_df.iloc[0]["CustomerID"]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Customer ID",
                customer_id,
            )

        with col2:

            st.metric(
                "Transactions Added",
                len(transaction_df),
            )

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Manage Transactions")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🗑 Remove Last Transaction",
                use_container_width=True,
            ):

                st.session_state.transactions.pop()

                st.session_state.pop("prediction", None)

                st.session_state.pop("ai_recommendation", None)

                st.rerun()

        with col2:

            if st.button(
                "🧹 Clear All Transactions",
                use_container_width=True,
            ):

                st.session_state.transactions = []

                st.session_state.pop("prediction", None)

                st.session_state.pop("ai_recommendation", None)

                st.rerun()

        if len(transaction_df) < 3:

            st.warning(
                f"""
        Minimum **3 transactions** are required.

        Current Transactions: **{len(transaction_df)}**
        """
            )

        else:

            st.success("✅ Ready for Prediction")

            if st.button(
                "🚀 Generate Prediction",
                use_container_width=True,
            ):
                with st.spinner("Generating prediction..."):

                    try:

                        customer_ids = {
                            t["CustomerID"] for t in st.session_state.transactions
                        }

                        if len(customer_ids) != 1:

                            st.error(
                                "All transactions must belong to the same customer."
                            )

                        else:

                            prediction = predict_customer(st.session_state.transactions)

                            st.session_state["prediction"] = prediction

                            st.success("Prediction generated successfully.")

                    except Exception as e:

                        st.error(str(e))

        if "prediction" in st.session_state:

            prediction = st.session_state["prediction"]

            st.markdown("---")

            st.subheader("📊 Prediction Summary")

            col1, col2, col3 = st.columns(3)

            with col1:

                render_kpi_card(
                    "👤 Customer ID",
                    prediction["CustomerID"],
                    "Predicted Customer",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            with col2:

                render_kpi_card(
                    "📉 Churn Probability",
                    f"{prediction['Churn_Probability']:.2%}",
                    "Risk of Churn",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            with col3:

                render_kpi_card(
                    "💰 Predicted CLV",
                    f"₹ {prediction['Predicted_CLV']:,.2f}",
                    "Customer Lifetime Value",
                )

            col4, col5, col6 = st.columns(3)

            with col4:

                render_kpi_card(
                    "⚠ Revenue at Risk",
                    f"₹ {prediction['Revenue_at_Risk']:,.2f}",
                    "Potential Revenue Loss",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            with col5:

                render_kpi_card(
                    "🚨 Risk Category",
                    prediction["Risk_Category"],
                    "Customer Risk",
                )

            st.markdown("<br>", unsafe_allow_html=True)

            with col6:

                render_kpi_card(
                    "🎯 Customer Action",
                    prediction["Customer_Action"],
                    "Recommended Action",
                )

            st.markdown("---")

            st.subheader("🤖 AI Business Recommendation")

            if st.button(
                "Generate AI Recommendation",
                use_container_width=True,
            ):

                with st.spinner("Generating AI recommendation..."):

                    try:

                        recommendation = get_prediction_recommendation(prediction)

                        st.session_state["ai_recommendation"] = recommendation

                    except Exception as e:

                        st.error(str(e))


            if st.session_state.get("recommendation"):
                

                st.success("Recommendation Generated Successfully")


                st.markdown(st.session_state["ai_recommendation"])

              


        render_footer()


elif page == "📄 Executive Summary":

    st.title("📄 Executive Summary")

    st.info(
        """
This report summarizes the overall customer intelligence
analysis, key business insights and recommended actions.
"""
    )

    st.markdown(executive_summary)

    render_footer()


elif page == "ℹ️ About":

    st.markdown(
        "<div class='hero-box'><h2 style='margin:0;'>About Customer Intelligence</h2></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='panel'><h3 style='margin-top:0;'>A modern platform for customer retention and revenue growth</h3><p class='small-muted'>This platform combines analytics, machine learning, and generative AI to turn customer signals into high-impact business actions. Explore executive KPIs, customer profiles, AI recommendations, and revenue risk insights in a single workspace.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='panel'>"
        "<h4 style='margin-top:0;'>Platform Capabilities</h4>"
        "<ul style='padding-left:1.2rem; margin:0; color:#cbd5e1;'>"
        "<li>Integrated churn, CLV, and revenue-at-risk analytics</li>"
        "<li>Executive-ready dashboards and KPI summaries</li>"
        "<li>AI-generated customer retention recommendations</li>"
        "<li>FastAPI endpoints for programmatic access</li>"
        "<li>Notebook-driven model development and analysis</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )
    render_footer()
