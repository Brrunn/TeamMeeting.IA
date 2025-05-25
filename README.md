

## Structure : 
📁 app/
├── doc_creation.py # Génère le compte rendu Word via Gemini
├── main.py # Script principal (exécution locale)
├── record.py # Enregistre l’audio depuis le micro (non utilisé pour le moment car on drag and drop des fichiers .wav pour le moment, mais faites vous plaisir si vous voulez l'activer)
├── streamlit_app.py # Interface utilisateur
├── text_processing.py # Nettoie et segmente le texte transcrit
├── transcript.py # Transcrit le fichier audio avec Whisper
📁 data/
├── CRC-TemplateIA.docx # Template Word utilisé pour générer les CR
├── .wav # Fichiers audio source
├── transcription.txt # Résultat brut de la transcription
├── compte_rendu_.docx # Compte rendu final généré

### 1. Cloner le dépôt

git clone https://github.com/brrunn/TeamMeeting.IA.git
cd TeamMeeting.IA

### 2. Créer un environnement virtuel

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

### 3. Installer les dépendances

pip install -r requirements.txt

### 4. Lancer l’application

streamlit run app/streamlit_app.py


## Utilisation avec Docker

### 1. Construire l’image

docker build -t compte-rendu-app .

### 2. Lancer le conteneur

docker run -p 8501:8501 compte-rendu-app

=> L'interface est disponible sur http://localhost:8501


-------

## Stack utilisée 

Python 3.11

Streamlit

OpenAI Whisper

Google Gemini API

python-docx

Docker

--------

Projet développé dans le cadre de Junior ISEP
