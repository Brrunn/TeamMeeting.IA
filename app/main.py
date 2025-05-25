import os
from datetime import datetime
from app.record import record_audio
from app.transcript import transcribe_audio
from app.text_processing import process_transcription
from app.doc_creation import generate_doc_from_segments

def ensure_dirs():
    for folder in ["data/audio", "data/transcripts", "data/segments", "data/outputs", "data/templates"]:
        os.makedirs(folder, exist_ok=True)

def main():
    ensure_dirs()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    audio_path = f"data/audio/reunion_{timestamp}.wav"
    transcript_path = f"data/transcripts/transcription_{timestamp}.txt"
    segments_path = f"data/segments/segments_{timestamp}.txt"
    template_path = "data/templates/CRC-TemplateIA.docx"
    output_path = f"data/outputs/compte_rendu_{timestamp}.docx"

    # Étape 1 : Enregistrement audio - Pas utilisé dans cette version mais à utiliser plus tard
    record_audio(filename=audio_path, duration=None)  # ou None pour manuel

    # Étape 2 : Transcription audio
    text = transcribe_audio(audio_file=audio_path)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Étape 3 : Découpage en ODJ
    process_transcription(transcript_path, segments_path)

    # Étape 4 : Génération du document Word
    generate_doc_from_segments(segments_path, template_path, output_path)

    print(f"\n Rapport final prêt : {output_path}")

if __name__ == "__main__":
    main()
