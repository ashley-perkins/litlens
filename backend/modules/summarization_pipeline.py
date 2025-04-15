import os
from backend.modules import pdf_extractor, embedder, relevance_filter, summarizer
from backend.utils.pdf_utils import extract_text_from_pdf
from dotenv import load_dotenv
from backend.utils.output_writer import save_summary_to_file

# Ensure .env is loaded (needed for OpenAI API key)
load_dotenv()

def summarize_from_pdfs(folder_path, goal, threshold=0.4):
    try:
        papers = []

        # Step 1: Extract PDF text
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                full_path = os.path.join(folder_path, filename)
                text = extract_text_from_pdf(full_path)
                papers.append({"filename": filename, "content": text})

        # Step 2: Embed papers
        embedded = embedder.embed_papers(papers)

        # Step 3: Filter by relevance
        relevant = relevance_filter.filter_relevant_papers(embedded, goal, threshold=threshold)

        # Step 4: Summarize
        # Step 4: Summarize
        summaries = summarizer.summarize_papers(relevant, goal)

        # Step 5: Save output
        print ("writing summary to file:", summaries[0])
        save_summary_to_file(summary_data=summaries[0], filename="summary.txt")

        return summaries
    except Exception as e:
        raise RuntimeError(f"Summarization pipeline failed: {str(e)}")