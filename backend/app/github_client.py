import base64
import re
from typing import Any

import requests

from .config import get_settings


class GitHubClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.github_api_url
        self.max_files = settings.max_files
        self.max_file_bytes = settings.max_file_bytes
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": settings.github_api_version,
            "User-Agent": "ai-github-repository-analyzer",
        }
        if settings.github_token:
            self.headers["Authorization"] = f"Bearer {settings.github_token}"

    @staticmethod
    def parse_repository_url(url: str) -> tuple[str, str]:
        pattern = r"^https?://(?:www\.)?github\.com/([^/]+)/([^/#?]+?)(?:\.git)?/?$"
        match = re.match(pattern, url.strip())
        if not match:
            raise ValueError("Please provide a valid public GitHub repository URL.")
        return match.group(1), match.group(2)

    def _get(self, path: str) -> Any:
        response = requests.get(
            f"{self.base_url}{path}", headers=self.headers, timeout=20
        )
        if response.status_code == 404:
            raise ValueError("GitHub repository or requested resource was not found.")
        if response.status_code == 403:
            raise ValueError("GitHub rejected the request. Check permissions or API rate limits.")
        response.raise_for_status()
        return response.json()

    def analyze_repository(self, url: str) -> dict[str, Any]:
        owner, repo = self.parse_repository_url(url)
        repo_data = self._get(f"/repos/{owner}/{repo}")
        languages = self._get(f"/repos/{owner}/{repo}/languages")
        tree = self._get(
            f"/repos/{owner}/{repo}/git/trees/{repo_data['default_branch']}?recursive=1"
        )

        readme = ""
        try:
            readme_data = self._get(f"/repos/{owner}/{repo}/readme")
            if readme_data.get("content"):
                readme = base64.b64decode(readme_data["content"]).decode("utf-8", errors="replace")
        except (ValueError, requests.RequestException):
            readme = ""

        files = []
        for item in tree.get("tree", []):
            if item.get("type") != "blob":
                continue
            path = item.get("path", "")
            if self._should_skip(path):
                continue
            files.append(path)
            if len(files) >= self.max_files:
                break

        contents: dict[str, str] = {}
        for path in files:
            if not self._is_source_file(path):
                continue
            try:
                data = self._get(f"/repos/{owner}/{repo}/contents/{path}")
                if data.get("size", 0) > self.max_file_bytes:
                    continue
                encoded = data.get("content", "")
                if encoded:
                    contents[path] = base64.b64decode(encoded).decode("utf-8", errors="replace")
            except (ValueError, requests.RequestException, UnicodeDecodeError):
                continue

        return {
            "repository": {
                "name": repo_data.get("name"),
                "full_name": repo_data.get("full_name"),
                "owner": repo_data.get("owner", {}).get("login"),
                "description": repo_data.get("description"),
                "default_branch": repo_data.get("default_branch"),
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "open_issues": repo_data.get("open_issues_count", 0),
                "size_kb": repo_data.get("size", 0),
                "html_url": repo_data.get("html_url"),
            },
            "languages": languages,
            "tree": files,
            "readme": readme,
            "contents": contents,
        }

    @staticmethod
    def _should_skip(path: str) -> bool:
        parts = set(path.split("/"))
        excluded_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}
        excluded_ext = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".zip", ".exe", ".dll", ".pdf"}
        return bool(parts & excluded_dirs) or any(path.lower().endswith(ext) for ext in excluded_ext)

    @staticmethod
    def _is_source_file(path: str) -> bool:
        return path.lower().endswith((".py", ".js", ".ts", ".java", ".go", ".cpp", ".c", ".cs"))
