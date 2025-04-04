# LitLens 🧠📚  
_A Lightweight AI-Powered Literature Review Assistant_

![LitLens Banner](https://user-images.githubusercontent.com/your-github-username/banner-placeholder.png)  
> “Designed to summarize, structure, and surface scientific insights with clarity and speed.”

---

## 🚀 What is LitLens?

**LitLens** is an AI-augmented literature review tool that extracts, filters, and summarizes research papers based on a defined research goal. Built with researchers, students, and program leads in mind, LitLens turns a folder of PDFs into a structured summary report — in either Markdown or plain text.

---

## 🧩 Core Features

- 📝 **Auto-Summarization by Section**: Breaks down papers by intro, methods, results, etc.
- 🎯 **Goal-Driven Relevance Filtering**: Only includes papers relevant to your research goal.
- 🧠 **Semantic Embedding Matching**: Uses OpenAI embeddings to understand content meaning.
- 🗂️ **Table of Contents & Metadata**: Extracts section titles, authors, journal, and year.
- 📦 **Markdown + TXT Export**: Ready-to-read reports for publication or knowledge capture.
- 🧪 **Modular Codebase**: Clean architecture for easy scaling or front-end integration.

---

## 📌 Roadmap
 Hugging Face backend for chunking + summarization

 Lovable (React) frontend for drag-and-drop + interactive review

 Research Timeline Generator

 In-browser chatbot mode

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

## ⚙️ How It Works

```bash
python litlens.py \
  --goal "My research goal here" \
  --input-dir "path_to_your_pdfs" \
  --threshold 0.4 \
  --output "output_directory" \
  --format md



