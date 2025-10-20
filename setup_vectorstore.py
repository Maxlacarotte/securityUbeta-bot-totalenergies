from openai import OpenAI



vector_store = client.vector_stores.create(
    name="ubeta_security_docs"
)

print("Vector store créé :", vector_store.id)
