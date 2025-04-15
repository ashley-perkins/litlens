---
title: LitLens
emoji: 📚
colorFrom: gray
colorTo: indigo
sdk: docker
app_file: backend/app.py
pinned: true
---

🧠📚 LitLens

A Lightweight AI-Powered Literature Review Assistant

“Designed to summarize, structure, and surface scientific insights with clarity and speed.”

📌 Overview

LitLens helps researchers, students, and reviewers transform PDFs into concise, structured summaries using AI. Built for speed and clarity, LitLens lets you:

Upload single or multiple scientific PDFs

Define a custom research goal (optional)

Generate clean summaries using Hugging Face LLMs

Download a full Markdown report

🚀 Live Deployment

LitLens is live and hosted on Hugging Face Spaces:
🔗 https://ashley-perkins-litlens.hf.space

Swagger UI for backend: https://ashley-perkins-litlens.hf.space/docs

✅ Current Status

✅ Summary generation via Hugging Face Transformers

✅ Multi-PDF support

✅ Downloadable Markdown report

✅ Hugging Face + FastAPI deployment

🔜 Citation organization + goal filtering

🔜 Token overflow & rate limit improvements

🔧 API Endpoints

POST /summarize-hf

Summarize a text passage with a given research goal using Hugging Face.

Sample Payload:

{
  "goal": "Identify appendix proteins",
  "content": "The presence of alpha-synuclein in the appendix..."
}

Sample Response:

{
  "goal": "Identify appendix proteins",
  "summary": "Alpha-synuclein in the appendix suggests a potential link to Parkinson’s."
}

GET /

Root endpoint. Confirms the backend is up.

🛠 Built With

FastAPI – Backend framework

Hugging Face Transformers – LLM for summarization

Docker – Containerized deployment

React – Frontend UI

📄 Local Setup

🔁 Clone the repo

git clone https://github.com/yourname/litlens.git
cd litlens

🧠 Backend

cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 7860

💻 Frontend

cd frontend
npm install
npm start

App available at localhost:3000
Backend API at localhost:7860

🧪 Example Request

{
  "goal": "Understand how gut microbiota impacts immune function",
  "content": "The gut microbiota plays a crucial role in modulating immune responses..."
}

🤝 Contributing

LitLens is in active development! Feedback, ideas, and PRs are welcome.

This is an early MVP with more features on the way.

📜 License

MIT License

Respect the original work. Forks welcome — but redistribution without significant modification or written permission is discouraged.