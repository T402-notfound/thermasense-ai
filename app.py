import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ThermaSense AI - Industrial Grid", layout="wide")

# --- CUSTOM DEEP DARK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
        color: #eceff4;
    }
    div.row-widget.stRadio > div{
        background-color: #111827;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #374151;
    }
    .metric-card {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #3b82f6; margin-bottom: 15px;
    }
    .metric-card-agro {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #10b981; margin-bottom: 15px;
    }
    .metric-card-money {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #eab308; margin-bottom: 15px;
    }
    .box-report {
        background-color: #111827; padding: 20px; border-radius: 8px;
        border: 1px solid #4b5563; margin-top: 15px;
    }
    .valve-box {
        background-color: #111827; padding: 15px; border-radius: 8px;
        border: 1px solid #374151; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL SYSTEM TITLE IN MAIN AREA ---
st.title("🏭 ThermaSense AI Platform")
st.markdown("<h4 style='color:#9ca3af; margin-top:-15px;'>Algorithmic Routing & Inter-Sectorial Energy Optimization (Cement + Agro)</h4>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# SIDEBAR CONTROL & NAVIGATION UNIT
# ==========================================
st.sidebar.image("https://img.icons8.com/external-flatart-icons-flat-flatarticons/128/external-factory-industry-flatart-icons-flat-flatarticons.png", width=70)
st.sidebar.title("🎛️ Control Center")
st.sidebar.write("---")

# 1. Sidebar Radio Navigation
st.sidebar.subheader("📂 Navigation")
navigation_page = st.sidebar.radio(
    "Select an interface:",
    [
        "🏢 1. Factory Internal Optimization", 
        "🚜 2. Agro Consumption & Billing", 
        "🗓️ 3. Seasonal Variability Matrix", 
        "📊 4. Annual Report & Predictive Vision"
    ]
)

st.sidebar.write("---")

# 2. Simulation Sliders
st.sidebar.subheader("🕹️ Live Ingestion Configuration")
clinker_load = st.sidebar.slider("Cement Kiln Thermal Load (%)", 40, 100, 85)

st.sidebar.markdown("""
<div style='background-color:#111827; padding:10px; border-radius:5px; border-left:3px solid #10b981;'>
<small style='color:#10b981;'>● SCADA Stream Live</small><br>
<small style='color:#9ca3af;'>Status: Connected to Kiln 1</small>
</div>
""", unsafe_allow_html=True)

# --- GLOBAL CALCULATION MATRIX ---
total_energy_recovered = int(clinker_load * 12.5) 
water_heating_internal = int(total_energy_recovered * 0.15)
drying_internal = int(total_energy_recovered * 0.45)
factory_total_internal = water_heating_internal + drying_internal

farms_allocated_energy = total_energy_recovered - factory_total_internal

# Dynamic calculations for Valve Actuation %
valve_internal_pct = int((factory_total_internal / total_energy_recovered) * 100) if total_energy_recovered > 0 else 0
valve_external_pct = 100 - valve_internal_pct

# Financial rates (MAD per kWh)
traditional_energy_cost = 0.85 
agro_discounted_rate = 0.35    

factory_hourly_savings = int(factory_total_internal * traditional_energy_cost)
farms_hourly_revenue = int(farms_allocated_energy * agro_discounted_rate)


# ==========================================
# RENDER PAGES BASED ON SIDEBAR SELECTION
# ==========================================

# 🏢 PAGE 1: FACTORY OPTIMIZATION
if navigation_page == "🏢 1. Factory Internal Optimization":
    st.header("🏢 Cement Plant Internal Consumption & Savings")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><h4>Total Energy Captured</h4><h2>{total_energy_recovered} kW</h2><small>Gross recovered exergy stream</small></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h4>Water Heating & Drying</h4><h2>{factory_total_internal} kW</h2><small>Water ({water_heating_internal} kW) | Drying ({drying_internal} kW)</small></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card-money"><h4>Substituted OPEX Avoided</h4><h2>+ {factory_hourly_savings} DH/h</h2><small>Saved classical fossil-fuel costs</small></div>', unsafe_allow_html=True)
    
    # 🤖 جودة الإضافة هنا: عرض حالة الصمامات الأوتوماتيكية الحية بناءً على خوارزمية الـ AI
    st.write("---")
    st.subheader("🤖 Smart Thermal Routing Valves (AI Autonomous Control)")
    st.markdown("<small style='color:#9ca3af;'>Real-time dynamic actuators adjustment based on SCADA feed without human intervention.</small>", unsafe_allow_html=True)
    
    v1, v2 = st.columns(2)
    with v1:
        st.markdown(f"""
        <div class="valve-box" style="border-top: 4px solid #3b82f6;">
            <h5 style="color:#3b82f6;">🔒 Valve V-101 (Factory Core Internal)</h5>
            <h2 style="margin:10px 0;">{valve_internal_pct}% OPEN</h2>
            <small style="color:#9ca3af;">Routing heat to pre-heating loops & mills</small>
        </div>
        """, unsafe_allow_html=True)
    with v2:
        st.markdown(f"""
        <div class="valve-box" style="border-top: 4px solid #10b981;">
            <h5 style="color:#10b981;">🌍 Valve V-102 (Agro External Grid)</h5>
            <h2 style="margin:10px 0;">{valve_external_pct}% OPEN</h2>
            <small style="color:#9ca3af;">Routing surplus exergy to agricultural micro-grids</small>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("---")
    st.subheader("🔮 Weekly Internal Savings Forecast (Next 7 Days)")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    np.random.seed(42) 
    pred_factory_savings = [factory_hourly_savings * 24 * np.random.uniform(0.9, 1.1) for _ in range(7)]
    df_factory = pd.DataFrame({'Days': days, 'Generated Savings (DH)': pred_factory_savings}).set_index('Days')
    st.bar_chart(df_factory)

# 🚜 PAGE 2: AGRO DEMAND
elif navigation_page == "🚜 2. Agro Consumption & Billing":
    st.header("🚜 Local Agricultural Sector Consumption & Invoicing")
    ca1, ca2, ca3 = st.columns(3)
    with ca1:
        st.markdown(f'<div class="metric-card-agro"><h4>Thermal Flow Routed to Agro</h4><h2>{farms_allocated_energy} kW</h2><small>Direct micro-grid surplus injection</small></div>', unsafe_allow_html=True)
    with ca2:
        st.markdown(f'<div class="metric-card-agro"><h4>Discounted Green Rate</h4><h2>{agro_discounted_rate} DH / kWh</h2><small>Standard Grid Cost: 0.85 DH/kWh (Attractive Offer)</small></div>', unsafe_allow_html=True)
    with ca3:
        st.markdown(f'<div class="metric-card-money"><h4>Billing Secondary Revenue</h4><h2>+ {farms_hourly_revenue} DH/h</h2><small>Secondary cash loop for the cement plant</small></div>', unsafe_allow_html=True)
    
    st.subheader("⏰ Weekly Demand & Consumption Forecasting via Daily Profile")
    hours_profile = ['Morning', 'Noon', 'Evening', 'Night']
    pred_agro_demand = [farms_allocated_energy * 0.8, farms_allocated_energy * 0.4, farms_allocated_energy * 1.2, farms_allocated_energy * 1.5]
    df_agro = pd.DataFrame({'Day Period': hours_profile, 'Estimated Consumption (kW)': pred_agro_demand}).set_index('Day Period')
    st.line_chart(df_agro)

# 🗓️ PAGE 3: SEASONAL VARIABILITY
elif navigation_page == "🗓️ 3. Seasonal Variability Matrix":
    st.header("🗓️ Macro-Grid Consumption Balance Matrix Across Seasons")
    st.write("Cross-technical macro analysis of Supply/Demand equilibrium (Plant + Agro Grid)")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.subheader("❄️ Standard Profile: Winter Season")
        st.markdown("""
        * **Agro Demand (Greenhouses):** Critical Peak (High heating requirements during freezing nights).
        * **AI Routing Strategy:** Absolute automated priority given to external agricultural cooperative grids.
        * **Billing Revenues:** Maximum Yield (+30% secondary cash generation).
        * **Plant Internal Drying:** Reduced to baseline technical nominal flow.
        """)
        chart_winter = pd.DataFrame({'Thermal Flow': ['Internal Water', 'Internal Drying', 'Agro Micro-Grids'], 'kW': [water_heating_internal, drying_internal * 0.5, farms_allocated_energy * 1.5]}).set_index('Thermal Flow')
        st.bar_chart(chart_winter, color="#3b82f6")

    with col_s2:
        st.subheader("☀️ Standard Profile: Summer Season")
        st.markdown("""
        * **Agro Demand (Greenhouses):** Absolute Minimum (Only occasional localized crop drying).
        * **AI Routing Strategy:** Total autonomous re-routing inward to accelerate raw material grinding mill cycles.
        * **Factory Efficiency:** Peak internal optimization (Zero atmospheric heat loss, maximized internal OPEX reduction).
        * **Billing Revenues:** Moderate but highly stable.
        """)
        chart_summer = pd.DataFrame({'Thermal Flow': ['Internal Water', 'Internal Drying', 'Agro Micro-Grids'], 'kW': [water_heating_internal, drying_internal * 1.3, farms_allocated_energy * 0.2]}).set_index('Thermal Flow')
        st.bar_chart(chart_summer, color="#10b981")

# 📊 PAGE 4: ANNUAL & PREDICTIVE VISION
elif navigation_page == "📊 4. Rapport Annuel & Vision Predictive":
    st.header("📊 Annual Energy Balance Consolidation & Y+1 Strategy")
    
    cy1, cy2, cy3 = st.columns(3)
    annual_savings = factory_hourly_savings * 24 * 365
    annual_revenue = farms_hourly_revenue * 24 * 365
    total_annual_impact = annual_savings + annual_revenue
    
    with cy1:
        st.markdown(f'<div class="metric-card-money" style="border-left:5px solid #eceff4;"><h4>Annual Valorized Energy</h4><h2>{(total_energy_recovered * 24 * 365):,} kWh</h2><small>Consolidated balance (Plant + Agro)</small></div>', unsafe_allow_html=True)
    with cy2:
        st.markdown(f'<div class="metric-card-money"><h4>Global Financial Impact</h4><h2>{total_annual_impact:,} DH / year</h2><small>Savings ({annual_savings:,} DH) | Sales ({annual_revenue:,} DH)</small></div>', unsafe_allow_html=True)
    with cy3:
        st.markdown(f'<div class="box-report" style="border-left: 5px solid #ef4444; margin-top:0px;"><h4>Displaced CO2 Emissions</h4><h2>~ 648 Tonnes / year</h2><small>Direct atmospheric environmental impact</small></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🔮 Predictive Analytics & Strategic Roadmap for the Upcoming Year (2027)")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.write("### 📈 Consumption Rationalization Trajectory")
        st.info("🤖 **AI Predictive Engine Insight:** By optimizing raw material drying schedules based on next year's core production forecasting models, the plant can increase its thermal self-sufficiency coefficient by an extra **4.2%**, cutting down residual auxiliary fossil fuel ignition costs.")
    with col_v2:
        st.markdown(f"""
        <div class="box-report">
            <h4>📋 Strategic Action Plan (AI Automated Optimization)</h4>
            <hr style='border-color:#4b5563;'>
            • <b>Grid Scaling:</b> Integrate 3 new peripheral agricultural cooperatives into the thermal loop by Q2.<br>
            • <b>Dynamic Regulation:</b> Achieve full autonomous orchestration of routing actuators using the deployed digital twin framework.<br>
            • <b>Target ROI Schedule:</b> Total physical infrastructure amortization achieved in <b>14 months</b>.
        </div>
        """, unsafe_allow_html=True)
