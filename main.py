import streamlit as st
import pandas as pd
from databricks import sql
import time

st.set_page_config(page_title="INVICTUS FAITH - DATABRICKS HUD", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070f; color: #f1f5f9; }
    div[data-testid="stMetricValue"] { color: #00f0ff !important; font-family: 'Courier New', monospace; font-weight: 800; }
    div[data-testid="stMetric"] { background: #0b111e; border: 1px solid #1e293b; border-radius: 8px; padding: 15px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(ttl=60)
def get_databricks_client():
    return sql.connect(
        server_hostname=st.secrets["databricks"]["server_hostname"],
        http_path=st.secrets["databricks"]["http_path"],
        access_token=st.secrets["databricks"]["access_token"]
    )

def run_lakehouse_query(query_string):
    with get_databricks_client() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_string)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)

st.markdown("<h2 style='color: #00f0ff; margin-bottom: 0px;'>🌌 INVICTUS FAITH // LAKEHOUSE INTEGRATION</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 0.9rem;'>LIVE TELEMETRY EXTRACTED DIRECTLY FROM DATABRICKS UNITY CATALOG</p>", unsafe_allow_html=True)
st.markdown("---")

feed_active = st.sidebar.checkbox("🛰️ CONNECT STREAMING LAKEHOUSE ENGINE", value=True)

try:
    metrics_query = """
    SELECT 
        count(model_identifier) as live_nodes,
        coalesce(sum(estimated_investment_usd), 0) as capital_pool,
        coalesce(avg(realized_roi_percentage), 0) as avg_roi
    FROM main.ai_telemetry.realtime_ai_product_launches
    """
    metrics_df = run_lakehouse_query(metrics_query)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="TOTAL GLOBAL AI CAPITAL INJECTED", value=f"${metrics_df['capital_pool'][0]:,.0f}")
    with col2:
        st.metric(label="ACTIVE MODEL DEPLOYMENT NODES", value=f"{int(metrics_df['live_nodes'][0])} LIVE")
    with col3:
        st.metric(label="AVERAGE SYSTEM REALIZED ROI YIELD", value=f"{metrics_df['avg_roi'][0]:.1f}%")

    st.markdown("---")
    st.markdown("#### ⏳ DATABRICKS DELTA LAKE INSIGHT TICKER (LIVE INGEST)")
    
    ticker_query = """
    SELECT 
        date_format(ingestion_timestamp, 'HH:mm:ss') as tick_time,
        model_identifier as model_spec,
        ai_category_vector as category,
        concat('$', format_number(estimated_investment_usd, 0)) as investment,
        realized_roi_percentage as roi
    FROM main.ai_telemetry.realtime_ai_product_launches
    ORDER BY ingestion_timestamp DESC
    LIMIT 5
    """
    ticker_df = run_lakehouse_query(ticker_query)
    st.table(ticker_df)

except Exception as e:
    st.warning("🔒 Waiting for Databricks Lakehouse Pipeline Synchronization...")
    st.info("The application dashboard structure is running perfectly. Once your background Databricks notebook streaming job begins writing to main.ai_telemetry.realtime_ai_product_launches, this pipeline hud will instantly light up with streaming statistics.")

if feed_active:
    time.sleep(5)
    st.rerun()
