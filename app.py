# -*- coding: utf-8 -*-
import sys
import os

# === FORCE UTF-8 AVANT TOUT ===
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# === PATCH HTTPX AVANT IMPORT ===
import httpx._models

# Sauvegarder la fonction originale
_original_normalize = httpx._models._normalize_header_value

def _patched_normalize_header_value(value, encoding=None):
    """Force UTF-8 pour tous les headers HTTP"""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        # Force UTF-8 au lieu d'ASCII
        return value.encode('utf-8')
    return str(value).encode('utf-8')

# Appliquer le patch
httpx._models._normalize_header_value = _patched_normalize_header_value

# === IMPORTS APRÈS LE PATCH ===
import streamlit as st
from openai import OpenAI

# === CONFIG ===
# La clé API sera récupérée depuis les secrets de Streamlit Cloud
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
VECTOR_STORE_ID = "vs_68f64cb6fd4881919c6354cbb2db11c1"

# === INTERFACE STREAMLIT ===
st.set_page_config(page_title="Ubeta Security Q&A", layout="centered")
st.title("Ubeta — Questions sécurité")

q = st.text_input("Pose ta question :", placeholder="Ex: Quelles procédures d'évacuation ?")

if st.button("Envoyer") and q.strip():
    with st.spinner("Analyse des documents..."):
        try:
            resp = client.responses.create(
                model="gpt-4.1-mini",
                input=q,
                tools=[{"type": "file_search", "vector_store_ids": [VECTOR_STORE_ID]}],
            )
            st.success("✅ Réponse :")
            st.write(resp.output_text)
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
            import traceback
            st.code(traceback.format_exc())