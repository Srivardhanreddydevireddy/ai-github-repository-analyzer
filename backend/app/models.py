from typing import Any

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    repository_url: str = Field(..., description="Public GitHub repository URL")


class Finding(BaseModel):
    category: str
    severity: str
    title: str
    evidence: str
    recommendation: str


class AnalysisResponse(BaseModel):
    repository: dict[str, Any]
    languages: dict[str, int]
    structure: dict[str, Any]
    documentation: dict[str, Any]
    code_quality: dict[str, Any]
    scores: dict[str, float]
    findings: list[Finding]
    ai: dict[str, Any]
