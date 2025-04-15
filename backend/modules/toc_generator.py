import logging
from backend.modules import chunker
from backend.utils.pdf_utils import extract_title_from_text

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def extract_paper_title(paper):
    return paper.get('title') or extract_title_from_text(paper.get('content', '')) or "Untitled Paper"

def generate_toc(summaries, goal, markdown=False):
    if markdown:
        toc = f"## Table of Contents\n\n**Research Goal:** {goal}\n\n"
    else:
        toc = f"Table of Contents\n=======================\n\nResearch Goal: {goal}\n\n"

    for i, paper in enumerate(summaries, 1):
        paper_title = extract_paper_title(paper)
        toc += f"{i}. {paper_title}\n"

        chunks = paper.get('chunks', [])
        section_titles = []
        seen = set()

        for chunk in chunks:
            section_title = chunk.get('title', 'Untitled Section').strip().capitalize()
            if section_title not in seen:
                seen.add(section_title)
                section_titles.append(section_title)

        if section_titles:
            for section in section_titles:
                prefix = "    - " if not markdown else "    - "
                toc += f"{prefix}{section}\n"
        else:
            toc += "    - *No recognized sections*\n"

    toc += "\n--- End of Table of Contents ---\n"

    return toc

def inject_section_titles(summary_text, section_title, markdown=False):
    if markdown:
        return f"### {section_title}\n\n" + summary_text
    else:
        return f"{section_title}\n\n" + summary_text
