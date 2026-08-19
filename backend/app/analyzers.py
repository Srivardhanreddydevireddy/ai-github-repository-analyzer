import ast
from pathlib import PurePosixPath
from typing import Any


def analyze_structure(tree: list[str]) -> dict[str, Any]:
    source_files = [p for p in tree if p.lower().endswith((".py", ".js", ".ts", ".java", ".go", ".cpp", ".c", ".cs"))]
    test_files = [p for p in tree if "test" in PurePosixPath(p).name.lower() or "/tests/" in f"/{p.lower()}/"]
    docs = [p for p in tree if p.lower().endswith((".md", ".rst", ".txt"))]
    dependency_files = [
        p for p in tree
        if PurePosixPath(p).name.lower() in {
            "requirements.txt", "pyproject.toml", "package.json", "pom.xml", "build.gradle", "go.mod"
        }
    ]
    top_dirs = sorted({p.split("/")[0] for p in tree if "/" in p})
    return {
        "total_files_scanned": len(tree),
        "source_files": len(source_files),
        "test_files": len(test_files),
        "documentation_files": len(docs),
        "dependency_files": dependency_files,
        "top_level_directories": top_dirs,
    }


def analyze_readme(readme: str) -> dict[str, Any]:
    text = readme.lower()
    checks = {
        "exists": bool(readme.strip()),
        "description": any(k in text for k in ("description", "overview", "about")),
        "installation": any(k in text for k in ("installation", "install", "setup")),
        "usage": any(k in text for k in ("usage", "how to use", "getting started")),
        "requirements": any(k in text for k in ("requirements", "dependencies", "prerequisites")),
        "testing": "test" in text,
    }
    score = round(sum(checks.values()) / len(checks) * 100, 1)
    return {"checks": checks, "score": score, "word_count": len(readme.split())}


def analyze_python_file(path: str, source: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": path,
        "lines": len(source.splitlines()),
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "long_functions": [],
        "high_complexity": [],
        "deep_nesting": [],
        "broad_exceptions": 0,
        "parse_error": None,
    }
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        result["parse_error"] = f"Line {exc.lineno}: {exc.msg}"
        return result

    result["functions"] = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree))
    result["classes"] = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
    result["imports"] = sum(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))
    result["broad_exceptions"] = sum(
        isinstance(n, ast.ExceptHandler) and (n.type is None or isinstance(n.type, ast.Name) and n.type.id == "Exception")
        for n in ast.walk(tree)
    )

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            length = end - node.lineno + 1
            complexity = 1 + sum(
                isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.IfExp, ast.BoolOp, ast.comprehension))
                for child in ast.walk(node)
            )
            nesting = _max_nesting(node)
            if length > 40:
                result["long_functions"].append({"name": node.name, "line": node.lineno, "lines": length})
            if complexity > 10:
                result["high_complexity"].append({"name": node.name, "line": node.lineno, "complexity": complexity})
            if nesting > 4:
                result["deep_nesting"].append({"name": node.name, "line": node.lineno, "depth": nesting})
    return result


def _max_nesting(node: ast.AST) -> int:
    def walk(current: ast.AST, depth: int) -> int:
        branch_nodes = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith)
        current_depth = depth + (1 if isinstance(current, branch_nodes) else 0)
        return max([current_depth] + [walk(child, current_depth) for child in ast.iter_child_nodes(current)])
    return max(0, walk(node, 0) - 1)


def analyze_python_sources(contents: dict[str, str]) -> dict[str, Any]:
    files = [analyze_python_file(path, source) for path, source in contents.items() if path.endswith(".py")]
    return {
        "files_analyzed": len(files),
        "lines": sum(f["lines"] for f in files),
        "functions": sum(f["functions"] for f in files),
        "classes": sum(f["classes"] for f in files),
        "imports": sum(f["imports"] for f in files),
        "long_functions": [x for f in files for x in f["long_functions"]],
        "high_complexity": [x for f in files for x in f["high_complexity"]],
        "deep_nesting": [x for f in files for x in f["deep_nesting"]],
        "broad_exceptions": sum(f["broad_exceptions"] for f in files),
        "parse_errors": [
            {"path": f["path"], "error": f["parse_error"]}
            for f in files if f["parse_error"]
        ],
    }
