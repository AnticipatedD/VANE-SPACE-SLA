# VANE-SPACE-SLA (v1.0) 🛰️

**Mission-Critical AI Assurance & Deterministic Zero-Trust Telemetry Engine**

---

## Executive Overview

`VANE-SPACE-SLA` is an enterprise-grade Python and Rust zero-trust telemetry, prompt-grounding, and agentic orchestration toolkit. Designed for resource-constrained edge environments and high-throughput ingestion gateways, the engine bridges probabilistic AI outputs with deterministic cryptographic verification.

* **Primary Stack:** Python 3.11+, Rust (Ed25519 cryptography, dCBOR serialization), and the official `google-genai` SDK (`gemini-2.5-flash` / `gemini-2.5-pro`).
* **Architecture:** Deterministic Zero-Trust Telemetry Pipeline featuring sliding-window anti-replay protection, causal hash-chaining, and multi-agent architectural auditing.

<a href="https://launchnest.io/p/vane-space-sla-enterprise-command-center" target="_blank">
  <img src="https://launchnest.io/badge/vane-space-sla-enterprise-command-center.svg?variant=featured" alt="VANE-SPACE-SLA Enterprise Command Center on LaunchNest" width="220" height="56" />
</a>

---

### Live Site
- GitHub Pages: [https://anticipatedd.github.io/VANE-SPACE-SLA](https://anticipatedd.github.io/VANE-SPACE-SLA/)

![VANE-SPACE-SLA Concurrent Subagent Architecture](subagent_architecture_diagram.png)

---

## Core Features & Modules

1. **Deterministic Telemetry Evaluation (`src/main.py`)**: Validates real-time packet payloads against strict Pydantic schemas and cryptographic signatures.
2. **Automated Code Health Auditing (`src/repo_audit.py`)**: Recursively scans repository source files, filters build artifacts and virtual environments, and leverages Gemini models to generate structural health reports.
3. **Multi-Agent Orchestration (`src/agent_orchestrator.py`)**: Executes structured multi-persona pipelines (Code Architect & Security Auditor) with live token streaming and robust error handling.
4. **Rust Verification Core (`telemetry_core.rs`)**: Implements strict canonical serialization (dCBOR), sliding-window replay bitmasks, and hardware-anchored key attestation.

---

## Installation & Environment Setup

Ensure `Termux` (ARM64) or the target Linux/macOS environment has Python 3.11+ installed. The repository relies strictly on locked dependency pins via `requirements-lock.txt`.

```bash
# Clone the repository
git clone [https://github.com/AnticipatedD/VANE-SPACE-SLA.git](https://github.com/AnticipatedD/VANE-SPACE-SLA.git)
cd VANE-SPACE-SLA

# Create virtual environment and install locked dependencies
python -m venv .venv
source .venv/bin/activate

# On Windows: .venv\Scripts\activate
pip install -r requirements-lock.txt
```

# Execution & Testing
Export your Gemini API key before executing audit or orchestration utilities:
```bash
export GEMINI_API_KEY="your_api_key_here"

# Run automated repository health audit
python src/repo_audit.py src --model gemini-2.5-flash

# Run multi-agent architectural pipeline
python src/agent_orchestrator.py "Enhance telemetry packet validation with cryptographic verification" --model gemini-2.5-flash
```

# Running the Test Suite
The test suite utilizes `pytest`, `pytest-cov`, and `pytest-mock` to ensure high test coverage and robust unit validation:
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=70 -v tests/

# CI/CD Pipeline & Code Quality Automated quality gates are enforced via GitHub Actions (`.github/workflows/ci.yml`), executing:Linting: ruff check src/ tests/Type Checking: mypy src/ 
Testing & Coverage: pytest with strict coverage threshold gating ($\ge 70\%$).
```
---

## What This Project Does

- Simulates multi-gate validation
- Provides a strict / moderate / soft prompt grounding builder
- Uses environment variables
- Includes structured logging
- Comes with a pytest test suite
- Has GitHub Actions CI with coverage gate

---

## Project Structure

VANE-SPACE-SLA/
├── src/
│   ├── repo_audit.py
│   ├── agent_orchestrator.py
│   └── vane_space_init.py
├── Rust-Edge-Engine/
│   └── telemetry_core.rs
├── tests/
│   ├── test_repo_audit.py
│   ├── test_agent_orchestrator.py
│   ├── test_vane_space_init.py
│   ├── test_strict_prompt_builder.py
│   └── test_voice_agents.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── strict_prompt_builder.py
├── strict_prompt_builder.js
├── requirements-lock.txt
├── package.json
├── package-lock.json
├── .env.example
├── ARCHITECTURE.md
├── CONTRIBUTING.md
└── README.md

---

## Development 
- All tests must pass locally before opening a PR.
- Coverage gate is enforced in CI (--cov-fail-under=70).
- Prefer small, focused commits that include both the change and its tests.
~/VANE-SPACE-SLA $ python src/agent_orchestrator.py "Enhance telemetry packet validation with cryptographic verification"

---

## Compliance & Architectural Directive

1. **Deterministic Wire Enforcement:**
Standardize schema serialization using a strictly validated CDDL (Concise Data Definition Language) profile. Include tests across ARM64 (Android/iOS) and x86_64 ingestion clusters to assert matching binary digests over test vectors.

2. **Identity-to-Key Hardware Attestation:**
Prior to telemetry dispatch, edge nodes must complete an explicit mutual attestation handshake (Apple App Attest / Android Keystore Key Attestation) to enroll their hardware-backed key. The gateway must resolve `key_id` to this verified, hardware-anchored certificate chain.

3. **Formal Resolution of Out-of-Order Streams:**
If UDP/QUIC unreliable transport is mandated for edge telemetry, **strictly decouple the ingestion ingress from the ledger auditor**. Ingestion gateways should confirm signatures and track the replay bitmask, while a downstream stream processor reassembles sequences to verify the Merkle or hash-chain timeline.

---
### Author

* **MD ABUL HOSSAIN**
* **IBM Business Partner Plus** | European F&T Expert
* **ID:** EX2026D1473148
* **Web of Science ResearcherID:** QQZ-6739-2026
* **ORCID:** 0009-0004-4378-5298
* **Microsoft Learn:** Level 13 (234 Badges, 43 Trophies)

---

## License
MIT License – see [LICENSE](license.md) file.

---
© 2026 MD ABUL HOSSAIN. All Rights Reserved.
