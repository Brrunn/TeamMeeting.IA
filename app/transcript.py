def transcribe_audio(audio_file):
    import whisper
    import warnings
    import os
    import certifi

    os.environ['SSL_CERT_FILE'] = certifi.where()
    warnings.simplefilter("ignore")
    
    # Charger le modèle (tiny, base, small, medium, large)
    model = whisper.load_model("small")
    
    print("Transcription en cours...")
    result = model.transcribe(audio_file, language="fr")
    
    print("Transcription terminée.")
    return result["text"]


