import os
import sys
from google import genai

def audit_repository() -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    target_dir = "src"
    file_contents = {}
    
    if not os.path.exists(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        file_contents[path] = f.read()
                except Exception as e:
                    file_contents[path] = f"Error reading file: {e}"

    if not file_contents:
        print("No Python files found to audit.")
        return

    prompt = (
        "Perform a rigorous code health and structural audit on the following repository source files. "
        "Identify potential bottlenecks, type-hint compliance, and structural improvements:\n\n"
        f"{file_contents}"
    )

    client = genai.Client()
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    
    print("=== Automated Repository Health Report ===")
    print(response.text)

if __name__ == "__main__":
    audit_repository()
