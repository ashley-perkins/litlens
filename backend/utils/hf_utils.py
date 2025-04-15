import httpx
import os

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not API_TOKEN:
    raise EnvironmentError("HUGGINGFACE_API_TOKEN not found in environment variables.")

async def summarize_text_with_hf_api(text: str, model_name: str = "facebook/bart-large-cnn"):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": text}
    url = f"https://api-inference.huggingface.co/models/{model_name}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result[0]["summary_text"]

