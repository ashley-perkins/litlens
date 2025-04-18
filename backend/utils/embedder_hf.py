# utils/embedder_hf.py
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer, models 
import logging
import os

try:
    import nltk
    nltk.data.path.append("/tmp/nltk_data")
    nltk.download("punkt", download_dir="/tmp/nltk_data")
except Exception as e:
    logging.error(f"❌ NLTK download failed: {e}")
    raise

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Load HF embedding model (fully compatible with Hugging Face Spaces)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Manually create the SentenceTransformer model
word_embedding_model = models.Transformer(MODEL_NAME)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

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