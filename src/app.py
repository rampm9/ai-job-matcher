from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional
import os
import time
from .engine import analyze_texts

# Initialize FastAPI app
app = FastAPI(
    title="JobMatch Checker", 
    version="1.0.0",
    description="AI-powered job matching with explainable results"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "http://localhost:3000"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ultra-simple in-memory rate limiter (per IP)
VISITS = {}
LIMIT = 30  # requests per 5 minutes
WINDOW = 300

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    ip = request.client.host
    now = time.time()
    VISITS.setdefault(ip, [])
    VISITS[ip] = [t for t in VISITS[ip] if now - t < WINDOW]
    if len(VISITS[ip]) >= LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
    VISITS[ip].append(now)
    return await call_next(request)

# Mount templates
templates = Jinja2Templates(directory="templates")

class AnalyzeRequest(BaseModel):
    jd_text: str
    cv_text: str

class AnalyzeFileRequest(BaseModel):
    jd_text: str
    cv_file_content: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
def analyze(req: AnalyzeRequest) -> Dict[str, Any]:
    """Analyze job description and CV text"""
    try:
        result = analyze_texts(req.jd_text, req.cv_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-file")
async def analyze_file(
    jd_text: str,
    cv_file: UploadFile = File(...)
) -> Dict[str, Any]:
    """Analyze job description with uploaded CV file"""
    try:
        # Read file content
        if cv_file.content_type not in ["text/plain", "application/pdf"]:
            raise HTTPException(
                status_code=400, 
                detail="Only text and PDF files are supported"
            )
        
        content = await cv_file.read()
        
        # For text files, decode directly
        if cv_file.content_type == "text/plain":
            cv_text = content.decode('utf-8')
        else:
            # For PDF files, you'd need a PDF parser like PyPDF2
            # For now, return an error
            raise HTTPException(
                status_code=400,
                detail="PDF parsing not implemented yet. Please use text files or paste content directly."
            )
        
        result = analyze_texts(jd_text, cv_text)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.get("/config")
def get_config():
    """Get application configuration"""
    return {
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "version": "1.0.0",
        "features": {
            "web_interface": True,
            "file_upload": True,
            "api_endpoints": True
        }
    }
