# AI-Based GitHub Repository Analyzer

An AI-assisted developer tool that collects GitHub repository data, performs deterministic static analysis, calculates explainable quality metrics, and generates practical improvement recommendations.

## Status

✅ **Working MVP architecture implemented**

The repository contains the backend analysis pipeline, GitHub API integration, Python static-analysis engine, scoring system, optional AI layer, dashboard, tests, Docker configuration, and CI workflow.

## What It Does

Enter a public GitHub repository URL and the system:

1. Validates the repository URL.
2. Retrieves repository metadata, languages, README content and repository tree through the GitHub REST API.
3. Filters irrelevant files and collects supported source files.
4. Performs repository-structure, documentation and Python AST-based analysis.
5. Calculates code-quality, documentation, structure, maintainability and overall scores.
6. Generates evidence-based findings.
7. Optionally sends structured findings to an LLM for natural-language recommendations.
8. Displays the result in a web dashboard.

## Architecture

```text
GitHub Repository URL
        ↓
FastAPI Backend
        ↓
GitHub REST API Collector
        ↓
Repository Snapshot
        ↓
┌────────────────────────────────────┐
│ Structure │ README │ Python AST    │
│ Analysis  │ Checks │ Code Metrics  │
└──────────────────┬─────────────────┘
                   ↓
             Finding Aggregator
                   ↓
              Scoring Engine
                   ↓
            Optional AI / LLM
                   ↓
            Analysis Dashboard
```

## Technology Stack

- **Python 3.12+**
- **FastAPI** + Uvicorn
- **GitHub REST API**
- **Python `ast` module** for syntax-tree analysis
- **Requests** for HTTP integration
- **Pydantic** for request/response validation
- **SQLite-ready architecture** for future persistence
- **Optional LLM integration** through the OpenAI Responses API
- **HTML/CSS/JavaScript** dashboard
- **Pytest** automated tests
- **Docker** containerization
- **GitHub Actions** CI

## Analysis Capabilities

### Repository Metadata

- Repository name and owner
- Description
- Default branch
- Stars
- Forks
- Open issues
- Repository size
- Language statistics

### Repository Structure

- Source-file count
- Test-file detection
- Documentation-file detection
- Dependency/configuration file detection
- Top-level directory information

### Documentation

Checks for README presence and indicators for:

- Description/overview
- Installation/setup
- Usage/getting started
- Requirements/dependencies
- Testing information

### Python Code Analysis

The first language-specific analyzer uses Python AST and detects:

- Functions and classes
- Imports
- Function length
- High-complexity functions
- Deep nesting
- Broad exception handling
- Python parsing errors

### Scoring

The initial scoring model uses transparent weighted categories:

```text
Overall = Code Quality × 0.30
        + Documentation × 0.20
        + Structure × 0.20
        + Maintainability × 0.30
```

The scoring thresholds are heuristic indicators, not proof of correctness or security.

## AI Layer

AI is intentionally separated from deterministic analysis.

```text
Measured Findings
      ↓
Structured Evidence
      ↓
LLM
      ↓
Summary + Strengths + Weaknesses + Priority Actions
```

If no `OPENAI_API_KEY` is configured, the application still works and returns deterministic recommendations.

## Run Locally

### 1. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and optionally add:

```text
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Do not commit `.env` or API keys.

### 4. Start the application

```bash
uvicorn backend.app.main:app --reload
```

Open:

- Dashboard: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### 5. Run tests

```bash
pytest -q
```

## Docker

```bash
docker build -t ai-github-repository-analyzer .
docker run --rm -p 8000:8000 --env-file .env ai-github-repository-analyzer
```

## Security Notes

- Never expose GitHub or AI API keys in frontend code.
- Never execute downloaded repository source code.
- Treat repository content as untrusted input.
- Limit repository size and number of files analyzed.
- Keep AI recommendations grounded in measured findings.

## Limitations

- The initial language-specific analyzer focuses on Python.
- Static metrics are indicators and require context.
- AI recommendations can be incorrect.
- Very large repositories require stronger pagination, caching and asynchronous processing.
- Private repositories require appropriate authorization.

## Future Enhancements

- JavaScript/TypeScript, Java, Go and C++ analyzers
- Pull-request analysis
- Commit-history insights
- Repository comparison
- Historical quality trends
- Analysis persistence and user accounts
- GitHub App/OAuth integration
- Custom scoring profiles
- Local/private LLM support

## Resume Description

> Developed an AI-powered GitHub repository analyzer using Python and FastAPI that collects repository metadata and source information through REST APIs, performs AST-based static code and documentation analysis, calculates explainable quality metrics, and generates AI-assisted recommendations through a structured LLM workflow.

## Author

**Srivardhanreddy Devireddy**
