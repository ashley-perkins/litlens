from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def filter_relevant_papers(goal_embedding, paper_embeddings, threshold=0.4):
    print("Calculating similarities...")

    similarities = cosine_similarity(
        [goal_embedding],
        paper_embeddings
    )[0]

    relevant_papers = []

    for idx, score in enumerate(similarities):
        if score >= threshold:
            print(f"✅ Paper {idx} (Similarity: {score:.2f})")
            relevant_papers.append(idx)
        else:
            print(f"❌ Paper {idx} (Similarity: {score:.2f})")

    return relevant_papers

