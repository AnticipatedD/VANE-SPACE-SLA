#!/usr/bin/env python3
"""Multi-agent orchestrator for architectural and security review."""

import argparse
import os
import sys
from typing import NamedTuple
from google import genai
from google.genai.errors import APIError


class OrchestrationResult(NamedTuple):
    architectural_plan: str
    security_audit: str


def run_agent_orchestrator(
    task_description: str,
    model: str = "gemini-2.5-flash"
) -> OrchestrationResult:
    """Runs sequential persona agents to generate and audit system architectures."""
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("Error: GEMINI_API_KEY environment variable is not set.")

    client = genai.Client()

    try:
        # Phase 1: Code Architect Persona
        architect_prompt = (
            "You are an expert Code Architect specializing in deterministic AI governance "
            "and mobile edge systems. Review the following objective and provide a precise "
            "architectural implementation strategy:\n"
            f"Objective: {task_description}"
        )
        architect_response = client.models.generate_content(
            model=model,
            contents=architect_prompt,
        )
        plan_text = architect_response.text or ""

        # Phase 2: Security Auditor Persona
        security_prompt = (
            "You are a Zero-Trust Security Auditor. Review the architectural plan below, "
            "evaluate zero-trust telemetry risks, and enforce strict compliance standards:\n"
            f"Architectural Plan:\n{plan_text}"
        )
        security_response = client.models.generate_content(
            model=model,
            contents=security_prompt,
        )
        security_text = security_response.text or ""

    except APIError as e:
        sys.exit(f"Gemini API invocation error: {e.message}")

    return OrchestrationResult(
        architectural_plan=plan_text,
        security_audit=security_text,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-agent architectural orchestrator.")
    parser.add_argument(
        "task",
        nargs="?",
        default="Deploy a real-time zero-trust validation loop for ARM64 node telemetry.",
        help="Task or objective for the agents to process.",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="Gemini model tag to use (default: gemini-2.5-flash)",
    )
    args = parser.parse_args()

    result = run_agent_orchestrator(args.task, model=args.model)

    print("=== [Agent 1: Code Architect] ===")
    print(result.architectural_plan)
    print("\n" + "=" * 40 + "\n")
    print("=== [Agent 2: Security Auditor] ===")
    print(result.security_audit)
```
