import os
from pdfminer.high_level import extract_text
from utils.pdf_utils import extract_pdf_metadata

def extract_papers(pdf_folder):
    papers = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            print(f"📄 Reading: {filename}")

            text = extract_text(filepath)
            text_length = len(text.strip())

            if text_length < 100:
                print(f"⚠️ Skipping {filename} (empty or too small)")
                continue

            papers.append({
                "filename": filename,
                "content": text
            })

    print(f"✅ Extracted {len(papers)} papers.\n")
    return papers
