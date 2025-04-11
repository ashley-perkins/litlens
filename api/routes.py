from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from modules import summarizer, pdf_extractor, embedder, relevance_filter, report_generator
from utils import output_writer
from utils import hf_utils
from utils.pdf_utils import extract_pdf_metadata
import os
import tempfile
import logging
from typing import List, Dict, Any
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import Query
from utils.output_writer import sanitize_filename

# === Configure logger ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# === Inline Text Summarization ===
class SummarizeRequest(BaseModel):
    goal: str
    content: str

@router.post("/summarize")
def summarize_text(request: SummarizeRequest):
    try:
        logger.info("🔹 Inline summarization started")
        summary = summarizer.summarize_inline_text(request.content, request.goal)
        logger.info("✅ Inline summarization completed")
        return {
            "goal": request.goal,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"❌ Inline summarization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

# === Hugging Face Summarization ===
@router.post("/summarize-hf")
async def summarize_with_huggingface(request: SummarizeRequest):
    try:
        logger.info("🟡 Hugging Face summarization started...")
        summary = await hf_utils.summarize_text_with_hf_api(request.content)
        logger.info("✅ Hugging Face summarization completed")
        return {
            "goal": request.goal,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"❌ Hugging Face summarization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Hugging Face summarization failed: {str(e)}")

# ✅ Root route for Hugging Face App
@router.get("/", include_in_schema=False)
def root():
    logger.info("🌐 Root endpoint accessed")
    return JSONResponse(
        content={
            "message": "✅ LitLens backend is running.",
            "usage": "Use the /summarize-hf endpoint or visit /docs for API documentation.",
        }
    )

# === Full File Upload Summarization ===
@router.post("/summarize-pdfs")
async def summarize_uploaded_pdfs(
    files: List[UploadFile] = File(..., description="PDF files to summarize"),
    goal: str = Form("", description="Research goal to guide summarization")
):
    try:
        logger.info(f"📁 Starting LitLens pipeline on uploaded files with goal: {goal}")

        if not files:
            logger.warning("⚠️ No files received from request.")
            raise HTTPException(status_code=400, detail="No files uploaded.")

        extracted_papers = []
        for file in files:
            suffix = os.path.splitext(file.filename)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            paper = pdf_extractor.extract_text_from_pdf(tmp_path)
            extracted_papers.append(paper)
            os.remove(tmp_path)

        if not extracted_papers:
            logger.warning("⚠️ No valid PDFs extracted from uploads.")
            raise HTTPException(status_code=400, detail="No valid PDFs found.")

        logger.info("🔎 Embedding and filtering uploaded papers")
        goal_embedding, paper_embeddings = embedder.embed_goal_and_papers(goal, extracted_papers)
        relevant_indexes = relevance_filter.filter_relevant_papers(goal_embedding, paper_embeddings, threshold=0.4)
        relevant_papers = [extracted_papers[i] for i in relevant_indexes]

        if not relevant_papers:
            logger.warning("⚠️ No papers matched the research goal.")
            raise HTTPException(status_code=404, detail="No papers matched the research goal.")

        logger.info("📝 Summarizing relevant papers")
        summaries = summarizer.summarize_papers(relevant_papers, goal)

        output_path = output_writer.save_summary_to_file(summaries, goal)
        logger.info(f"✅ Report generated at {output_path}")

        return {
            "goal": goal,
            "summaries": summaries,
            "output_path": output_path
        }

    except Exception as e:
        logger.error(f"❌ Summarization pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=f"Summarization pipeline failed: {str(e)}")

# === Report Markdown Export ===
class ReportRequest(BaseModel):
    goal: str
    summaries: List[Dict[str, Any]]


@router.post("/report")
def generate_report(request: ReportRequest):
    try:
        logger.info("📄 Report generation endpoint hit.")
        report = report_generator.generate_markdown_report(request.summaries, request.goal)

        # Save to temp file
        safe_goal = sanitize_filename(request.goal)
        filename = f"{safe_goal}_summary_report.md"
        output_path = os.path.join(tempfile.gettempdir(), filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        logger.info("✅ Markdown report generated and saved.")
        return FileResponse(output_path, media_type="text/markdown", filename=filename)

    except Exception as e:
        logger.error(f"❌ Failed to generate markdown report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate markdown report: {str(e)}")

@router.get("/download")
async def download_file(path: str = Query(..., description="Path to the file on server")):
    try:
        return FileResponse(path, media_type="application/octet-stream", filename=os.path.basename(path))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {e}")