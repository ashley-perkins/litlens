---
title: LitLens
emoji: 🧠📚
colorFrom: indigo
colorTo: pink
sdk: docker
app_file: app.py
pinned: true
---

# LitLens 🧠📚  
_A Lightweight AI-Powered Literature Review Assistant_

![LitLens Banner](https://user-images.githubusercontent.com/your-github-username/banner-placeholder.png)  
> “Designed to summarize, structure, and surface scientific insights with clarity and speed.”

---

## 🚀 What is LitLens?

**LitLens** is an AI-augmented literature review tool that extracts, filters, and summarizes research papers based on a defined research goal. Built with researchers, students, and program leads in mind, LitLens turns a folder of PDFs into a structured summary report — in either Markdown or plain text.

It's like having a research assistant who never sleeps.

---

## 🧩 Core Features

- 📝 **Auto-Summarization by Section**: Breaks down papers by intro, methods, results, etc.
- 🎯 **Goal-Driven Relevance Filtering**: Only includes papers relevant to your research goal.
- 🧠 **Semantic Embedding Matching**: Uses OpenAI embeddings to understand content meaning.
- 🗂️ **Table of Contents & Metadata**: Extracts section titles, authors, journal, and year.
- 📦 **Markdown + TXT Export**: Ready-to-read reports for publication or knowledge capture.
- 🧪 **Modular Codebase**: Clean architecture for easy scaling or front-end integration.

---

## 🛣️ Roadmap (In Progress)

✅ Hugging Face backend for chunking + summarization

🧩 Lovable (React) frontend with drag-and-drop + interactive review

🗓️ Research Timeline Generator

🤖 In-browser chatbot mode for real-time querying

---

## 🧠 Built With
Python 3.10+

OpenAI API (gpt-3.5-turbo, embeddings)

pdfminer, tiktoken, scikit-learn, dotenv

---

## 👩‍🔬 Author
Ashley — Program Manager turned AI Builder
✨ GitHub: @ashley-perkins
✨ Co-led with: ChatGPT🧠

---

🛡️ License
This project is released under the MIT License, with the following additional terms:

🔒 Respect the original work.
This project was created as a public MVP by Ashley Perkins.
Forks are welcome, but direct replication, commercial use, or redistribution of the project or its name without significant modification and written permission is prohibited.
If you’re interested in building on LitLens or collaborating—reach out.

---

## ⚙️ How It Works

```bash
python litlens.py \
  --goal "My research goal here" \
  --input-dir "path_to_your_pdfs" \
  --threshold 0.4 \
  --output "output_directory" \
  --format md
<<<<<<< HEAD



=======
🧪 Summarize a Folder of Scientific PDFs
LitLens can now process a full folder of scientific papers, filter them based on a research goal, summarize the relevant ones using GPT-4, and export a beautifully formatted markdown report.

🔁 Endpoint
http
Copy
Edit
POST /summarize-pdfs
🔧 Request Body
json
Copy
Edit
{
  "goal": "identify biomarkers for appendiceal neoplasms",
  "folder_path": "test_pdfs"
}
goal: Your specific research goal.

folder_path: Relative or absolute path to the folder containing your PDFs.

✅ Output
A markdown report will be saved to the output/ directory.

Filename format:

Copy
Edit
{safe_goal}_summary_report.md
Example:

bash
Copy
Edit
output/identify_biomarkers_for_appendiceal_neoplasms_summary_report.md
📦 Example Report Format
markdown
Copy
Edit
# LitLens Summary Report

## Research Goal
identify biomarkers for appendiceal neoplasms

## Table of Contents
1. [Paper Title](#paper-1)
   - Year: 2022 | Journal: Nature | Authors: Smith et al.
   - Abstract
   - Methods
   - Results
2. [Another Paper](#paper-2)
   - Year: 2021
   - Discussion
   - Conclusion

--- End of Table of Contents ---

## Paper 1: Paper Title  
*Year: 2022 | Journal: Nature | Authors: Smith et al.*

- Key findings in bullet points  
- Relevance to goal  
- [Reviewer Note]: This paper strongly supports the research goal by identifying key biomarkers in...

## Paper 2: Another Paper  
*Year: 2021*

- Summary of unrelated findings  
- [Reviewer Note]: This paper is not directly relevant to the goal but provides useful context.

✨ LitLens v0.3: Added summarization pipeline, markdown export, and output routing
