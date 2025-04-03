# v0.3.6.1 - Hotfix: Streamlined Tokenization + Logging

import re
import tiktoken
import logging

from config import ChunkerConfig

# Only show WARNINGS by default
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def chunk_text(text, max_tokens=None):
    if max_tokens is None:
        max_tokens = ChunkerConfig.MAX_TOKENS

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
            "title": title.strip(),
            "content": content.strip()
        })

    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

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
                    logging.warning(f"Paragraph too large (> {max_tokens} tokens), skipping")
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

    logging.info(f"Total Chunks Created: {len(chunks)}")

    return chunks
