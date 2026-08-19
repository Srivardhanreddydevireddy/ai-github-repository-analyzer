from backend.app.analyzers import analyze_python_file, analyze_readme, analyze_structure, analyze_python_sources


def test_readme_analysis():
    result = analyze_readme("# Demo\n## Installation\n## Usage\nrequirements and tests")
    assert result["checks"]["exists"] is True
    assert result["checks"]["installation"] is True
    assert result["score"] > 0


def test_structure_analysis():
    result = analyze_structure(["src/main.py", "tests/test_main.py", "README.md", "requirements.txt"])
    assert result["source_files"] == 1
    assert result["test_files"] == 1
    assert "requirements.txt" in result["dependency_files"]


def test_python_ast_analysis():
    source = "def add(a, b):\n    return a + b\n"
    result = analyze_python_file("main.py", source)
    assert result["functions"] == 1
    assert result["classes"] == 0
    assert result["parse_error"] is None


def test_python_source_aggregation():
    result = analyze_python_sources({"main.py": "class A:\n    pass\n"})
    assert result["files_analyzed"] == 1
    assert result["classes"] == 1
