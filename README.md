# VANE-SPACE-SLA (v1.0) 🛰️

**Deterministic Multi-Gate Telemetry Validation & Strict Prompt Grounding Toolkit**  
*Demonstration / Portfolio Project*

A lightweight, self-contained Python toolkit that demonstrates multi-gate telemetry validation and strict prompt grounding concepts.  
All external AI and infrastructure services are **intentionally simulated** so the project remains fully runnable without any paid or external dependencies.

---

### Live Site
- GitHub Pages: [https://anticipatedd.github.io/VANE-SPACE-SLA](https://anticipatedd.github.io/VANE-SPACE-SLA/)

![VANE-SPACE-SLA Concurrent Subagent Architecture](subagent_architecture_diagram.png)

---

## What This Project Does

- Simulates multi-gate telemetry validation
- Provides a strict / moderate / soft prompt grounding builder
- Uses environment variables (no hardcoded secrets)
- Includes structured logging
- Comes with a pytest test suite
- Has GitHub Actions CI with coverage gate

This is **not** a production RAG system and does **not** call real IBM watsonx, Milvus, FAISS, Redis, or PostgreSQL services.

---

## Quick Start

```bash
git clone https://github.com/AnticipatedD/VANE-SPACE-SLA.git
cd VANE-SPACE-SLA

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env

# Run tests (must pass with ≥ 70% coverage)
pytest --cov=. --cov-report=term-missing --cov-fail-under=70

# Run the main entry point
python vane_space_init.py
```
---

## Project Structure

VANE-SPACE-SLA/
├── vane_space_init.py
├── strict_prompt_builder.py
├── strict_prompt_builder.js
├── requirements.txt
├── package.json
├── package-lock.json
├── .env.example
├── .github/workflows/ci.yml
├── tests/
│   ├── test_vane_space_init.py
│   ├── test_strict_prompt_builder.py
│   └── test_voice_agents.py
├── CONTRIBUTING.md
└── README.md

---

## Development 
- All tests must pass locally before opening a PR.
- Coverage gate is enforced in CI (--cov-fail-under=70).
- Prefer small, focused commits that include both the change and its tests.

---
### Author

* **MD ABUL HOSSAIN**
* **IBM Business Partner Plus** | European F&T Expert
* **ID:** EX2026D1473148
* **Web of Science ResearcherID:** QQZ-6739-2026
* **ORCID:** 0009-0004-4378-5298
* **Microsoft Learn:** Level 10 (96 Badges, 17 Trophies)

---

## License
MIT License – see [LICENSE](license.md) file.

---
© 2026 MD ABUL HOSSAIN. All Rights Reserved.
