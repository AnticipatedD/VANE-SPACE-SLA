import os
import sys
from google import genai

def run_agent_orchestrator(task_description: str) -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client()
    
    # Phase 1: Code Architect Persona
    architect_prompt = (
        "You are an expert Code Architect specializing in deterministic AI governance and mobile edge systems. "
        "Review the following objective and provide a precise architectural implementation strategy:\n"
        f"Objective: {task_description}"
    )
    architect_response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=architect_prompt
    )
    
    print("=== [Agent 1: Code Architect] ===")
    print(architect_response.text)
    print("\n" + "="*40 + "\n")

    # Phase 2: Security Auditor Persona
    security_prompt = (
        "You are a Zero-Trust Security Auditor. Review the architectural plan below, "
        "evaluate zero-trust telemetry risks, and enforce strict compliance standards:\n"
        f"Architectural Plan:\n{architect_response.text}"
    )
    security_response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=security_prompt
    )
    
    print("=== [Agent 2: Security Auditor] ===")
    print(security_response.text)

if __name__ == "__main__":
    default_task = "Deploy a real-time zero-trust validation loop for ARM64 node telemetry."
    task = sys.argv[1] if len(sys.argv) > 1 else default_task
    run_agent_orchestrator(task)
