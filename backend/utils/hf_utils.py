import httpx
import os
import logging

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not API_TOKEN:
    raise EnvironmentError("HUGGINGFACE_API_TOKEN not found in environment variables.")

async def summarize_text_with_hf_api(text: str, model_name: str = "philschmid/bart-large-cnn-samsum"):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": text}
    url = f"https://api-inference.huggingface.co/models/{model_name}"

    async with httpx.AsyncClient() as client:
        logging.debug(f"sending to HF model '{model_name}': {text[:300]}")
        response = await client.post(url, headers=headers, json=payload)

        try:
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list) and result and "summary_text" in result[0]:
                return result[0]["summary_text"]
            else:
                raise ValueError(f"Unexpected response format: {result}")
        except Exception as e:
            logging.error(f"❌ HuggingFace API error: {e}")
            logging.debug(f"📦 Full HF response: {response.text}")
            raise

