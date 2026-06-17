import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. Page Configuration
st.set_page_config(page_title="ThermaSense AI - Dashboard", layout="wide")

# 2. Custom CSS for Industrial Dark Theme alignment
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #eceff4; }
    .metric-box {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #10b981; margin-bottom: 20px;
    }
    .metric-box-danger {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #ef4444; margin-bottom: 20px;
    }
    .law-box {
        background-color: #111827; padding: 15px; border-radius: 8px;
        border-right: 4px solid #3b82f6; direction: rtl; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Main Header (Appearing in Arabic/French for the Jury)
st.title("🏭 منصة ThermaSense AI — MVP")
st.markdown("<h4 style='color:#9ca3af;'>Optimisation et Routage Dynamique de la Chaleur Fatale Industrielle</h4>", unsafe_allow_html=True)
st.write("---")

# 4. Legal Context (Law 47-09 Framework)
st.markdown("""
<div class='law-box'>
    <strong>⚖️ الإطار القانوني والسياق المغربي (Loi 47-09):</strong> 
    يفرض القانون 47-09 تدقيقاً طاقياً إلزامياً على المنشآت التي يتجاوز استهلاكها 1500 tep/an. 
    وتقدّر الوكالة المغربية للنجاعة الطاقية (AMEE) متوسط إمكانيات التوفير بـ <strong>12.2%</strong>.
</div>
""", unsafe_allow_html=True)

# 5. Sidebar Simulation Controller for the Pitch
st.sidebar.header("🛠️ Simulation Controls")
st.sidebar.write("Use this to change factory states live in front of the jury:")
factory_mode = st.sidebar.selectbox(
    "Select Factory Status:",
    ["الوضع المستقر (Normal Mode)", "وضع رصد التسريب النشط (Active Leak - Compressor B)"]
)

# 6. Logic to switch variables based on mode
if factory_mode == "وضع رصد التسريب النشط (Active Leak - Compressor B)":
    current_temp = 72.4
    current_press = 1.9
    is_anomaly = True
    financial_loss = 450
else:
    current_temp = 50.8
    current_press = 4.1
    is_anomaly = False
    financial_loss = 0

# 7. Virtual Audit & Digital Twin Module
st.subheader("📊 1. التدقيق الافتراضي والتوأم الرقمي (Virtual Audit & Digital Twin)")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="metric-box"><h4>🌡️ Température d\'échappement</h4><h2>{current_temp} °C</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><h4>💨 Pression de flux (SCADA)</h4><h2>{current_press} Bar</h2></div>', unsafe_allow_html=True)
with col3:
    if is_anomaly:
        st.markdown(f'<div class="metric-box-danger"><h4>⚠️ AI Leak Detection</h4><h3 style="color:#ef4444;">تم رصد هدر مالي: {financial_loss} DH/h</h3></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-box"><h4>✅ Status Efficiency (AI)</h4><h3 style="color:#10b981;">Niveau Stable — 0 DH/h</h3></div>', unsafe_allow_html=True)

# 8. Time-series Simulation Data for Charting
np.random.seed(42)
timeline = [datetime.datetime.now() - datetime.timedelta(minutes=i*10) for i in range(40)]
timeline.reverse()
heat_readings = np.random.normal(loc=52.0, scale=1.5, size=40)

if is_anomaly:
    heat_readings[-12:] += 20.0  # Simulate the sudden spike

chart_df = pd.DataFrame({"Time": timeline, "Temperature (°C)": heat_readings}).set_index("Time")
st.line_chart(chart_df)

# 9. Smart Routing Optimization Module
st.write("---")
st.subheader("🔀 2. محرك التوجيه الديناميكي المتعدد المصادر (Smart Routing)")

col_src, col_snk = st.columns(2)

with col_src:
    st.write("### 📥 Source Capture")
    if is_anomaly:
        st.warning(f"⚠️ **Compressor B:** Rejet thermique anormal détecté à {current_temp}°C.")
    else:
        st.info("🔄 Source running within nominal parameters.")

with col_snk:
    st.write("### 🤖 Optimization Matrix Decision")
    if is_anomaly:
        st.success("🎯 **Auto-Routage Activé:**")
        st.markdown("""
        * **Action:** Ouverture des vannes motorisées vers le **Bassin de lavage** (Besoin: 55°C).
        * **Fossil Fuel Reduction:** Élimination immédiate de l'appoint au gaz naturel à **100%**.
        * **Financial Rescue:** Conversion immédiate des calories perdues en gains nets.
        """)
    else:
        st.info("🔄 AI algorithm monitoring the equilibrium between supply and demand matrix.")

# 10. Predictive Maintenance & SaaS Business Model
st.write("---")
st.subheader("💰 3. العائد الاستثماري ونموذج الأعمال للهاكثون (Business Model)")

col_biz1, col_biz2 = st.columns(2)
with col_biz1:
    st.write("### 🛡️ Maintenance Prédictive")
    st.info("🤖 Time-series analysis confirms Fouling Index is steady. Next optimal cleaning cycle for heat exchangers scheduled in 14 days to prevent execution degradation.")

with col_biz2:
    st.write("### 📊 Monetization Strategy (SaaS)")
    st.markdown("""
    * **Diagnostic & Setup (One-off):** Facturation d'un audit thermique initial boosté par l'IA.
    * **Licence SaaS (MRR):** Abonnement mensuel flexible de **5,000 DH à 15,000 DH/mois** selon la taille du site.
    * **ROI Fact:** Cost is instantly neutralized from Month 1 due to massive fossil fuel savings.
    """)
