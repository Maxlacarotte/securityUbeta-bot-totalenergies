from openai import OpenAI


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "Tu es un assistant qui répond brièvement."},
        {"role": "user", "content": "Bonjour, peux-tu me dire ce que fait TotalEnergies ?"}
    ]
)

print(response.choices[0].message.content)
