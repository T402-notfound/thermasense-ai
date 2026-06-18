import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ThermaSense AI - Multi-Grid Platform", layout="wide")

# --- CUSTOM DEEP DARK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
        color: #eceff4;
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
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL UNIT ---
st.sidebar.header("🕹️ Configuration Live Ingestion")
clinker_load = st.sidebar.slider("Charge du Four à Ciment (%)", 40, 100, 85)

# --- GLOBAL CALCULATION MATRIX ---
# Dynamic baseline generated from the slider
total_energy_recovered = int(clinker_load * 12.5) # Max 1250 kW
water_heating_internal = int(total_energy_recovered * 0.15)
drying_internal = int(total_energy_recovered * 0.45)
factory_total_internal = water_heating_internal + drying_internal

farms_allocated_energy = total_energy_recovered - factory_total_internal
losses_atmospheric = 0 if farms_allocated_energy >= 0 else abs(farms_allocated_energy)

# Financial rates (MAD per kWh)
traditional_energy_cost = 0.85 # Standard industrial Grid/Gas rate in Morocco
agro_discounted_rate = 0.35    # Attractive, cheap green rate for nearby farmers

factory_hourly_savings = int(factory_total_internal * traditional_energy_cost)
farms_hourly_revenue = int(farms_allocated_energy * agro_discounted_rate)

# --- SYSTEM TITLE ---
st.title("🏭 Plateforme ThermaSense AI — Éco-Système Global")
st.markdown("<h4>Routage Algorithmique & Optimisation Inter-Sectorielle (Cimenterie + Agro)</h4>", unsafe_allow_html=True)
st.write("---")

# --- NAVIGATION TABS SYSTEM (4 INTERFACES) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🏢 1. Optimisation Interne Usine", 
    "🚜 2. Consommation & Vente Mazarie", 
    "🗓️ 3. Variabilité Saisonnière (Hiver/Été)", 
    "📊 4. Rapport Annuel & Vision Predictive"
])

# ==========================================
# INTERFACE 1: CIMENTERIE (INTERNAL)
# ==========================================
with tab1:
    st.header("🏢 Consommation et Économies Internes de la Cimenterie")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><h4>Énergie Totale Capturée</h4><h2>{total_energy_recovered} kW</h2><small>Flux exergétique brut récupéré</small></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h4>Préchauffage Eau & Séchage</h4><h2>{factory_total_internal} kW</h2><small>Eau ({water_heating_internal} kW) | Séchage ({drying_internal} kW)</small></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card-money"><h4>OPEX Substitué Évité</h4><h2>+ {factory_savings} DH/h</h2><small>Économie d\'énergie fossile classique</small></div>', unsafe_allow_html=True)
    
    st.subheader("🔮 Prévisions d'Économies Internes Hebdomadaires (Next 7 Days)")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    pred_factory_savings = [factory_hourly_savings * 24 * np.random.uniform(0.9, 1.1) for _ in range(7)]
    df_factory = pd.DataFrame({'Jours': days, 'Économies Générées (DH)': pred_factory_savings}).set_index('Jours')
    st.bar_chart(df_factory)

# ==========================================
# INTERFACE 2: AGRO / MAZARIE (EXTERNAL)
# ==========================================
with tab2:
    st.header("🚜 Consommation du Secteur Agricole Local & Facturation")
    ca1, ca2, ca3 = st.columns(3)
    with ca1:
        st.markdown(f'<div class="metric-card-agro"><h4>Flux Routé vers les Mazarie</h4><h2>{farms_allocated_energy} kW</h2><small>Surplus thermique injecté en direct</small></div>', unsafe_allow_html=True)
    with ca2:
        st.markdown(f'<div class="metric-card-agro"><h4>Tarif Réduit Offert (Agro)</h4><h2>{agro_discounted_rate} DH / kWh</h2><small>Prix standard réseau : {traditional_energy_cost} DH/kWh (Offre Attractive)</small></div>', unsafe_allow_html=True)
    with ca3:
        st.markdown(f'<div class="metric-card-money"><h4>Revenus de Facturation</h4><h2>+ {farms_hourly_revenue} DH/h</h2><small>Gains secondaires pour la cimenterie</small></div>', unsafe_allow_html=True)
    
    st.subheader("⏰ Prévisions de Demande et Consommation Hebdomadaire par Profil Journalier")
    hours_profile = ['Matin (Morning)', 'Midi (Noon)', 'Soir (Evening)', 'Nuit (Night)']
    pred_agro_demand = [farms_allocated_energy * 0.8, farms_allocated_energy * 0.4, farms_allocated_energy * 1.2, farms_allocated_energy * 1.5]
    df_agro = pd.DataFrame({'Période de la Journée': hours_profile, 'Consommation Estimée (kW)': pred_agro_demand}).set_index('Période de la Journée')
    st.line_chart(df_agro)

