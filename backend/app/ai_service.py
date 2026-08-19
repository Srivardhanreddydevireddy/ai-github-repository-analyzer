import json
from typing import Any

import requests

from .config import get_settings


class AIService:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model

    def generate(self, repository: dict[str, Any], scores: dict[str, float], findings: list[dict[str, str]]) -> dict[str, Any]:
        if not self.api_key:
            return {
                "enabled": False,
                "message": "AI recommendations are disabled. Set OPENAI_API_KEY to enable the LLM layer.",
                "recommendations": [f["recommendation"] for f in findings[:5]],
            }

        prompt = {
            "repository": repository,
            "scores": scores,
            "findings": findings,
            "instructions": [
                "Summarize the repository using only the supplied evidence.",
                "Do not invent files, bugs, vulnerabilities, technologies, or metrics.",
                "Prioritize the most useful improvements.",
                "Return valid JSON with keys: summary, strengths, weaknesses, priority_actions.",
            ],
        }
        payload = {
            "model": self.model,
            "input": "You are a software-quality assistant. Analyze these structured findings:\n" + json.dumps(prompt, ensure_ascii=False),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post("https://api.openai.com/v1/responses", json=payload, headers=headers, timeout=45)
            response.raise_for_status()
            data = response.json()
            text = self._extract_text(data)
            parsed = self._parse_json(text)
            return {"enabled": True, "model": self.model, **parsed}
        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
            return {
                "enabled": True,
                "model": self.model,
                "error": f"AI service unavailable: {exc}",
                "recommendations": [f["recommendation"] for f in findings[:5]],
            }

    @staticmethod
    def _extract_text(data: dict[str, Any]) -> str:
        if isinstance(data.get("output_text"), str):
            return data["output_text"]
        chunks: list[str] = []
        for item in data.get("output", []):
            for content in item.get("content", []):
                if isinstance(content, dict) and isinstance(content.get("text"), str):
                    chunks.append(content["text"])
        return "\n".join(chunks)

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
        value = json.loads(cleaned)
        if not isinstance(value, dict):
            raise ValueError("AI response was not a JSON object")
        return value
