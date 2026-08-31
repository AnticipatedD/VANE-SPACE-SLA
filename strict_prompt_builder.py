#!/usr/bin/env python3
"""
Strict Prompt Grounding Builder - Demonstration Version
Author: MD ABUL HOSSAIN
"""

import os
import re
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("strict_prompt")

class StrictPromptBuilder:
    def __init__(self, model_id: str = "demo-model", grounding_strength: str = "strict"):
        self.model_id = model_id
        self.grounding_strength = grounding_strength
        self.conversation_history: List[Dict[str, str]] = []

        self.eu_expert_id = os.getenv("EU_EXPERT_ID", "MYEUEXPERTID")
        self.ibm_saas_account_id = os.getenv("IBM_SAAS_ACCOUNT_ID", "demo-account")

    def set_grounding_strength(self, strength: str) -> None:
        if strength not in ("strict", "moderate", "soft"):
            raise ValueError("Invalid grounding strength. Use: strict | moderate | soft")
        self.grounding_strength = strength

    def build_grounded_prompt(self, user_query: str, audited_contexts: Optional[List[str]] = None) -> Dict[str, Any]:
        if audited_contexts is None:
            audited_contexts = []

        if self.grounding_strength == "strict":
            mandate = (
                "STRICT GROUNDING ACTIVE\n"
                "Answer ONLY from the provided context blocks.\n"
                "If insufficient, reply exactly: [HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]"
            )
        elif self.grounding_strength == "moderate":
            mandate = "MODERATE GROUNDING: Prefer context blocks. Mark any external knowledge clearly."
        else:
            mandate = "SOFT GUIDANCE: Use context as primary source."

        truth_context = "\n".join(
            f"[CONTEXT_{i}]: {block}" for i, block in enumerate(audited_contexts)
        )

        prompt = (
            f"MODEL: {self.model_id}\n"
            f"EU_EXPERT: {self.eu_expert_id}\n"
            f"{mandate}\n\n"
            f"{truth_context}\n\n"
            f"USER QUERY: {user_query}\n"
            f"RESPONSE:"
        )

        return {
            "prompt": prompt,
            "metadata": {
                "model_id": self.model_id,
                "grounding_strength": self.grounding_strength,
                "context_block_count": len(audited_contexts),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
