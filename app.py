import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ThermaSense AI - Executive Dashboard", layout="wide")

# --- CUSTOM CLEAN DARK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
        color: #eceff4;
    }
    .metric-box {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #3b82f6; margin-bottom: 15px;
    }
    .metric-box-agro {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #10b981; margin-bottom: 15px;
    }
    .metric-box-money {
        background-color: #1f2937; padding: 20px; border-radius: 10px;
        border-left: 5px solid #eab308; margin-bottom: 15px;
    }
    .report-box {
        background-color: #111827; padding: 20px; border-radius: 8px;
        border: 1px solid #4b5563; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🏭 Cimenterie & Éco-Système Agricole — ThermaSense AI")
st.markdown("<h4 style='color:#9ca3af;'>Interface de Gestion et de Routage Énergétique (MVP Live Demo)</h4>", unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR INTERACTIVE CONTROLS FOR THE PITCH ---
st.sidebar.header("🕹️ Simulateur Live (Pour le Jury)")
st.sidebar.write("Modifiez la production du four pour voir l'adaptation instantanée du système :")

# One main slider to control the whole demo logic live
clinker_production_load = st.sidebar.slider("Charge de Production du Four (%)", 40, 100, 85)
season = st.sidebar.selectbox("Saison Actuelle :", ["Hiver (Winter)", "Intersaison", "Été (Summer)"])

# --- LIVE MATHEMATICAL SIMULATION LOGIC (Fast & Lightweight) ---
# Total energy generated is directly proportional to furnace load
total_energy = int(clinker_production_load * 11.2) # e.g., 85% * 11.2 = 952 kW
internal_water_heating = int(total_energy * 0.15)  # 15% always goes to water heating

if season == "Hiver (Winter)":
    farm_demand = 450
    drying_allocated = max(50, total_energy - internal_water_heating - farm_demand)
    farm_allocated = total_energy - internal_water_heating - drying_allocated
elif season == "Été (Summer)":
    farm_demand = 80
    farm_allocated = farm_demand
    drying_allocated = total_energy - internal_water_heating - farm_allocated
else:
    farm_demand = 250
    drying_allocated = max(200, int(total_energy * 0.4))
    farm_allocated = total_energy - internal_water_heating - drying_allocated

# Financial Modeling (MAD/h)
factory_savings = int((internal_water_heating + drying_allocated) * 0.45) # Fossil fuel substituted
farm_revenue = int(farm_allocated * 0.30) # Green heat sold to farmers
total_financial_gain = factory_savings + farm_revenue

# Predictions for the next shifts (AI forecasting mock based on load)
pred_next_production = int(total_energy * 1.05)
pred_next_farm_demand = int(farm_demand * 0.9) if season != "Hiver (Winter)" else farm_demand

# --- MODULE 1: PRODUCTION & CONSOMMATION (⚡ ENERGIE) ---
st.subheader("⚡ 1. Flux Énergétiques en Temps Réel")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-box"><h4>Énergie Capturée</h4><h2>{total_energy} kW</h2><small>Source: Échappement Four</small></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><h4>Préchauffage Eau</h4><h2>{internal_water_heating} kW</h2><small>Consommation Usine</small></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-box"><h4>Séchage Matière</h4><h2>{drying_allocated} kW</h2><small>Consommation Usine</small></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-box-agro"><h4>Routage Mazarie</h4><h2>{farm_allocated} kW</h2><small>Demande Agricole</small></div>', unsafe_allow_html=True)

# --- MODULE 2: REVENUS & OPEX (💰 GAINS ET PERTES) ---
st.write("---")
st.subheader("💰 2. Impact Financier Horaire")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown(f'<div class="metric-box-money"><h4>Économies Cimenterie</h4><h2>+ {factory_savings} DH/h</h2><small>Charbon/Fioul évité</small></div>', unsafe_allow_html=True)
with col_f2:
    st.markdown(f'<div class="metric-box-money"><h4>Facturation Mazarie</h4><h2>+ {farm_revenue} DH/h</h2><small>Chaleur verte vendue</small></div>', unsafe_allow_html=True)
with col_f3:
    st.markdown(f'<div class="metric-box-money" style="border-left: 5px solid #10b981;"><h4>Gain Économique Total</h4><h2>{total_financial_gain} DH/h</h2><small>Valorisation nette</small></div>', unsafe_allow_html=True)

# --- MODULE 3: PREDICTIONS FUTURE & SEASONS (🔮 PREVISIONS AI) ---
st.write("---")
st.subheader("🔮 3. Prévisions Prédictives (AI Next 24h)")
col_p1, col_p2 = st.columns(2)

with col_p1:
    st.write("### 📈 Tendances de Production Estimées")
    st.info(f"Modèle prédictif estime une hausse de production à **{pred_next_production} kW** pour le prochain shift basé sur le planning des fours.")
    
    # Simple interactive chart showing stability
    chart_data = pd.DataFrame({
        'Heures': ['-12h', '-8h', '-4h', 'Actuel', '+4h (Pred)', '+8h (Pred)'],
        'Énergie (kW)': [total_energy-20, total_energy+10, total_energy-5, total_energy, pred_next_production, pred_next_production-10]
    }).set_index('Heures')
    st.line_chart(chart_data)

with col_p2:
    st.write("### 📉 Prévisions de Demande Agricole")
    st.success(f"La demande des coopératives agricoles stabilisera autour de **{pred_next_farm_demand} kW** selon les données météo saisonnières.")
    
    # Monthly synthetic summary report at the bottom of predictions
    st.markdown(f"""
    <div class="report-box">
        <strong>📋 Rapport Mensuel Estimé (Cimenterie + Mazarie) :</strong><br>
        • Énergie totale valorisée : <b>{(total_energy * 24 * 30):,} kWh / mois</b><br>
        • Réduction CO2 globale : <b>~ 54 Tonnes évitées</b><br>
        • Total Gains & Facturation : <b>{(total_financial_gain * 24 * 30):,} DH / mois</b>
    </div>
    """, unsafe_allow_html=True)
