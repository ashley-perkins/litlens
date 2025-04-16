# utils/embedder_hf.py

from transformers import AutoTokenizer, AutoModel
import torch
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Load HF embedding model (compatible with HF Spaces)
MODEL_NAME = "thenlper/gte-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def embed_text(text: str) -> list:
    try:
        logging.info("🌐 Generating HF embedding...")
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        return embedding
    except Exception as e:
        logging.error(f"❌ HF embedding failed: {e}")
        raise

def embed_papers(papers):
    for paper in papers:
        paper["embedding"] = embed_text(paper["content"])
    return papers

def embed_goal_and_papers(goal, papers):
    goal_embedding = embed_text(goal)
    paper_embeddings = [embed_text(p["content"]) for p in papers]
    return goal_embedding, paper_embeddings