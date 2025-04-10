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

**A Lightweight AI-Powered Literature Review Assistant**

---

## 🎯 Description

> “Designed to summarize, structure, and surface scientific insights with clarity and speed.”

---

![LitLens Banner](coming soon)

---

## ✅ Current Status

The **LitLens backend is live on Hugging Face**, powered by **FastAPI** and **Docker**.

You can interact with it via Swagger UI:
[https://ashley-perkins-litlens.hf.space/docs](https://ashley-perkins-litlens.hf.space/docs)

---

## 🔧 Available Endpoints

### `POST /summarize-hf`

Summarizes a short paragraph of text using a Hugging Face transformer model.

---

#### ✅ Sample Payload:

```json
{
  "goal": "Identify appendix proteins",
  "content": "The presence of alpha-synuclein in the appendix..."
}

✅ Sample Response:
{
  "goal": "Identify appendix proteins",
  "summary": "Alpha-synuclein in the appendix suggests a potential link to Parkinson’s."
}

GET /
Root route – simple uptime check.

Returns a confirmation message that the backend is live.

🔬 Upcoming Features
Feature

Status

Summarize full folders of PDFs

🔜 In development

Embed + filter findings by goal

🔜 In development

Generate downloadable .md reports

🔜 In development

Handle token overflow + rate limit

✅ Completed locally

🛠️ Built With
FastAPI – blazing-fast API framework

Hugging Face Transformers – for abstractive summarization

Docker – deployment to Hugging Face Spaces

🧪 Example Request (via /summarize-hf)
POST /summarize-hf
```json
{
  "goal": "Understand how gut microbiota impacts immune function",
  "content": "The gut microbiota plays a crucial role in modulating immune responses..."
}

📄 Want to Run It Locally?
Clone this repo

Add your OpenAI and/or Hugging Face API keys to .env

Run locally:

uvicorn app:app --reload --port 7860

Then open:

http://127.0.0.1:7860/docs

🤝 Contributing
This is a WIP MVP! Feedback, suggestions, and PRs are welcome.

LitLens is being actively developed and expanded — your ideas are valued.


---

📜 License
MIT License


Respect the original work. Forks are welcome, but commercial use or redistribution without significant modification and written permission is prohibited.