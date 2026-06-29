

from utils.predictor import predict_customer
import os
from pathlib import Path
from turtle import left
import pandas as pd
import plotly.express as px
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

from utils.groq_utils import generate_business_recommendation

load_dotenv()

st.set_page_config(page_title="Customer Intelligence Dashboard", page_icon="📊", layout="wide")

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


DATA_DIR = ROOT / "data" / "processed"


ROOT_1 = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_1 / "assets"

hero_path = ASSETS_DIR / "hero.png"

HERO_IMAGE = Image.open(hero_path)


PAGES = [
    "🏠 Home",
    "📊 Executive Dashboard",
    "👤 Customer Explorer",
    "🤖 AI Recommendation",
    "⚡ Real-Time Prediction",   # NEW
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

if not DATA_DIR.exists():
    st.error(f"Processed data directory not found: {DATA_DIR}")
    st.stop()

customer_data_candidates = [DATA_DIR / "revenue_at_risk.csv", DATA_DIR / "revenue_at_risk_analysis.csv"]
data_path = next((path for path in customer_data_candidates if path.exists()), None)

if data_path is None:
    st.error("No revenue-at-risk dataset was found in the processed data folder.")
    st.stop()

@st.cache_data(show_spinner=False)
def load_customer_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
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


@st.cache_data(show_spinner=False)
def load_summary(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Executive summary not generated yet."


REPORTS_DIR = ROOT / "reports"

customer_df = load_customer_data(data_path)
summary_path = REPORTS_DIR / "executive_summary.md"
executive_summary = load_summary(summary_path)


def render_footer():
    st.markdown("---")
    st.caption("Developed by Aman Rajpoot | Customer Intelligence & Revenue Growth Platform")


def render_kpi_card(title: str, value: str, subtitle: str):
    st.markdown(
        f"""
        <div class="panel">
            <div class="small-muted">{title}</div>
            <div style="font-size: 1.45rem; font-weight: 700; color: #f8fafc; margin-top: 0.2rem;">{value}</div>
            <div class="small-muted" style="margin-top: 0.2rem;">{subtitle}</div>
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
    unsafe_allow_html=True
    )

    left, center,right=st.columns([0.9, 6, 0.09])

    with center:

        st.image(
            HERO_IMAGE,
            width=750,
        )



    st.markdown("<br>", unsafe_allow_html=True)


    col1,col2,col3,col4=st.columns(4)

    with col1:

        st.markdown("""
        <div class="feature-card">

        <h2>📉</h2>

        <h4>Predict</h4>

        Predict customer churn using
        Machine Learning models.

        </div>
        """,unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">

        <h2>👥</h2>

        <h4>Understand</h4>

        Perform RFM Segmentation
        and Customer Persona Analysis.

        </div>
        """,unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="feature-card">

        <h2>💰</h2>

        <h4>Maximize</h4>

        Estimate Customer Lifetime Value
        to improve business growth.

        </div>
        """,unsafe_allow_html=True)

    with col4:

        st.markdown("""
        <div class="feature-card">

        <h2>🤖</h2>

        <h4>Act</h4>

        Generate AI-powered
        business recommendations.

        </div>
        """,unsafe_allow_html=True)


        
    

  

    

    

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
        

    
                
    #st.markdown("<div class='panel' style='margin-top:1.5rem;'><h3 style='margin-top:0;'>Data. Insights. Growth.</h3><p class='small-muted'>From data to decisions — build stronger relationships, improve retention, and unlock long-term revenue.</p></div>", unsafe_allow_html=True)
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

    st.markdown("<br><br>",unsafe_allow_html=True)


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

elif page == "📊 Executive Dashboard":
    st.title("Executive Dashboard")

    total_customers = len(customer_df)
    high_risk_customers = int((customer_df["Risk_Category"].str.contains("High|Critical", case=False, na=False)).sum())
    critical_risk_customers = int((customer_df["Risk_Category"].str.contains("Critical", case=False, na=False)).sum())
    avg_clv = customer_df["Predicted_CLV"].mean()
    total_revenue_at_risk = customer_df["Revenue_at_Risk"].sum()
    avg_churn_rate = customer_df["Churn_Probability"].mean()
    top_segment = customer_df["Segment"].value_counts().idxmax()
    top_persona = customer_df["Customer_Persona"].value_counts().idxmax()
    highest_revenue_customer = customer_df.loc[customer_df["Revenue_at_Risk"].idxmax(), "CustomerID"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("👥 Total Customers", f"{total_customers:,}", "Active customer base")
    with col2:
        render_kpi_card("💰 Revenue at Risk", f"${total_revenue_at_risk:,.2f}", "Exposure across portfolio")
    with col3:
        render_kpi_card("📈 Avg CLV", f"${avg_clv:,.2f}", "Expected customer value")
    with col4:
        render_kpi_card("⚠️ High Risk", f"{high_risk_customers}", "Customers needing action")

    st.markdown("---")
    col5, col6, col7 = st.columns(3)
    with col5:
        render_kpi_card("📉 Avg Churn %", f"{avg_churn_rate:.2%}", "Overall churn outlook")
    with col6:
        render_kpi_card("🏷️ Top Segment", str(top_segment), "Largest segment")
    with col7:
        render_kpi_card("🧑 Top Persona", str(top_persona), "Most common persona")

    st.subheader("Top Customers by Revenue at Risk")
    st.dataframe(
        customer_df[["CustomerID", "Segment", "Customer_Persona", "Churn_Probability", "Predicted_CLV", "Revenue_at_Risk", "Risk_Category", "Customer_Action"]]
        .sort_values("Revenue_at_Risk", ascending=False)
        .head(20),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("Customer Risk Distribution")
    risk_counts = customer_df["Risk_Category"].value_counts().reset_index()
    risk_counts.columns = ["Risk_Category", "Customers"]
    risk_fig = px.pie(
        risk_counts,
        values="Customers",
        names="Risk_Category",
        title="Risk Category Breakdown",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(risk_fig, use_container_width=True)

    st.subheader("CLV vs Churn Probability")
    scatter_fig = px.scatter(
        customer_df,
        x="Predicted_CLV",
        y="Churn_Probability",
        size="Revenue_at_Risk",
        color="Risk_Category",
        hover_data=["CustomerID"],
        title="CLV vs Churn Probability by Revenue at Risk",
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.subheader("Top 10 Customers by Revenue at Risk")
    top_customers = customer_df[["CustomerID", "Revenue_at_Risk", "Risk_Category"]].sort_values("Revenue_at_Risk", ascending=False).head(10)
    top_fig = px.bar(
        top_customers,
        x="Revenue_at_Risk",
        y="CustomerID",
        color="Risk_Category",
        orientation="h",
        labels={"CustomerID": "Customer ID", "Revenue_at_Risk": "Revenue at Risk"},
        title="Top 10 Customers by Revenue at Risk",
    )
    st.plotly_chart(top_fig, use_container_width=True)
    render_footer()

elif page == "👤 Customer Explorer":
    st.title("Customer Explorer")

    search_term = st.text_input("Search Customer ID")
    if search_term:
        filtered_df = customer_df[customer_df["CustomerID"].astype(str).str.contains(search_term, case=False, na=False)]
    else:
        filtered_df = customer_df

    customer_ids = sorted(filtered_df["CustomerID"].astype(int).tolist())
    if not customer_ids:
        st.warning("No matching customers found.")
        render_footer()
        st.stop()
    selected_customer = st.selectbox("Select a customer", customer_ids)
    customer_row = customer_df[customer_df["CustomerID"] == selected_customer].iloc[0]

    st.markdown(f"<div class='hero-box'><h3 style='margin:0;'>Customer {selected_customer}</h3><p style='margin:0.2rem 0 0 0; color:#f8fafc;'>Segment: {customer_row.get('Segment', 'Unknown')} | Persona: {customer_row.get('Customer_Persona', 'Unknown')}</p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("📉 Churn Probability", f"{customer_row.get('Churn_Probability', 0):.2%}", "Customer churn outlook")
    with col2:
        render_kpi_card("💎 Predicted CLV", f"${customer_row.get('Predicted_CLV', 0):,.2f}", "Future customer value")
    with col3:
        render_kpi_card("⚠️ Revenue at Risk", f"${customer_row.get('Revenue_at_Risk', 0):,.2f}", "Monetary exposure")

    st.subheader("Customer Profile")
    profile_df = pd.DataFrame(
        [
            {
                "Customer ID": int(customer_row["CustomerID"]),
                "Segment": customer_row.get("Segment", "Unknown"),
                "Persona": customer_row.get("Customer_Persona", "Unknown"),
                "Churn Probability": customer_row.get("Churn_Probability", 0),
                "Predicted CLV": customer_row.get("Predicted_CLV", 0),
                "Revenue at Risk": customer_row.get("Revenue_at_Risk", 0),
                "Risk Category": customer_row.get("Risk_Category", "Unknown"),
                "Customer Action": customer_row.get("Customer_Action", "Monitor"),
            }
        ]
    )
    st.dataframe(profile_df, use_container_width=True)
    # ----------------------------------------------------------
# Download Selected Customer Report
# ----------------------------------------------------------

    customer_report = profile_df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Customer Report",
        data=customer_report,
        file_name=f"customer_{selected_customer}_report.csv",
        mime="text/csv",
    )
    
    render_footer()

elif page == "🤖 AI Recommendation":

    st.title("🤖 AI Recommendation")

    search_term = st.text_input("Search Customer ID")

    if search_term:
        filtered_df = customer_df[
            customer_df["CustomerID"].astype(str).str.contains(
                search_term,
                case=False,
                na=False,
            )
        ]
    else:
        filtered_df = customer_df

    customer_ids = sorted(filtered_df["CustomerID"].astype(int).tolist())

    if not customer_ids:
        st.warning("No customer found.")
        st.stop()

    selected_customer = st.selectbox(
        "Choose Customer",
        customer_ids,
    )

    customer_row = customer_df[
        customer_df["CustomerID"] == selected_customer
    ].iloc[0]

    

    if st.button("Generate AI Recommendation"):

        try:

            with st.spinner("Generating..."):

                recommendation = generate_business_recommendation(
                    customer_row.to_dict()
                )

            

            

            

            st.session_state["recommendation"] = recommendation

        except Exception as e:

            st.exception(e)

    

    if st.session_state.get("recommendation"):

        st.success("Recommendation")

        st.write(st.session_state["recommendation"])

    else:

        st.warning("No recommendation available.")





elif page == "⚡ Real-Time Prediction":

    st.title("⚡ Real-Time Customer Prediction")

    st.markdown(
        "Enter customer transaction details below."
    )

    st.divider()

    st.subheader("Customer Transaction")

    # customer_id = st.number_input(
    #     "Customer ID",
    #     min_value=1,
    #     step=1,
    # )

    st.subheader("Customer Information")

    # Customer ID is entered only once
    if len(st.session_state.transactions) == 0:

        customer_id = st.number_input(
            "Customer ID",
            min_value=1,
            step=1,
            key="customer_id",
        )

    else:

        customer_id = st.session_state.transactions[0]["CustomerID"]

        st.text_input(
            "Customer ID",
            value=str(customer_id),
            disabled=True,
        )

    invoice_date = st.date_input(
        "Invoice Date",
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
    )

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.01,
        value=1.00,
    )

    country = st.text_input(
        "Country",
        value="United Kingdom",
    )

    description = st.text_input(
        "Description",
    )

    stock_code = st.text_input(
        "Stock Code",
    )

    if st.button(
        "➕ Add Transaction",
        use_container_width=True,
    ):

        invoice_no = (
            f"INV{len(st.session_state.transactions)+1}"
        )

        transaction = {

            "InvoiceNo": invoice_no,

            "StockCode": stock_code,

            "Description": description,

            "Quantity": quantity,

            "InvoiceDate": str(invoice_date),

            "UnitPrice": unit_price,

            "CustomerID": customer_id,

            "Country": country,

        }

        st.session_state.transactions.append(
            transaction
        )

        st.success(
            "Transaction added successfully."
        )

    st.divider()

    st.subheader("Current Transactions")

    if st.session_state.transactions:

        transaction_df = pd.DataFrame(
            st.session_state.transactions
        )

        transaction_df["Revenue"] = (
            transaction_df["Quantity"]
            * transaction_df["UnitPrice"]
        )

        st.dataframe(
            transaction_df,
            use_container_width=True,
        )

    else:

        st.info(
            "No transactions added yet."
        )

    st.divider()

    # st.button(
    #     "🚀 Predict Customer",
    #     use_container_width=True,
    # )


 # ----------------------------------------------------------
# Predict Customer
# ----------------------------------------------------------
# ----------------------------------------------------------
# Action Buttons
# ----------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        predict = st.button(
            "🚀 Predict Customer",
            use_container_width=True,
            type="primary",
        )

    with col2:

        clear_customer = st.button(
            "🗑️ Clear & New Customer",
            use_container_width=True,
        )

    # ----------------------------------------------------------
    # Clear Current Customer
    # ----------------------------------------------------------

    if clear_customer:

        st.session_state["transactions"] = []


        st.session_state.pop("prediction_result", None)

        st.session_state.pop("recommendation", None)


        st.rerun()

    # ----------------------------------------------------------
    # Predict Customer
    # ----------------------------------------------------------

    if predict:

        if len(st.session_state.transactions) == 0:

            st.warning(
                "Please add at least one transaction."
            )

        else:

            transaction_df = pd.DataFrame(
                st.session_state.transactions
            )

            if len(transaction_df) < 3:

                st.warning(
                    """
    ⚠️ This prediction is based on fewer than **3 transactions**.

    The model was trained using customers with purchase history,
    so predictions for customers with very limited transactions
    may be less reliable.
    """
                )

            try:

                with st.spinner(
                    "Predicting customer..."
                ):

                    result = predict_customer(
                        transaction_df
                    )

                st.session_state["prediction_result"] = result


                st.session_state.pop(
        "recommendation",
        None,
    )

                st.success(
                    "Prediction completed successfully."
                )

            except Exception as e:

                st.exception(e)


    # ----------------------------------------------------------
    # Show Prediction Result
    # ----------------------------------------------------------
    if (
        "prediction_result" in st.session_state
        and st.session_state["prediction_result"] is not None):



        result = st.session_state["prediction_result"]

        st.divider()

        st.subheader("📊 Prediction Results")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Customer Persona",
            result["Customer_Persona"],
        )

        c2.metric(
            "Churn Probability",
            f"{result['Churn_Probability']:.2%}",
        )

        c3.metric(
            "Predicted CLV",
            f"${result['Predicted_CLV']:,.2f}",
        )

        c4, c5, c6 = st.columns(3)

        c4.metric(
            "Revenue at Risk",
            f"${result['Revenue_at_Risk']:,.2f}",
        )

        c5.metric(
            "Risk Category",
            result["Risk_Category"],
        )
        

        st.divider()

        st.subheader("📌 Recommended Business Action")


        st.info(
        result["Customer_Action"]
    )

    # ----------------------------------------------------------
    # AI Recommendation
    # ----------------------------------------------------------

    st.divider()

    if st.button(
        "🤖 Generate AI Recommendation",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Generating AI recommendation..."
            ):

                recommendation = generate_business_recommendation(
                    result
                )

                st.session_state["recommendation"] = recommendation

        except Exception as e:

            st.exception(e)

    # ----------------------------------------------------------
    # Display AI Recommendation
    # ----------------------------------------------------------

    if (
        "recommendation" in st.session_state
        and st.session_state["recommendation"] is not None
    ):

        st.subheader("🤖 AI Business Recommendation")

        st.markdown(
            st.session_state["recommendation"]
        )

        render_footer()


elif page == "📄 Executive Summary":

    st.markdown("<div class='hero-box'><h2 style='margin:0;'>📄 Executive Summary</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'>{executive_summary}</div>", unsafe_allow_html=True)
    render_footer()

elif page == "ℹ️ About":

    st.markdown("<div class='hero-box'><h2 style='margin:0;'>About Customer Intelligence</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'><h3 style='margin-top:0;'>A modern platform for customer retention and revenue growth</h3><p class='small-muted'>This platform combines analytics, machine learning, and generative AI to turn customer signals into high-impact business actions. Explore executive KPIs, customer profiles, AI recommendations, and revenue risk insights in a single workspace.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>"
                "<h4 style='margin-top:0;'>Platform Capabilities</h4>"
                "<ul style='padding-left:1.2rem; margin:0; color:#cbd5e1;'>"
                "<li>Integrated churn, CLV, and revenue-at-risk analytics</li>"
                "<li>Executive-ready dashboards and KPI summaries</li>"
                "<li>AI-generated customer retention recommendations</li>"
                "<li>FastAPI endpoints for programmatic access</li>"
                "<li>Notebook-driven model development and analysis</li>"
                "</ul>"
                "</div>",
                unsafe_allow_html=True)
    render_footer()
