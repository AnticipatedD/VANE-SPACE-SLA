#!/usr/bin/env python3
"""Automated repository code health auditor using Google Gemini."""

import argparse
import os
from pathlib import Path
import sys
from typing import Dict, Iterator, Set
from google import genai
from google.genai.errors import APIError

IGNORED_DIRS: Set[str] = {
    ".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache", "dist", "build"
}
MAX_FILE_BYTES: int = 500_000  # 500 KB limit per file


def collect_python_files(target_dir: Path) -> Dict[Path, str]:
    """Recursively collect readable Python source files within target_dir."""
    collected: Dict[Path, str] = {}

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                if path.stat().st_size > MAX_FILE_BYTES:
                    collected[path] = "# [File skipped: exceeds maximum size limit]"
                    continue
                try:
                    collected[path] = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError) as exc:
                    collected[path] = f"# [Error reading file: {exc}]"

    return collected


def build_audit_prompt(file_contents: Dict[Path, str]) -> str:
    """Format collected files into clean Markdown context."""
    sections = [
        "Perform a rigorous code health and structural audit on the following repository source files.",
        "Identify potential bottlenecks, type-hint compliance, and structural improvements.\n"
    ]
    for path, code in file_contents.items():
        sections.append(f"### File: `{path.as_posix()}`\n```python\n{code}\n```\n")
    return "\n".join(sections)


def audit_repository(target_path: Path, model: str = "gemini-2.5-pro") -> None:
    """Executes the repository health check with streaming output."""
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("Error: GEMINI_API_KEY environment variable is not set.")

    if not target_path.exists():
        sys.exit(f"Error: Target path '{target_path}' does not exist.")

    files = collect_python_files(target_path)
    if not files:
        print("No Python files found to audit.")
        return

    prompt = build_audit_prompt(files)
    client = genai.Client()

    print(f"Auditing {len(files)} files with model '{model}'...\n")
    print("=== Automated Repository Health Report ===\n")

    try:
        response_stream = client.models.generate_content_stream(
            model=model,
            contents=prompt,
        )
        for chunk in response_stream:
            print(chunk.text, end="", flush=True)
        print("\n")
    except APIError as e:
        sys.exit(f"\nAPI Error during audit: {e.message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit repository source code via Gemini.")
    parser.add_argument(
        "target",
        nargs="?",
        default="src",
        type=Path,
        help="Path to directory or package to audit (default: 'src')",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-pro",
        help="Gemini model identifier (default: gemini-2.5-pro)",
    )
    args = parser.parse_args()
    audit_repository(args.target, model=args.model)
```
