from backend.app.scoring import build_findings, calculate_scores


def test_scores_are_bounded():
    structure = {
        "source_files": 5,
        "test_files": 2,
        "dependency_files": ["requirements.txt"],
    }
    documentation = {"score": 80, "checks": {"exists": True}}
    code = {
        "high_complexity": [],
        "long_functions": [],
        "deep_nesting": [],
        "broad_exceptions": 0,
        "parse_errors": [],
    }
    scores = calculate_scores(structure, documentation, code)
    assert 0 <= scores["overall"] <= 100
    assert 0 <= scores["code_quality"] <= 100


def test_findings_detect_missing_tests():
    structure = {"source_files": 2, "test_files": 0, "dependency_files": []}
    documentation = {
        "score": 100,
        "checks": {"exists": True, "description": True, "installation": True, "usage": True, "requirements": True, "testing": True},
    }
    code = {"high_complexity": [], "long_functions": [], "deep_nesting": [], "broad_exceptions": 0, "parse_errors": []}
    findings = build_findings(structure, documentation, code)
    assert any(f["category"] == "Testing" for f in findings)
