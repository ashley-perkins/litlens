# v0.3.7 - GPT-4 Token Limit Tuning & Resilient Chunking 

import re
import tiktoken
import logging
import os
from backend.config import ChunkerConfig
from openai import OpenAI  
from dotenv import load_dotenv

# Only show WARNINGS by default
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env file")
client = OpenAI(api_key=api_key)

# === CHUNKING ===
def chunk_text(text, max_tokens=None):
    if max_tokens is None:
        max_tokens = 3000  # 🔧 Lowered to allow room for prompt overhead (GPT-4 safe)

    pattern_str = '|'.join([re.escape(title) for title in ChunkerConfig.SECTION_TITLES])
    section_pattern = re.compile(rf'^((?:\d+\.\s+)?(?:{pattern_str}))', re.IGNORECASE | re.MULTILINE)

    splits = section_pattern.split(text)
    logging.info(f"Detected {len(splits)//2} sections after splitting")

    sections = []
    for i in range(1, len(splits), 2):
        title = splits[i].strip() if i < len(splits) and splits[i] else f"Section {i//2 + 1}"
        content = splits[i+1] if i+1 < len(splits) else ""
        sections.append({
            "id": i//2 + 1,
            "title": title,
            "content": content.strip()
        })

    enc = tiktoken.encoding_for_model("gpt-4")  # ✅ GPT-4 tokenization

    chunks = []
    current_chunk = ""
    current_tokens = 0
    current_title = ""

    for section in sections:
        section_title = section["title"]
        section_content = section["content"]
        section_text = f"{section_title}\n{section_content}"
        section_tokens = len(enc.encode(section_text))

        if section_tokens > max_tokens:
            paragraphs = section_content.split("\n\n")
            for para in paragraphs:
                para_text = f"{section_title}\n{para.strip()}"
                para_tokens = len(enc.encode(para_text))

                if para_tokens > max_tokens:
                    logging.warning(f"🚫 Skipping oversized paragraph (> {max_tokens} tokens)")
                    continue

                if current_tokens + para_tokens <= max_tokens:
                    current_chunk += "\n\n" + para_text
                    current_tokens += para_tokens
                else:
                    if current_chunk:
                        chunks.append({"title": current_title, "content": current_chunk.strip()})
                    current_chunk = para_text
                    current_title = section_title
                    current_tokens = para_tokens

            if current_chunk:
                chunks.append({"title": current_title, "content": current_chunk.strip()})
                current_chunk = ""
                current_tokens = 0
        else:
            if current_tokens + section_tokens <= max_tokens and section_title == current_title:
                current_chunk += "\n\n" + section_text
                current_tokens += section_tokens
            else:
                if current_chunk:
                    chunks.append({"title": current_title, "content": current_chunk.strip()})
                current_chunk = section_text
                current_title = section_title
                current_tokens = section_tokens

    if current_chunk:
        chunks.append({"title": current_title, "content": current_chunk.strip()})

    logging.info(f"✅ Total Chunks Created: {len(chunks)}")
    return chunks

# === EMBEDDING ===
def embed_text(text):
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    max_tokens = 8191
    tokens = enc.encode(text)

    if len(tokens) > max_tokens:
        logging.warning(f"⚠️ Trimming embedding input from {len(tokens)} to {max_tokens} tokens")
        text = enc.decode(tokens[:max_tokens])

    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def embed_papers(papers):
    print("🧠 Generating embeddings...")
    for paper in papers:
        embedding = embed_text(paper["content"])
        paper["embedding"] = embedding
    print("✅ Embeddings complete.")
    return papers

def embed_goal_and_papers(goal, papers):
    print("🧠 Embedding research goal...")
    goal_embedding = embed_text(goal)

    print("🧠 Embedding papers...")
    paper_embeddings = []
    for paper in papers:
        embedding = embed_text(paper["content"])
        paper_embeddings.append(embedding)

    print(f"✅ Embedded {len(paper_embeddings)} papers.")
    return goal_embedding, paper_embeddings