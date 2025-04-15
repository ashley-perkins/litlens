# config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not found in environment")

# Chunker Settings
class ChunkerConfig:
    MAX_TOKENS = 1000

    SECTION_TITLES = [
        "Abstract",
        "Introduction",
        "Background",
        "Methods",
        "Materials",
        "Results",
        "Discussion",
        "Conclusion",
        "References",
        "Summary",
        "Acknowledgments",
        "Study Design",
        "Patient Cohort",
        "Preliminary Results",
        "Future Work",
        "Limitations"
    ]