import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import os
from app.record import record_audio  # si besoin dans le futur
from app.transcript import transcribe_audio
from app.text_processing import process_transcription
from app.doc_creation import generate_docx_from_segments

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
TEMPLATE_FILE = os.path.join(DATA_DIR, "CRC-TemplateIA.docx")
OUTPUT_FILE = os.path.join(DATA_DIR, "compte_rendu_filled_gemini.docx")
TRANSCRIPTION_TXT = os.path.join(DATA_DIR, "transcription.txt")
ODJ_SEGMENTS_TXT = "data/transcription_odj_segments.txt"

st.title("📝 Générateur de compte-rendu de réunion")

uploaded_file = st.file_uploader("📤 Upload un fichier audio (.mp3 ou .wav)", type=["mp3", "wav"])

if uploaded_file:
    file_path = os.path.join(DATA_DIR, uploaded_file.name)
    print("uploaded_file:", uploaded_file)
    print("file_path:", file_path)
    print("os.path.exists(file_path):", os.path.exists(file_path))
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Fichier enregistré : {file_path}")

    if st.button("🚀 Générer le compte-rendu"):
        with st.spinner("⏳ Transcription en cours..."):
            transcription = transcribe_audio(file_path)
            with open(TRANSCRIPTION_TXT, "w", encoding="utf-8") as f:
                f.write(transcription)

        with st.spinner("✂️ Découpage en ODJ..."):
            segments = process_transcription(TRANSCRIPTION_TXT, ODJ_SEGMENTS_TXT)

        with st.spinner("🧠 Résumé avec Gemini..."):
            generate_docx_from_segments(ODJ_SEGMENTS_TXT, TEMPLATE_FILE, OUTPUT_FILE)

        st.success("✅ Compte-rendu généré !")

        with open(OUTPUT_FILE, "rb") as f:
            st.download_button(
                label="📥 Télécharger le compte rendu Word",
                data=f,
                file_name="compte_rendu_reunion.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
