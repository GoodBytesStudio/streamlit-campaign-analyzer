import streamlit as st
import pandas as pd
import openai

# Configuration de l'interface
st.title("🔍 Analyse IA des Performances de Campagne")
st.write("Déposez vos fichiers CSV pour obtenir un rapport et des recommandations en temps réel.")

# Téléchargement des fichiers
uploaded_files = st.file_uploader("Ajoutez vos fichiers CSV (Emails, Inscriptions, Médias Sociaux)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    dataframes = {}
    for file in uploaded_files:
        df = pd.read_csv(file, encoding='latin1')
        dataframes[file.name] = df
        st.write(f"**{file.name}** chargé avec {df.shape[0]} lignes et {df.shape[1]} colonnes")

    # Fonction d'analyse de la campagne
    def analyze_campaign(dataframes):
        insights = []
        
        # Vérification des données et extraction des stats
        for name, df in dataframes.items():
            if 'Emails' in name:
                total_emails = df.shape[0]
                open_rate = df['Open Rate (%)'].mean() if 'Open Rate (%)' in df.columns else "N/A"
                insights.append(f"📩 {total_emails} emails envoyés avec un taux d'ouverture moyen de {open_rate}%")
            
            if 'Inscriptions' in name:
                total_inscriptions = df.shape[0]
                revenue = df['Montant de l'inscription'].sum() if 'Montant de l'inscription' in df.columns else "N/A"
                insights.append(f"🎟️ {total_inscriptions} inscriptions générant {revenue} CAD")
            
            if 'Médias Sociaux' in name:
                impressions = df['Impressions publicitaires'].sum() if 'Impressions publicitaires' in df.columns else "N/A"
                clicks = df['Nombre total de clics'].sum() if 'Nombre total de clics' in df.columns else "N/A"
                insights.append(f"📲 {impressions} impressions sur les réseaux sociaux et {clicks} clics")

        # Génération des recommandations avec OpenAI
        prompt = "\n".join(insights) + "\n\nQue pouvons-nous améliorer pour atteindre 200 ventes ?"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Tu es un expert en marketing digital et analyse de campagnes."},
                      {"role": "user", "content": prompt}]
        )
        return insights, response["choices"][0]["message"]["content"]
    
    insights, recommendations = analyze_campaign(dataframes)
    
    st.subheader("📊 Résumé des Performances")
    for insight in insights:
        st.write("✅", insight)
    
    st.subheader("🚀 Recommandations IA")
    st.write(recommendations)
