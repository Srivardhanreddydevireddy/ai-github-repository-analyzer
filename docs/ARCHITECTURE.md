# System Architecture

## Overview

The application follows a layered architecture so that GitHub integration, deterministic analysis, AI reasoning, and presentation remain separate.

## Layers

### 1. API Layer

Receives repository analysis requests and returns analysis results. FastAPI is planned for this layer.

### 2. Repository Collector

Responsible for communicating with GitHub APIs and retrieving metadata, README content, repository trees, and relevant source files.

### 3. Analysis Engine

Runs deterministic checks against the collected repository data. For Python, the initial implementation will use the built-in `ast` module and additional analysis utilities where appropriate.

### 4. Finding Aggregator

Normalizes raw analysis results into structured findings with fields such as category, severity, evidence, and recommendation context.

### 5. AI Recommendation Engine

Receives the structured findings and selected repository context. It explains findings, prioritizes improvements, and produces actionable recommendations.

### 6. Persistence Layer

SQLite is planned for storing analysis requests, repository snapshots, findings, and generated reports during the initial version.

### 7. Presentation Layer

A lightweight dashboard will display repository metadata, quality metrics, findings, and AI recommendations.

## Data Flow

```text
Client
  |
  v
FastAPI Endpoint
  |
  v
GitHub Collector -----> GitHub REST API
  |
  v
Repository Snapshot
  |
  +----> Metadata Analyzer
  |
  +----> Documentation Analyzer
  |
  +----> Source Analyzer
  |
  v
Finding Aggregator
  |
  v
Quality Score
  |
  v
AI Recommendation Engine
  |
  v
Structured Report
  |
  +----> SQLite
  |
  +----> Dashboard / API Response
```

## Design Principles

- Keep deterministic measurements separate from AI-generated interpretation.
- Validate external API responses before processing them.
- Do not store GitHub tokens or API keys in source control.
- Limit the amount of repository code sent to an external AI provider.
- Make every recommendation traceable to an observed finding where possible.
- Design language analyzers as replaceable modules.
