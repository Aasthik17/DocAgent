"""FastAPI application entry point for DocAgent."""
import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import AgentRequest, AgentResponse
from app.agent.core import DocAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("DocAgent.App")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Autonomous Document-Generating AI Agent API. Accepts natural language requests, plans and executes tasks, reflects on quality, and produces polished Microsoft Word (.docx) documents."
)

# CORS middleware for open frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint reporting system status."""
    return {
        "status": "online",
        "app": settings.app_name,
        "version": settings.version,
        "docs_generated_count": len(list(settings.docs_dir.glob("*.docx"))),
        "default_provider": settings.default_provider
    }

@app.post("/agent", response_model=AgentResponse, tags=["Agent"])
def execute_agent(request_data: AgentRequest):
    """
    Main Autonomous Agent Endpoint:
    Accepts JSON {"request": "..."} and optional model_provider override.
    Plans, resolves assumptions, executes tasks, reflects, and produces a .docx Word document.
    """
    try:
        agent = DocAgent(provider_override=request_data.model_provider)
        response = agent.run(request_data)
        return response
    except Exception as e:
        logger.error(f"Error during agent execution: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent execution failure: {str(e)}")

@app.get("/download/{doc_id}", tags=["Documents"])
def download_document(doc_id: str):
    """Streams the generated Microsoft Word (.docx) document by doc_id."""
    matches = list(settings.docs_dir.glob(f"*{doc_id}*.docx"))
    if not matches:
        raise HTTPException(status_code=404, detail=f"Document with ID '{doc_id}' not found.")
    
    file_path = matches[0]
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.get("/", response_class=HTMLResponse, tags=["UI"])
@app.get("/demo", response_class=HTMLResponse, tags=["UI"])
def serve_interactive_demo():
    """Serves the interactive web demo console."""
    index_path = settings.static_dir / "index.html"
    if not index_path.exists():
        return HTMLResponse("<h3>DocAgent UI file missing</h3>", status_code=500)
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
