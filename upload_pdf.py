from openai import OpenAI


vector_store_id = "vs_68f64cb6fd4881919c6354cbb2db11c1"  # ton ID

# Remplace le chemin ci-dessous par le chemin complet vers ton PDF
pdf_path = r"C:\Users\maxla\Desktop\SECURITY BOT TOTALENERGIE 2025\12 Ubeta_Security_Only.pdf"

file_stream = open(pdf_path, "rb")

client.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store_id,
    files=[file_stream],
)

print("PDF ajouté avec succès au vector store.")
