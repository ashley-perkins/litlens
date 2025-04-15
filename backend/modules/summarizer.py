from openai import OpenAI   
from dotenv import load_dotenv
import os
import tiktoken
import time
from backend.modules import chunker
from backend.utils.pdf_utils import extract_title_from_text, extract_pdf_metadata

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env file")
client = OpenAI(api_key=api_key)

def count_message_tokens(messages, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    tokens_per_message = 4  # every message structure adds overhead
    tokens = 0
    for msg in messages:
        tokens += tokens_per_message
        for key, value in msg.items():
            tokens += len(enc.encode(value))
    tokens += 2  # reply primer
    return tokens

def summarize_papers(relevant_papers, goal):
    print("🟣 Starting summarization...\n")
    summaries = []

    enc = tiktoken.encoding_for_model("gpt-4")
    MAX_TOKENS = 8192
    BUFFER_TOKENS = 500
    ALLOWED_TOKENS = MAX_TOKENS - BUFFER_TOKENS

    for paper in relevant_papers:
        print(f"🔍 Summarizing: {paper.get('title', 'Untitled')} ({paper['filename']})")

        metadata = paper.get("metadata") or extract_pdf_metadata(paper.get('content', ''))
        paper_title = metadata.get("title") or extract_title_from_text(paper['content'])
        paper['title'] = paper_title
        paper['metadata'] = metadata

        print(f"Extracted title: {paper_title}")

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

            prompt = (
                f"You are an expert scientific writer assisting with a literature review.\n\n"
                f"Research Goal: {goal}\n\n"
                f"Paper Metadata:\n"
                f"- Title: {metadata.get('title', 'N/A')}\n"
                f"- Authors: {metadata.get('authors', 'N/A')}\n"
                f"- Journal: {metadata.get('journal', 'N/A')}\n"
                f"- Year: {metadata.get('year', 'N/A')}\n\n"
                f"Task:\n"
                f"- Summarize the following section of a research paper.\n"
                f"- Focus on relevance to the research goal.\n"
                f"- Use clear, academic bullet points (Markdown format).\n"
                f"- End with a [Reviewer Note] evaluating the section’s usefulness.\n\n"
                f"Section Title: {section_title}\n"
                f"Section Content:\n{section_content}"
            )

            messages = [{"role": "user", "content": prompt}]
            token_count = count_message_tokens(messages)
            if token_count > ALLOWED_TOKENS:
                print(f"⚠️ Trimming section: {section_title} from {token_count} tokens")
                prompt_base = prompt.replace(section_content, '')
                allowed_section_tokens = ALLOWED_TOKENS - count_message_tokens([{"role": "user", "content": prompt_base}])
                section_trimmed = enc.decode(enc.encode(section_content)[:allowed_section_tokens])
                prompt = prompt.replace(section_content, section_trimmed)
                print(f"✂️ Trimmed section to {allowed_section_tokens} tokens")

            print(f"✏️ Summarizing Section: {section_title} ({i+1}/{len(chunks)})")

            success = False
            while not success:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    success = True
                except Exception as e:
                    if "rate_limit_exceeded" in str(e):
                        print("⏳ Rate limit hit. Waiting 2s before retry...")
                        time.sleep(2)
                    else:
                        raise e

            chunk_summary = response.choices[0].message.content.strip()
            paper_summary += chunk_summary + "\n\n"

            time.sleep(1.5)  # Delay to avoid spamming API

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
    prompt = (
        f"You are an expert scientific writer assisting with a literature review.\n\n"
        f"Research Goal: {goal}\n\n"
        f"Task:\n"
        f"- Summarize the content below in 3–5 bullet points.\n"
        f"- Keep tone academic, format Markdown.\n"
        f"- End with a [Reviewer Note] about how well this aligns with the goal.\n\n"
        f"Content:\n{content}"
    )

    enc = tiktoken.encoding_for_model("gpt-4")
    messages = [{"role": "user", "content": prompt}]
    if count_message_tokens(messages) > 7692:
        allowed = 7692 - count_message_tokens([{"role": "user", "content": prompt.replace(content, '')}])
        content_trimmed = enc.decode(enc.encode(content)[:allowed])
        prompt = prompt.replace(content, content_trimmed)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
