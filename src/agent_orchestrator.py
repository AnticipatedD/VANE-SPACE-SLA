#!/usr/bin/env python3
"""Multi-agent orchestration pipeline using Google Gemini."""

from __future__ import annotations

import argparse
import sys
from google import genai
from google.genai import types
from google.genai.errors import APIError


def run_agent_phase(
    client: genai.Client,
    model: str,
    system_instruction: str,
    user_input: str,
    phase_header: str,
) -> str:
    """Execute a single agent streaming phase with system instructions."""
    print(phase_header)
    output_parts: list[str] = []

    response_stream = client.models.generate_content_stream(
        model=model,
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        ),
    )

    for chunk in response_stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            output_parts.append(chunk.text)

    print("\n\n" + "=" * 40 + "\n")
    return "".join(output_parts)


def run_agent_orchestrator(task_description: str, model: str = "gemini-2.5-flash") -> None:
    """Orchestrates multi-phase architecture and security analysis."""
    client = genai.Client()

    # Phase 1: Code Architect
    architect_system = (
        "You are an expert Code Architect specializing in deterministic AI governance "
        "and mobile edge systems. Provide precise architectural implementation strategies."
    )
    architect_plan = run_agent_phase(
        client=client,
        model=model,
        system_instruction=architect_system,
        user_input=f"Objective: {task_description}",
        phase_header=f"=== [Agent 1: Code Architect] (Model: {model}) ===",
    )

    # Phase 2: Security Auditor
    security_system = (
        "You are a Zero-Trust Security Auditor. Review the architectural plan, "
        "evaluate zero-trust telemetry risks, and enforce strict compliance standards."
    )
    run_agent_phase(
        client=client,
        model=model,
        system_instruction=security_system,
        user_input=f"Architectural Plan:\n{architect_plan}",                                                                  phase_header="=== [Agent 2: Security Auditor] ===",
    )


def main() -> int:                                             """CLI execution entrypoint."""
    parser = argparse.ArgumentParser(description="Multi-agent architectural orchestration via Gemini.")                   parser.add_argument(                                           "task",                                                    nargs="?",
        default="Deploy a real-time zero-trust validation loop for ARM64 node telemetry.",                                    help="Task description for the agent pipeline",        )                                                          parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="Gemini model identifier (default: gemini-2.5-flash)",
    )
    args = parser.parse_args()

    try:
        run_agent_orchestrator(args.task, model=args.model)
        return 0                                               except APIError as exc:
        print(f"API Error during orchestration: {exc.message}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Orchestration failure: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
