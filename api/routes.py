from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modules import summarizer, pdf_extractor, embedder, relevance_filter, report_generator
from utils import output_writer
from utils import hf_utils
from utils.pdf_utils import extract_pdf_metadata
import os
from fastapi.responses import JSONResponse
import logging

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

# === Full Folder Summarization ===
class PDFSummarizationRequest(BaseModel):
    goal: str
    folder_path: str

@router.post("/summarize-pdfs")
def summarize_pdfs(request: PDFSummarizationRequest):
    try:
        logger.info(f"📁 Starting full summarization pipeline for folder: {request.folder_path}")

        if not os.path.exists(request.folder_path):
            logger.warning("⚠️ Input directory not found.")
            raise HTTPException(status_code=404, detail="Input directory not found.")

        # 1. Extract PDFs
        papers = pdf_extractor.extract_text_from_folder(request.folder_path)
        if not papers:
            logger.warning("⚠️ No valid PDFs found in directory.")
            raise HTTPException(status_code=400, detail="No valid PDFs found.")

        # 2. Embed & Filter
        logger.info("🔎 Embedding and filtering papers for relevance")
        goal_embedding, paper_embeddings = embedder.embed_goal_and_papers(request.goal, papers)
        relevant_indexes = relevance_filter.filter_relevant_papers(goal_embedding, paper_embeddings, threshold=0.4)
        relevant_papers = [papers[i] for i in relevant_indexes]

        if not relevant_papers:
            logger.warning("⚠️ No papers matched the research goal.")
            raise HTTPException(status_code=404, detail="No papers matched the research goal.")

        # 3. Summarize
        logger.info("📝 Summarizing relevant papers")
        summaries = summarizer.summarize_papers(relevant_papers, request.goal)

        # 4 & 5. Export Summary to Output File (let it handle formatting)
        output_path = output_writer.save_summary_to_file(summaries, request.goal)
        logger.info(f"✅ Report generated at {output_path}")

        return {
            "goal": request.goal,
            "summaries": summaries,
            "output_path": output_path
        }

    except Exception as e:
        logger.error(f"❌ Summarization pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=f"Summarization pipeline failed: {str(e)}")