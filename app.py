# -*- coding: utf-8 -*-
import sys
import os
# === FORCE UTF-8 AVANT TOUT ===
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# === PATCH HTTPX AVANT IMPORT ===
import httpx._models
_original_normalize = httpx._models._normalize_header_value

def _patched_normalize_header_value(value, encoding=None):
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode('utf-8')
    return str(value).encode('utf-8')

httpx._models._normalize_header_value = _patched_normalize_header_value

# === IMPORTS APRÈS LE PATCH ===
import streamlit as st
from openai import OpenAI

# === CONFIG ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
VECTOR_STORE_ID = "vs_68f64cb6fd4881919c6354cbb2db11c1"

# === CONFIGURATION DE LA PAGE ===
st.set_page_config(
    page_title="Assistant Sécurité - Projet Ubeta",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"  # OUVERT par défaut pour desktop
)

# === STYLES CSS PERSONNALISÉS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    * { font-family: 'Montserrat', sans-serif; }

    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

    /* Cacher le header sur desktop uniquement */
    @media (min-width: 769px) {
        header[data-testid="stHeader"] { display: none; }
    }

    /* Header visible et stylé sur mobile */
    @media (max-width: 768px) {
        header[data-testid="stHeader"] {
            background: linear-gradient(90deg, #0054A6 0%, #003d7a 100%);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        /* Icônes du header et chevrons toujours BLANCS (plusieurs sélecteurs pour robustesse) */
        header[data-testid="stHeader"] svg,
        header[data-testid="stHeader"] svg path,
        header [data-testid="baseButton-headerNoPadding"] svg,
        header [data-testid="baseButton-headerNoPadding"] svg path,
        header button[kind="header"] svg,
        header button[kind="header"] svg path,
        header button[title] svg,
        header button[title] svg path,
        [data-testid="stSidebar"] button svg,
        [data-testid="stSidebar"] button svg path,
        [data-testid="collapsedControl"] svg,
        [data-testid="collapsedControl"] svg path {
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }

        /* Supprimer la barre blanche arrondie (decoration/toolbar) qui dépasse */
        div[data-testid="stDecoration"],
        div[data-testid="stToolbar"] {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: 0 !important;
        }

        /* Remonter légèrement le contenu */
        .stAppViewContainer .main .block-container {
            padding-top: 0.5rem !important;
            margin-top: 0 !important;
        }

        /* Adoucir le premier bloc */
        .main-card { margin-top: 6px !important; box-shadow: 0 6px 24px rgba(0,0,0,0.08) !important; }
    }

    #MainMenu { display: none; }
    footer { display: none; }

    .block-container { padding-top: 1rem !important; }
    .main .block-container { padding-top: 1rem !important; max-width: 100%; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0054A6 0%, #003d7a 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }

    .main-card {
        background: white; border-radius: 20px; padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin: 10px auto; max-width: 900px;
    }
    .main-title {
        color: #0054A6; font-size: 2.8em; font-weight: 700; text-align: center;
        margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle { color: #666; font-size: 1.2em; text-align: center; margin-bottom: 30px; font-weight: 400; }

    .stTextInput input {
        border-radius: 12px !important; border: 2px solid #0054A6 !important; padding: 15px !important;
        font-size: 1.1em !important; transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #EE3124 !important; box-shadow: 0 0 0 3px rgba(238, 49, 36, 0.1) !important;
    }

    .stButton button {
        background: linear-gradient(90deg, #EE3124 0%, #c41f14 100%); color: white; border: none; border-radius: 12px;
        padding: 15px 40px; font-size: 1.1em; font-weight: 600; width: 100%; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(238, 49, 36, 0.3);
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(238, 49, 36, 0.4); }

    .stSuccess { background-color: #d4edda; border-left: 5px solid #28a745; border-radius: 8px; padding: 15px; margin-top: 20px; }
    .stError { background-color: #f8d7da; border-left: 5px solid #dc3545; border-radius: 8px; padding: 15px; margin-top: 20px; }

    .response-box {
        background: #f8f9fa; border-left: 5px solid #0054A6; border-radius: 10px; padding: 25px; margin-top: 20px;
        font-size: 1.05em; line-height: 1.7;
    }

    .logo-container { text-align: center; padding: 20px 0; margin-bottom: 30px; border-bottom: 2px solid rgba(255,255,255,0.2); }
    [data-testid="stSidebar"] img { display: block; margin-left: auto; margin-right: auto; }

    .info-box { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; margin: 20px 0; backdrop-filter: blur(10px); }
    .stSpinner > div { border-top-color: #EE3124 !important; }

    @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.8;} }
    .pulse-icon { animation: pulse 2s infinite; }
</style>
""", unsafe_allow_html=True)

# === JS: fermer auto la sidebar sur mobile, laisser ouverte sur desktop ===
st.markdown("""
<script>
(function() {
  const MOBILE_MAX = 768;
  const isMobile = window.innerWidth <= MOBILE_MAX;
  const flag = "sidebar_autocollapse_done";

  if (isMobile && !sessionStorage.getItem(flag)) {
    const tryCollapse = () => {
      const btn =
        document.querySelector('button[kind="header"]') ||
        document.querySelector('header [data-testid="baseButton-headerNoPadding"]') ||
        document.querySelector('header button[title]');
      if (btn) {
        btn.click();
        sessionStorage.setItem(flag, "1");
        return true;
      }
      return false;
    };

    if (!tryCollapse()) {
      const obs = new MutationObserver(() => { if (tryCollapse()) { obs.disconnect(); } });
      obs.observe(document.body, { childList: true, subtree: true });
      setTimeout(() => obs.disconnect(), 5000);
    }
  }
})();
</script>
""", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    try:
        st.image("assets/Logo_TotalEnergies.png", width=180)
    except:
        st.markdown("### 🔴 TotalEnergies")
    st.markdown("---")
    st.markdown("### 📍 Projet Ubeta")
    st.markdown("**Localisation :** Nigeria")
    st.markdown("""
    <div class="info-box">
        <h4 style='margin-top:0;'>🛡️ Assistant Sécurité</h4>
        <p style='font-size:0.9em; margin-bottom:0;'>
            Posez vos questions sur les procédures de sécurité, les protocoles d'urgence, 
            et les directives du projet Ubeta.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    ### 💡 Exemples de questions
    - Procédures d'évacuation d'urgence
    - Équipements de protection individuelle
    - Protocoles HSE du site
    - Consignes en cas d'incident
    - Formation sécurité obligatoire
    """)
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; font-size:0.85em; opacity:0.8; margin-top:30px;'>
        <p>🔒 Données confidentielles<br>Usage interne uniquement</p>
        <p style='margin-top:20px;'>© 2025 TotalEnergies</p>
    </div>
    """, unsafe_allow_html=True)

# === CONTENU PRINCIPAL ===
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown("""
<h1 class="main-title">
    <span class="pulse-icon">🛡️</span> Assistant Sécurité - Projet Ubeta
</h1>
<p class="subtitle">Obtenez des réponses instantanées sur les procédures de sécurité</p>
""", unsafe_allow_html=True)

q = st.text_input(
    "Votre question :",
    placeholder="Ex: Quelles sont les procédures d'évacuation en cas d'urgence ?",
    label_visibility="collapsed"
)

st.markdown("""
<p style='text-align: center; color: #666; font-size: 0.95em; margin-top: 15px; font-style: italic;'>
    📚 Basé sur la documentation "Ubeta Field Development Project Environmental Impact Assessment"
</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    send_button = st.button("🔍 Rechercher la réponse", use_container_width=True)

if send_button and q.strip():
    with st.spinner("🔄 Analyse des documents de sécurité en cours..."):
        try:
            resp = client.responses.create(
                model="gpt-4.1-mini",
                input=q,
                tools=[{"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]}],
            )
            st.markdown("---")
            st.success("✅ Réponse trouvée dans la base documentaire")
            st.markdown(f"""
            <div class="response-box">
                {resp.output_text}
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error("❌ Une erreur est survenue lors de la recherche")
            st.markdown(f"**Détails de l'erreur :** `{str(e)}`")
            with st.expander("🔧 Informations techniques (pour le support)"):
                import traceback
                st.code(traceback.format_exc())

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-top:50px; padding:20px; color:#666; font-size:0.9em;'>
    <p>⚠️ <strong>Important :</strong> Cet assistant fournit des informations basées sur la documentation officielle du projet Ubeta.</p>
    <p>En cas d'urgence réelle, suivez toujours les protocoles établis et contactez immédiatement les responsables HSE.</p>
</div>
""", unsafe_allow_html=True)
