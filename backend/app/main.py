from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .ai_service import AIService
from .analyzers import analyze_python_sources, analyze_readme, analyze_structure
from .github_client import GitHubClient
from .models import AnalysisResponse, AnalyzeRequest, Finding
from .scoring import build_findings, calculate_scores

app = FastAPI(
    title="AI-Based GitHub Repository Analyzer",
    description="Analyze a GitHub repository using deterministic code-quality checks and AI-assisted recommendations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    frontend = Path(__file__).resolve().parents[2] / "frontend" / "index.html"
    if frontend.exists():
        return FileResponse(frontend)
    return {"message": "AI-Based GitHub Repository Analyzer is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalyzeRequest) -> AnalysisResponse:
    try:
        data = GitHubClient().analyze_repository(request.repository_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Repository collection failed: {exc}") from exc

    structure = analyze_structure(data["tree"])
    documentation = analyze_readme(data["readme"])
    code_quality = analyze_python_sources(data["contents"])
    scores = calculate_scores(structure, documentation, code_quality)
    findings = build_findings(structure, documentation, code_quality)
    ai = AIService().generate(data["repository"], scores, findings)

    return AnalysisResponse(
        repository=data["repository"],
        languages=data["languages"],
        structure=structure,
        documentation=documentation,
        code_quality=code_quality,
        scores=scores,
        findings=[Finding(**item) for item in findings],
        ai=ai,
    )
