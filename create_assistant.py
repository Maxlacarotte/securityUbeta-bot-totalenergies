import os
from openai import OpenAI

# Utilise la même clé API que dans tes autres fichiers


# L'ID du vector store que tu as déjà créé
vector_store_id = "vs_68f64cb6fd4881919c6354cbb2db11c1"

assistant = client.beta.assistants.create(
  name="Assistant Sécurité Ubeta",
  instructions="Tu es un expert des documents de sécurité Ubeta. Réponds aux questions des utilisateurs en te basant exclusivement sur les informations contenues dans les fichiers fournis. Cite tes sources si possible.",
  model="gpt-4.1-mini",
  tools=[{"type": "file_search"}],
  tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
)

print(f"Assistant créé avec succès ! Copie cet ID dans ton fichier app.py :")
print(assistant.id)