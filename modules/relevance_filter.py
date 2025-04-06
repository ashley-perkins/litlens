from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def filter_relevant_papers(goal_embedding, paper_embeddings, threshold=0.4):
    try:
        print("Calculating similarities...")

        if not paper_embeddings:
            raise ValueError("No paper embeddings provided")

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

    except Exception as e:
        logging.error(f"🔥 Error in filter_relevant_papers: {e}")
        raise

