from transformers import pipeline
import os

# Load the Hugging Face summarization pipeline
# You can swap the model later if needed
def load_summarizer(model_name="facebook/bart-large-cnn"):
    print("🧠 Loading Hugging Face summarization model...")
    return pipeline("summarization", model=model_name, from_tf=True)

# Run a summarization task
def summarize_text(text, model=None, max_tokens=512):
    if model is None:
        model = load_summarizer()

    if len(text.strip()) == 0:
        return "[No content provided.]"

    # Hugging Face pipeline handles token truncation internally
    result = model(text, max_length=max_tokens, min_length=50, do_sample=False)
    return result[0]["summary_text"].strip()