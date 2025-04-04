from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken
from modules import chunker
from utils.pdf_utils import extract_title_from_text, extract_pdf_metadata

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env file")
client = OpenAI(api_key=api_key)

def summarize_papers(relevant_papers, goal):
    print("🟣 Starting summarization...\n")

    summaries = []

    for paper in relevant_papers:
        print(f"🔍 Summarizing: {paper.get('title', 'Untitled')} ({paper['filename']})")

        # ✅ Directly use metadata from extractor if available
        metadata = paper.get("metadata") or extract_pdf_metadata(paper.get('content', ''))
        paper_title = metadata.get("title") or extract_title_from_text(paper['content'])

        paper['title'] = paper_title
        paper['metadata'] = metadata

        print(f"Extracted title: {paper_title}")

        # ✅ Chunk and store chunks directly
        chunks = chunker.chunk_text(paper['content'])
        paper['chunks'] = chunks

        print(f"📄 Found {len(chunks)} sections")
        paper_summary = ""

        for i, chunk in enumerate(chunks):
            section_title = (chunk.get('title') or 'Untitled Section').strip()
            section_content = (chunk.get('content') or '').strip()

            if not section_content:
                print(f"⚠️ Skipping empty section: {section_title}")
                continue

            prompt = f"""
            You are an expert scientific writer assisting with a literature review.

            Research Goal: {goal}

            Paper Metadata (if available):
            - Title: {metadata.get("title", "N/A")}
            - Authors: {metadata.get("authors", "N/A")}
            - Journal: {metadata.get("journal", "N/A")}
            - Year: {metadata.get("year", "N/A")}

            Task: Summarize the following section of a research paper with the following rules:
            - Focus on how the content is relevant to the research goal.
            - Identify key findings, methods, or insights.
            - Write the summary as a clean, well-structured bullet-point list using "-" for each point.
            - Keep the summary concise but informative.
            - Avoid repeating minor details; emphasize the most important information.
            - At the end, add a [Reviewer Note] assessing whether this section meaningfully contributes to the research goal.
            - Style: Academic, formal, suitable for scientific literature reviews.
            - Output Format: Markdown.

            Section Title: {section_title}

            Section Content:
            {section_content}
            """

            print(f"✏️ Summarizing Section: {section_title} ({i+1}/{len(chunks)})")

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            chunk_summary = response.choices[0].message.content.strip()
            paper_summary += chunk_summary + "\n\n"

        summaries.append({
            "filename": paper['filename'],
            "title": paper_title,
            "summary": paper_summary.strip(),
            "chunks": chunks,
            "metadata": metadata,
            "goal": goal
        })

    print("\n✅ All papers summarized.\n")
    return summaries

def summarize_inline_text(content: str, goal: str) -> str:
    """Use summarization logic on a single text input instead of PDFs"""
    prompt = (
        f"You are an expert scientific writer assisting with a literature review.\n\n"
        f"Research Goal: {goal}\n\n"
        f"Content to Summarize:\n{content}\n\n"
        f"Task:\n- Summarize this content in 3–5 bullet points.\n"
        f"- Focus on findings relevant to the research goal.\n"
        f"- Keep tone academic, format clean (Markdown).\n"
        f"- End with a [Reviewer Note] assessing how well this content aligns with the research goal.\n"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # Or gpt-3.5 turbo if you want
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()