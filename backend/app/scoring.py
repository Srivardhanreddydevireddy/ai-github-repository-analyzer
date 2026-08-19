from typing import Any


def _clamp(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 1)


def calculate_scores(structure: dict[str, Any], documentation: dict[str, Any], code: dict[str, Any]) -> dict[str, float]:
    code_score = 100.0
    code_score -= min(30, len(code["high_complexity"]) * 7)
    code_score -= min(20, len(code["long_functions"]) * 4)
    code_score -= min(20, len(code["deep_nesting"]) * 5)
    code_score -= min(10, code["broad_exceptions"] * 2)
    code_score -= min(20, len(code["parse_errors"]) * 10)

    structure_score = 60.0
    if structure["source_files"] > 0:
        structure_score += 15
    if structure["test_files"] > 0:
        structure_score += 15
    if structure["dependency_files"]:
        structure_score += 10

    documentation_score = documentation["score"]

    maintainability_score = (code_score * 0.55) + (structure_score * 0.25) + (documentation_score * 0.20)
    overall = (code_score * 0.30) + (documentation_score * 0.20) + (structure_score * 0.20) + (maintainability_score * 0.30)

    return {
        "code_quality": _clamp(code_score),
        "documentation": _clamp(documentation_score),
        "structure": _clamp(structure_score),
        "maintainability": _clamp(maintainability_score),
        "overall": _clamp(overall),
    }


def build_findings(structure: dict[str, Any], documentation: dict[str, Any], code: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    if not documentation["checks"]["exists"]:
        findings.append({"category": "Documentation", "severity": "high", "title": "README is missing", "evidence": "No README content was found.", "recommendation": "Add a README with project purpose, setup, usage, and technology details."})
    else:
        missing = [name for name, ok in documentation["checks"].items() if not ok and name != "exists"]
        if missing:
            findings.append({"category": "Documentation", "severity": "medium", "title": "Documentation sections are incomplete", "evidence": f"Missing indicators: {', '.join(missing)}.", "recommendation": "Add the missing documentation sections and keep setup and usage instructions current."})

    if structure["test_files"] == 0:
        findings.append({"category": "Testing", "severity": "medium", "title": "No obvious test files detected", "evidence": "The repository tree did not contain files matching the test heuristics.", "recommendation": "Add automated tests for important modules and edge cases."})

    if code["high_complexity"]:
        findings.append({"category": "Code Quality", "severity": "high", "title": "High-complexity functions detected", "evidence": f"Detected {len(code['high_complexity'])} function(s) above the complexity threshold.", "recommendation": "Break complex functions into smaller units and add focused tests."})

    if code["long_functions"]:
        findings.append({"category": "Maintainability", "severity": "medium", "title": "Long functions detected", "evidence": f"Detected {len(code['long_functions'])} function(s) longer than the configured threshold.", "recommendation": "Extract cohesive responsibilities into smaller functions or modules."})

    if code["deep_nesting"]:
        findings.append({"category": "Maintainability", "severity": "medium", "title": "Deep nesting detected", "evidence": f"Detected {len(code['deep_nesting'])} function(s) with deep control-flow nesting.", "recommendation": "Use guard clauses, helper functions, or simpler control flow to reduce nesting."})

    if code["broad_exceptions"]:
        findings.append({"category": "Code Quality", "severity": "low", "title": "Broad exception handling detected", "evidence": f"Detected {code['broad_exceptions']} broad exception handler(s).", "recommendation": "Catch specific exceptions where practical and handle expected failures explicitly."})

    if not findings:
        findings.append({"category": "Overall", "severity": "info", "title": "No major heuristic issues detected", "evidence": "The configured checks did not identify major issues.", "recommendation": "Continue with regular testing, reviews, and documentation maintenance."})

    return findings
