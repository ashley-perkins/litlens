# embedder.py
from sentence_transformers import SentenceTransformer

# Load model globally (so we don't reload it every time)
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, general-purpose embedding model

def embed_goal_and_papers(goal, papers):
    print("Embedding research goal...")
    goal_embedding = model.encode(goal)
    
    print("Embedding papers...")
    paper_embeddings = []

    # Only store the embeddings (no extra dict structure)
    for paper in papers:
        embedding = model.encode(paper['content'])
        paper_embeddings.append(embedding)

    print(f"Embedded {len(paper_embeddings)} papers.")

    return goal_embedding, paper_embeddings
