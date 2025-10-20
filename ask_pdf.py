from openai import OpenAI


vector_store_id = "vs_68f64cb6fd4881919c6354cbb2db11c1"

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Quelles sont les principales mesures de sécurité décrites dans le document Ubeta ?",
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }
    ],
)

print(response.output_text)