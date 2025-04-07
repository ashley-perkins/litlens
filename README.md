---
title: LitLens
emoji: 🧠📚
colorFrom: indigo
colorTo: pink
sdk: docker
app_file: app.py
pinned: true
---

# 🧠📚 LitLens

_A Lightweight AI-Powered Literature Review Assistant_

> “Designed to summarize, structure, and surface scientific insights with clarity and speed.”

![LitLens Banner](https://user-images.githubusercontent.com/your-github-username/banner-placeholder.png)

---

## ✅ Current Status

LitLens backend is **running on Hugging Face** using **FastAPI** and Docker.

You can test the API using Swagger UI at:

/docs

Or use the deployed summarization endpoint:

/summarize-hf

---

## 🔧 Available Endpoints

`POST /summarize-hf`

Summarizes a short paragraph of text using a Hugging Face transformer model.

#### Payload:

```json
{
  "goal": "Identify appendix proteins",
  "content": "The presence of alpha-synuclein in the appendix..."
}

Returns:

{
  "goal": "Identify appendix proteins",
  "summary": "Alpha-synuclein in the appendix suggests a potential link to Parkinson’s."
}

GET /
Root route — sanity check for uptime.
Returns a confirmation message that the backend is live.

🧪 Upcoming Features
Feature	Status
Summarize full folders of PDFs	🔜 In development
Embed + filter findings by goal	🔜 In development
Generate downloadable .md reports	🔜 In development
Handle API key + token overflow	✅ Local complete

🛠️ Built With
FastAPI – for blazing-fast backend API

Hugging Face Transformers – for abstractive summarization

Docker – for deployment to Hugging Face Spaces

🤝 Contributing
This is a WIP MVP. Feature requests and feedback welcome —
LitLens is being actively developed and expanded!

📄 License
MIT License


---

## 🔍 API Documentation

The LitLens API is live and documented with Swagger UI.

👉 **Explore the API here**:  
https://ashley-perkins-litlens.hf.space/docs](https://ashley-perkins-litlens.hf.space/docs)

You can test all three endpoints directly in the browser:

| Endpoint           | Method | Description                                 |
|--------------------|--------|---------------------------------------------|
| `/summarize`       | POST   | Summarize a block of inline text.           |
| `/summarize-hf`    | POST   | Use Hugging Face model to summarize text.   |
| `/summarize-pdfs`  | POST   | Summarize PDFs uploaded to `test_pdfs/`.    |

---

### 🧪 Example Request (via `/summarize-hf`)

```json
POST /summarize-hf
{
  "goal": "Understand how gut microbiota impacts immune function",
  "content": "The gut microbiota plays a crucial role in modulating immune responses.."
}

📄 Want to Run It Locally?
Clone the repo

Add your OPENAI_API_KEY to .env

Run locally with uvicorn app:app --reload --port 7860

Then access: http://127.0.0.1:7860/docs