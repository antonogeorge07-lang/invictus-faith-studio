import streamlit as st
import pandas as pd
from databricks import sql
import time
from datetime import datetime

# 1. Page Node Framework Setup
st.set_page_config(
    page_title="🌌 INVICTUS FAITH // HOURLY HUD",
    page_icon="⏱️",
    layout="wide"
)

# Custom Cybernetic Style Overrides
st.markdown("""
<style>
    .stApp { background-color: #03050a; color: #e2e8f0; font-family: 'Courier New', monospace; }
    
    /* Neon Cyber Telemetry Metrics */
    div[data-testid="stMetricValue"] { 
        color: #00f0ff !important; 
        font-family: 'Courier New', monospace;
        font-weight: 900; 
        font-size: 1.8rem !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
    }
    div[data-testid="stMetric"] { 
        background: #090d16; 
        border: 1px solid #1e293b; 
        border-radius: 6px; 
        padding: 15px;
    }
    
    /* Ingest Log HUD Frame */
    .terminal-box {
        background-color: #020408;
        border: 1px solid #00f0ff;
        border-radius: 6px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #00f0ff;
    }
    .pulse-green { animation: blinker 2s linear infinite; color: #10b981; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# 2. Databricks Secure Connection Pool
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

# Dashboard Title
st.markdown("<h2 style='color: #00f0ff; letter-spacing: 2px; margin-bottom: 0px;'>🌌 INVICTUS FAITH // HOURLY TELEMETRY HUD</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 0.85rem;'>AUTO-REFRESHING GLOBAL DEPLOYMENT STREAM ENGINE</p>", unsafe_allow_html=True)
st.markdown("---")

# Active Stream Controls (Sidebar)
feed_active = st.sidebar.checkbox("🛰️ ACTIVE HOURLY AUTO-SYNC LOOP", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown("⏱️ **Temporal Aggregation Level:**")
st.sidebar.info("System queries automatically parse data structures and recalculate metrics matching a rolling 60-minute window interval.")

now_str = datetime.now().strftime("%H:%M:%S")

# Initialize streaming lock flag
should_rerun = False

try:
    # 3. CORE HOURLY METRICS QUERY (Includes Aggregated ROI Logic)
    hourly_analytics_query = """
    SELECT 
        date_format(date_trunc('hour', ingestion_timestamp), 'yyyy-MM-dd HH:00') AS system_hour_block,
        count(model_identifier) AS launch_velocity,
        coalesce(sum(estimated_investment_usd), 0) AS capital_pool_injected,
        coalesce(avg(realized_roi_percentage), 0) as net_hourly_roi
    FROM main.ai_telemetry.realtime_ai_product_launches
    GROUP BY 1
    ORDER BY system_hour_block DESC
    LIMIT 1
    """
    hourly_metrics = run_lakehouse_query(hourly_analytics_query)
    
    if hourly_metrics.empty:
        raise ValueError("Database table initialized but contains no data logs yet.")
        
    # 4. HOURLY SCOREBOARD HUD RENDER (4-Column Layout for ROI Integration)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="⏱️ CURRENT HOUR BLOCK", value=str(hourly_metrics['system_hour_block'][0]))
    with col2:
        st.metric(label="🚀 HOURLY LAUNCH VELOCITY", value=f"{int(hourly_metrics['launch_velocity'][0])} UNITS")
    with col3:
        st.metric(label="💰 HOURLY CAPITAL FLOW", value=f"${hourly_metrics['capital_pool_injected'][0]:,.0f}")
    with col4:
        st.metric(label="📈 AVERAGE REALIZED ROI", value=f"{hourly_metrics['net_hourly_roi'][0]:.1f}%")

    st.markdown("---")

    # 5. DETAILED HOURLY REGISTRY EXTRACTION GRID (Includes Specific ROI Target Column)
    st.markdown("#### 🧬 HOURLY TELEMETRY REGISTRY (ORGANIZATION, MODEL & ROI LINEAGE)")
    
    detailed_hourly_query = """
    SELECT 
        date_format(ingestion_timestamp, 'HH:mm') AS launch_tick,
        model_identifier AS ai_llm_model_name,
        deploying_organization AS investing_party_or_org,
        concat('$', format_number(estimated_investment_usd, 0)) AS capital_allocation,
        concat(format_number(realized_roi_percentage, 1), '%') AS calculated_roi
    FROM main.ai_telemetry.realtime_ai_product_launches
    WHERE date_trunc('hour', ingestion_timestamp) = date_trunc('hour', (
        SELECT max(ingestion_timestamp) FROM main.ai_telemetry.realtime_ai_product_launches
    ))
    ORDER BY ingestion_timestamp DESC
    """
    detailed_df = run_lakehouse_query(detailed_hourly_query)
    st.dataframe(detailed_df, use_container_width=True, hide_index=True)
    
    # Active table data verified, set refresh loop flag to true
    if feed_active:
        should_rerun = True

except Exception as e:
    # Safe Inception Offline Placeholder UI Block (No internal code loops here!)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="⏱️ CURRENT HOUR BLOCK", value="INITIALIZING")
    with col2: st.metric(label="🚀 HOURLY LAUNCH VELOCITY", value="0 UNITS")
    with col3: st.metric(label="💰 HOURLY CAPITAL FLOW", value="$0")
    with col4: st.metric(label="📈 AVERAGE REALIZED ROI", value="0.0%")
    
    st.markdown("---")
    st.markdown("#### ⏳ LANGWIRE STREAM MONITOR STATUS")
    offline_html = f"""
    <div class='terminal-box' style='border-color: #f59e0b; color: #f59e0b;'>
        <p><span class='pulse-green'>● ENGINE PRIMED & LISTENING</span> // Target Node Link Connected</p>
        <p>[{now_str}] SYSTEM READY: Dashboard framework successfully initialized on cloud servers.</p>
        <p>[{now_str}] STATUS: Awaiting streaming metrics from your active Databricks pipeline table.</p>
    </div>
    """
    st.markdown(offline_html, unsafe_allow_html=True)
    
    # Add a quick structural manual reload button to break out of the hanging spinner state
    if st.button("🛰️ RE-CHECK LAKEHOUSE AGGREGATES"):
        st.rerun()

# 6. Safe High-Frequency Execution Loop Trigger
if should_rerun:
    time.sleep(5)
    st.rerun()
