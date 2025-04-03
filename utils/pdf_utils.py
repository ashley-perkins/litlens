import re

# --- Lightweight PDF Utilities ---
# Moved into proper utils/ folder in Step 4.2


def extract_title_from_text(text):
    """
    Naive PDF title extractor.
    Looks for the first line or first <300 chars likely to be a title.
    """
    lines = text.strip().split('\n')
    for line in lines:
        clean_line = line.strip()
        if 10 < len(clean_line) < 200 and re.search(r'[A-Za-z]', clean_line):
            # Avoid pure numeric headers like "1. Introduction"
            if not re.match(r'^\d+\.\s', clean_line):
                return clean_line
    return "Untitled Paper"


def extract_section_titles(text):
    """
    Extracts candidate section titles from the PDF text for TOC generation.

    Returns a list of tuples: (section number, section title)
    """
    section_titles = []

    # Look for common section patterns with numbering
    section_pattern = re.compile(r'^(\d+)\.\s+(Abstract|Introduction|Methods|Materials|Results|Discussion|Conclusion|References|Acknowledgments)', re.IGNORECASE | re.MULTILINE)

    for match in section_pattern.finditer(text):
        section_num = match.group(1).strip()
        section_title = match.group(2).strip()
        section_titles.append((section_num, section_title))

    return section_titles


def extract_pdf_metadata(text):
    """
    Extracts basic metadata like publication year, authors, and journal if detectable.
    """
    metadata = {}

    # Detect year
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    if year_match:
        metadata['year'] = year_match.group(0)

    # Detect journal
    journal_match = re.search(r'(Journal|Proceedings|Conference)[^\n]{0,100}', text, re.IGNORECASE)
    if journal_match:
        metadata['journal'] = journal_match.group(0).strip()

    # Placeholder for authors (to be improved later)
    author_match = re.search(r'(?i)by\s+([A-Za-z,\s]+)', text[:1000])
    if author_match:
        metadata['authors'] = author_match.group(1).strip()

    return metadata
