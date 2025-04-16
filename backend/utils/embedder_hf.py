# utils/embedder_hf.py

from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Load HF embedding model (fully compatible with Hugging Face Spaces)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str):
    try:
        logging.info("🔵 Generating HF embedding...")
        embedding = model.encode(text, convert_to_numpy=True).tolist()
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