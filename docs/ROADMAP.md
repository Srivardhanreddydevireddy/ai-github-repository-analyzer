# Development Roadmap

## Phase 1 — Foundation

- Define project structure.
- Define repository and analysis data models.
- Document API contracts.
- Set up Python environment and dependencies.

## Phase 2 — GitHub Data Collection

- Parse repository URLs.
- Connect to GitHub REST API.
- Collect repository metadata.
- Retrieve README content.
- Retrieve repository tree.
- Handle pagination, rate limits, missing files, and API errors.

## Phase 3 — Static Analysis

- Implement Python source parsing with AST.
- Count files, functions, classes, and lines.
- Identify complexity indicators.
- Add maintainability-related rules.
- Analyze README and project organization.

## Phase 4 — Scoring

- Normalize findings.
- Define severity levels.
- Create transparent weighted quality categories.
- Generate an explainable repository score.

## Phase 5 — AI Recommendations

- Design structured prompts.
- Pass findings and relevant context to an LLM.
- Generate prioritized recommendations.
- Validate and structure model output.
- Handle model/API failures gracefully.

## Phase 6 — Backend

- Build FastAPI endpoints.
- Add request validation.
- Add analysis status handling.
- Store results in SQLite.

## Phase 7 — Dashboard

- Repository input screen.
- Summary metrics.
- Quality score visualization.
- Findings list.
- AI recommendations.
- Analysis history.

## Phase 8 — Quality and Deployment

- Unit tests.
- Integration tests.
- API tests.
- Performance improvements.
- Documentation cleanup.
- Containerization and deployment configuration.

## Future Enhancements

- Support JavaScript/TypeScript, Java, and other languages.
- Pull-request and commit history analysis.
- Trend analysis across repeated scans.
- Custom organization rules.
- Local/private LLM support.
- GitHub App integration.