# ==========================================
# INTERFACE 3: SEASONAL VARIABILITY
# ==========================================
with tab3:
    st.header("🗓️ Matrice Comparative de Consommation Selon les Saisons")
    st.write("Analyse macro-technique croisée de l'équilibre Offre/Demande (Usine + Mazarie)")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.subheader("❄️ Profil Type : Saison d'Hiver")
        st.markdown("""
        * **Demande Agricole (Serres) :** Maximale (Besoin de chauffage critique la nuit).
        * **Routage :** Priorité absolue donnée au réseau externe des coopératives.
        * **Gains de Facturation :** Très Élevés (+30% de revenus secondaires).
        * **Séchage Usine :** Réduit au minimum technique nominal.
        """)
        chart_winter = pd.DataFrame({'Flux': ['Eau Usine', 'Séchage Usine', 'Mazarie'], 'kW': [water_heating_internal, drying_internal * 0.5, farms_allocated_energy * 1.5]}).set_index('Flux')
        st.bar_chart(chart_winter, color="#3b82f6")

    with col_s2:
        st.subheader("☀️ Profil Type : Saison d'Été")
        st.markdown("""
        * **Demande Agricole (Serres) :** Minimale (Uniquement séchage de récoltes ponctuel).
        * **Routage :** Ré-aiguillage du surplus en interne vers les broyeurs de l'usine.
        * **Économies Usine :** Maximales (Zéro perte atmosphérique, optimisation OPEX interne).
        * **Gains de Facturation :** Modérés mais stables.
        """)
        chart_summer = pd.DataFrame({'Flux': ['Eau Usine', 'Séchage Usine', 'Mazarie'], 'kW': [water_heating_internal, drying_internal * 1.3, farms_allocated_energy * 0.2]}).set_index('Flux')
        st.bar_chart(chart_summer, color="#10b981")

# ==========================================
# INTERFACE 4: ANNUAL & PREDICTIVE VISION
# ==========================================
with tab4:
    st.header("📊 Bilan Énergétique Annuel & Rétrospective Prédictive (Y+1)")
    
    cy1, cy2, cy3 = st.columns(3)
    annual_savings = factory_hourly_savings * 24 * 365
    annual_revenue = farms_hourly_revenue * 24 * 365
    total_annual_impact = annual_savings + annual_revenue
    
    with cy1:
        st.markdown(f'<div class="metric-card-money" style="border-left:5px solid #eceff4;"><h4>Énergie Annuelle Valorisée</h4><h2>{(total_energy_recovered * 24 * 365):,} kWh</h2><small>Bilan consolidé Usine + Agro</small></div>', unsafe_allow_html=True)
    with cy2:
        st.markdown(f'<div class="metric-card-money"><h4>Gains Globaux (Annuel)</h4><h2>{total_annual_impact:,} DH / an</h2><small>Économies ({annual_savings:,} DH) | Ventes ({annual_revenue:,} DH)</small></div>', unsafe_allow_html=True)
    with cy3:
        st.markdown(f'<div class="metric-box-danger" style="background-color:#1f2937; padding:20px; border-radius:10px; border-left:5px solid #ef4444;"><h4>Émissions CO2 Évitées</h4><h2>~ 648 Tonnes / an</h2><small>Impact environnemental direct</small></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🔮 Vision Prédictive et Planification Stratégique pour l'Année Suivante (2027)")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.write("### 📈 Trajectoire de Rationalisation de la Consommation")
        st.info("🤖 **Analyse Prédictive de l'IA :** En optimisant les cycles de séchage de la matière première selon les prévisions de production de l'année prochaine, la cimenterie peut augmenter son taux d'auto-suffisance de **4.2%** supplémentaires, réduisant le recours aux énergies fossiles d'appoint.")
    with col_v2:
        st.markdown(f"""
        <div class="box-report">
            <h4>📋 Plan d'Action Stratégique (AI Insights)</h4>
            <hr style='border-color:#4b5563;'>
            • <b>Extension Réseau :</b> Intégrer 3 nouvelles coopératives agricoles au réseau de chaleur d'ici Q2.<br>
            • <b>Régulation Dynamique :</b> Automatisation complète des vannes d'aiguillage thermique via le jumeau numérique.<br>
            • <b>Target ROI :</b> Amortissement complet des infrastructures physiques de routage atteint en <b>14 mois</b>.
        </div>
        """, unsafe_allow_html=True)
