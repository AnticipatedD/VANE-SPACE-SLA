#!/usr/bin/env python3
"""Automated repository code health auditor using Google Gemini."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
from google import genai
from google.genai import types
from google.genai.errors import APIError

IGNORED_DIRS: set[str] = {
    ".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache", "dist", "build"
}
MAX_FILE_BYTES: int = 500_000  # 500 KB limit per file


def collect_python_files(target_dir: Path) -> dict[Path, str]:
    """Recursively collect readable Python source files within target_dir."""
    collected: dict[Path, str] = {}

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                try:
                    if path.stat().st_size > MAX_FILE_BYTES:
                        collected[path] = "# [File skipped: exceeds maximum size limit]"
                        continue
                    collected[path] = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError) as exc:
                    collected[path] = f"# [Error reading file: {exc}]"

    return collected


def build_audit_prompt(file_contents: dict[Path, str]) -> str:
    """Format collected files into clean Markdown context."""
    sections: list[str] = [
        "Perform a rigorous code health and structural audit on the following repository source files.",
        "Identify potential bottlenecks, type-hint compliance, and structural improvements.\n"
    ]
    for path, code in file_contents.items():
        sections.append(f"### File: `{path.as_posix()}`\n```python\n{code}\n```\n")
    return "\n".join(sections)


def audit_repository(target_path: Path, model: str = "gemini-2.5-flash", client: genai.Client | None = None) -> None:
    """Executes the repository health check with streaming output."""
    if not target_path.exists():
        raise FileNotFoundError(f"Target path '{target_path}' does not exist.")

    files = collect_python_files(target_path)
    if not files:
        print("No Python files found to audit.")
        return

    prompt = build_audit_prompt(files)
    if client is None:
        client = genai.Client()

    print(f"Auditing {len(files)} files with model '{model}'...\n")
    print("=== Automated Repository Health Report ===\n")

    response_stream = client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )
    for chunk in response_stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


def main() -> int:
    """CLI execution entrypoint."""
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
        default="gemini-2.5-flash",
        help="Gemini model identifier (default: gemini-2.5-flash)",
    )
    args = parser.parse_args()

    try:
        audit_repository(args.target, model=args.model)
        return 0
    except (FileNotFoundError, APIError, Exception) as exc:
        print(f"Audit failure: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
