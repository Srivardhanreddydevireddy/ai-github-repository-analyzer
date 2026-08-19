# Project Interview Guide

## Purpose

This guide keeps the project practical and easy to defend in an interview. The goal is to understand the implementation rather than present an unnecessarily large architecture.

## How to Present the Project

The project is a practical developer tool. A user enters a GitHub repository URL. The system collects repository information through the GitHub REST API, analyzes supported source code and documentation, calculates rule-based quality indicators, and uses AI to explain the findings and suggest improvements.

### Core flow

```text
GitHub URL
  ↓
GitHub API
  ↓
Repository data + source files
  ↓
Static analysis
  ↓
Findings + metrics
  ↓
Scoring
  ↓
AI explanation/recommendations
  ↓
Report
```

## Development Suggestions

- Keep the first version focused rather than claiming support for every language.
- Make Python the first fully supported language and use AST for understandable source analysis.
- Keep FastAPI because it is simple and appropriate for a Python API project.
- Use deterministic rules for measurable findings and AI mainly for explanation.
- Avoid unnecessary enterprise infrastructure that cannot be justified.
- Keep SQLite for the initial analysis history.
- Make the scoring formula transparent.
- Document limitations honestly.
- Prefer readable modules over excessive abstraction.
- Test the important analyzer and scoring functions.
- Keep the dashboard simple and useful.
- Never claim a feature that has not actually been implemented and tested.

## Important Technical Knowledge

The developer should understand URL parsing, REST/JSON, GitHub authentication and rate limits, repository file filtering, static analysis, Python AST, cyclomatic complexity, documentation checks, scoring, LLM integration, FastAPI, SQLite, error handling, and testing.

## Interview Questions

### General

**Q: What problem does the project solve?**

A: It automates the initial technical review of a GitHub repository so that a developer can quickly understand its structure, documentation and selected code-quality indicators.

**Q: Why did you choose this project?**

A: I wanted a practical project that combines Python backend development, API integration, code analysis and AI rather than being only a CRUD application.

**Q: Did you build this yourself?**

A: I developed it as a personal project. AI tools can be used as development assistants for ideas, debugging and documentation, but I understand the architecture, implementation decisions and main code paths.

### GitHub/API

**Q: Why GitHub API?**

A: It provides structured repository information and is more reliable than scraping GitHub web pages.

**Q: What data do you collect?**

A: Repository name, owner, description, languages, stars, forks, default branch, file tree, README and relevant source files.

**Q: What happens with API rate limits?**

A: The application should detect rate-limit responses, avoid unnecessary retries and provide a useful message. Authentication can increase the practical request allowance.

### Analysis

**Q: What is static analysis?**

A: Analyzing source code without executing it.

**Q: What is AST?**

A: An Abstract Syntax Tree is a structured representation of source code. In Python it lets the analyzer inspect functions, classes, imports, branches and nesting.

**Q: Why not execute repository code?**

A: Repository code is untrusted. Static analysis lets us inspect source without giving arbitrary code execution privileges.

**Q: What is cyclomatic complexity?**

A: It is an indicator of independent control-flow paths. Higher complexity generally means more paths to consider during testing and maintenance.

### AI

**Q: What does the AI do?**

A: It receives structured findings from deterministic analysis, explains them, groups related issues and suggests practical improvements.

**Q: Why not let AI calculate the score?**

A: A deterministic scoring formula is reproducible and explainable. AI output can vary between runs.

**Q: Can AI recommendations be wrong?**

A: Yes. AI is probabilistic, so its output is advisory and should be grounded in observed findings.

**Q: Why not send the entire repository to the AI?**

A: It increases cost and context size and makes the result harder to control. Structured findings provide focused evidence.

### Backend/database

**Q: Why FastAPI?**

A: It is a lightweight Python framework suitable for REST APIs and provides automatic API documentation.

**Q: Why SQLite?**

A: The first version only needs simple local persistence for analysis history. A larger multi-user system could use PostgreSQL.

### Limitations

**Q: Can this prove that code is bug-free?**

A: No. It provides selected quality indicators and recommendations; it does not replace a complete code review.

**Q: What are the limitations?**

A: Language coverage, contextual code-quality judgments, repository size, private repository permissions and uncertainty in AI recommendations.

**Q: What would you improve next?**

A: Add more language-specific analyzers, pull-request analysis, historical score trends, better duplication analysis and stronger repository-level reporting.

## Practical Questions to Prepare For

- Show where the GitHub API is called.
- Show where Python AST is used.
- Show how a long function is detected.
- Show how the score is calculated.
- Show what happens when a repository is not found.
- Show what happens when README is missing.
- Show what happens for an unsupported language.
- Show where the AI prompt is defined.
- Show how AI failures are handled.
- Show where analysis history is stored.
- Explain how you would add JavaScript support.

## If You Do Not Know an Answer

Do not invent an answer. Say: “I haven't implemented that part yet, but based on the architecture I would approach it this way…” Then explain what you do understand.

## Resume Safety Checklist

Before listing the project, make sure you can:

- Explain every technology listed.
- Run and demonstrate the main workflow.
- Explain the GitHub API request/response.
- Explain AST simply.
- Explain at least three analyzer rules.
- Explain the scoring calculation.
- Explain exactly what AI does.
- Explain limitations.
- Show tests for important functionality.
- Avoid claiming unimplemented features.
