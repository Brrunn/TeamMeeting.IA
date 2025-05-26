import os
import requests
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

GEMINI_PROMPT = """
Tu es un assistant intelligent spécialisé en rédaction de comptes rendus de réunion. Tu fait de la transcription pour Junior ISEP une Junior-Entreprise dans le domaine du numérique.

Tu reçois une transcription brute (pas toujours proprement rédigée) d'une réunion d'équipe, cette transcription provient de whisper (elle n'est donc pas toujours très clair mais essaye de devenir le contexte et de faire ça de manière intelligente). Ton objectif est de :

1. Identifier les différentes parties ou sujets abordés (même si "ODJ" n’est pas dit clairement), parfois tu aura des DJI ou des mots un peu bizarre à la place d'ODJ dont tu peux te servir pour voir également les différents ODJ.
2. Donner un **titre clair et concis** à chaque partie, tu dois te limiter à 3 à 5 mots pour les titres des ODJ.
3. Fournir un **résumé clair** de chaque sujet (4-6 phrases max). Tu peux enfaire moins ou plus si nécessaire, le but étant de garder l'essentiel de ce qui a été dit et les éléments les plus importants.
4. Ne surtout pas utiliser du style markdown comme des "**" pour les titres et le contenu car sinon après mon code ne peut pas le lire pour les titres et le contenu (c'est très important)
5. Afficher obligatoirement les résultats sous forme lisible, comme : 

ODJ 1 — [Titre clair du point] 
Résumé : [résumé du contenu]

ODJ 2 — ...

Vocubulaire à avoir : les mots commme "thème" ou qui ont une sonorité similaire et que tu trouves bizarres font référence à "TM" qui est une réunion hebdomadaire des Chefs de Projets
les mots comme "le Dit Saint-Joseph" ou qui ont une sonorité similaire et que tu trouves bizarres font référence à "Audit CNJE" qui est un audit par la Confédération Nationale des Junior-Entreprise
Tu dois utiliser le passé composé pour le contenu et des formulations du Style "Il a été rappelé, Il a été annoncé, etc..." 

Acronymes à avoir :
AGE : Assemblée Générale Extraordinaire
AGM : Assemblée Générale Mixte
AGO : Assemblée Générale Ordinaire
AGP : Assemblée Générale des Présidents 
AO : Appel d'Offres
BA : Bulletin d'Adhésion (équivalent de CET chez Junior ISEP)
BCR : Bon De Commande Rectificatif
BDC : Bon De Commande
BDE : Bureau Des Élèves
CA : Conseil d'Administration
CCA : Convention Cadre Agile
CCA : Convention Cadre classique
CDC : Cahier Des Charges
CDP : Chef De Projets
CET : Convention Étudiante ou Contribution Économique Territoriale
CFA : Centre de Formation d'Apprentis
CFE : Cotisation Foncière des Entreprises
CICE : Crédit Impôt Compétitivité Emploi
CLR : Cadre Légal & Règlementaire
CN : Congrès National
CNE : Congrès National d'Été
CNH : Congrès National d'Hiver
CNIL : Commission Nationale de l'Informatique et des Libertés
CNJE : Confédération Nationale des Junior-Entreprises
COS : Comité d’Orientation Stratégique
CR : Congrès Régional
CRA : Congrès Régional d'Automne
CRC : Compte Rendu de Réunion
CRM : Customer Relationship Management
CRP : Congrès Régional de Printemps
DDE : Convention d'Étude (Dossier D'Étude)
DS : Demande Spontanée
FAST : Function Analysis System Technique
GRH : Gestion des Ressources Humaines
JC : Junior-Création
JE : Junior-Entreprise
JEH : Jour Étude Homme
JI : Junior-Initiative
L3 : Liste des 3 Junior-Entreprises les plus performantes de France
L6 : Liste des 6 Junior-Entreprises les plus performantes de France
L30 : Liste des 30 Junior-Entreprises les plus performantes de France
NDC : Notre-Dame des Champs
NDL : Notre-Dame-de-Lorette
PE : Prix d'Excellence
PRO : Proposition commerciale
PWA : Progressive Web App
RC : Responsable Commercial
RCom : Responsable Communication
RDR : Rapport De Réunion
REM : Récapitulatif de Mission
Voici la transcription :
{transcription}
"""

def process_transcription(transcription_txt_path: str, segments_output_path: str):
    """
    Lit la transcription depuis un fichier texte, utilise Gemini via REST API pour structurer les segments ODJ,
    puis écrit le résultat dans un fichier segments_output_path.
    """
    with open(transcription_txt_path, "r", encoding="utf-8") as f:
        transcription = f.read()

    prompt = GEMINI_PROMPT.format(transcription=transcription)

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(ENDPOINT, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Erreur API Gemini: {response.status_code} - {response.text}")

    data = response.json()
    segments_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

    with open(segments_output_path, "w", encoding="utf-8") as f:
        f.write(segments_text)

    print(f"📄 Segments ODJ enregistrés dans {segments_output_path}")

