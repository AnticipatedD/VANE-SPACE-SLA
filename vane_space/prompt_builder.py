#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Strict Prompt Grounding Builder Module
Author: MD ABUL HOSSAIN
Description: Enforces hard context boundaries on LLM prompt construction
"""

import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from vane_space.logging_config import configure_logging
from vane_space.errors import PromptGroundingError

load_dotenv()
logger = configure_logging("vane_space.prompt_builder")


class StrictPromptBuilder:
    """
    Orchestrates deterministic prompt generation by grounding unstructured inputs
    against verified, audited data context structures.
    """

    SUPPORTED_STRENGTHS = ("strict", "moderate", "soft")

    def __init__(
        self,
        model_id: str = "demo-model",
        grounding_strength: str = "strict"
    ) -> None:
        """
        Initialize the prompt builder with model ID and grounding strength.
        
        Args:
            model_id: Target LLM model identifier
            grounding_strength: One of 'strict', 'moderate', or 'soft'
        
        Raises:
            TypeError: If model_id is not a string
            PromptGroundingError: If grounding_strength is invalid
        """
        if not isinstance(model_id, str):
            raise TypeError("Model ID parameter must be a string primitive.")

        self.model_id = model_id
        self.conversation_history: List[Dict[str, str]] = []

        # Safe extraction of organizational environment variables
        self.eu_expert_id = os.getenv("EU_EXPERT_ID", "MYEUEXPERTID")
        self.ibm_saas_account_id = os.getenv("IBM_SAAS_ACCOUNT_ID", "demo-account")

        # Initialize validation bounds
        self.set_grounding_strength(grounding_strength)

    def set_grounding_strength(self, strength: str) -> None:
        """
        Configure the strictness profile of the validation engine.
        
        Args:
            strength: One of 'strict', 'moderate', or 'soft'
        
        Raises:
            PromptGroundingError: If strength is not supported
        """
        if strength not in self.SUPPORTED_STRENGTHS:
            msg = f"Invalid grounding strength '{strength}'. Use: {' | '.join(self.SUPPORTED_STRENGTHS)}"
            logger.error(f"Rejected illegal grounding strength: {strength}")
            raise PromptGroundingError(msg)
        self.grounding_strength = strength
        logger.info(f"Grounding strength set to: {strength}")

    def validate_input_safety(self, user_query: str) -> bool:
        """
        Defensive gate guarding against basic prompt injection sequences.
        
        Args:
            user_query: User input string to validate
        
        Returns:
            True if query is safe, False otherwise
        """
        if not user_query or not user_query.strip():
            logger.warning("Empty or whitespace-only query rejected")
            return False

        # Catch basic attempt boundaries
        if "ignore previous instructions" in user_query.lower():
            logger.warning("Potential prompt disruption vector intercepted.")
            return False

        return True

    def build_grounded_prompt(
        self,
        user_query: str,
        audited_contexts: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Stitch context truth tables with target user queries into an isolated prompt template.
        
        Args:
            user_query: User's query string
            audited_contexts: List of verified context blocks
        
        Returns:
            Dictionary with 'prompt' and 'metadata' keys
        """
        if audited_contexts is None:
            audited_contexts = []

        # Enforce defensive payload checks
        if not self.validate_input_safety(user_query):
            user_query = "[SECURITY_ALTERATION: SAFE_FALLBACK_QUERY_APPLIED]"

        if self.grounding_strength == "strict":
            mandate = (
                "STRICT GROUNDING ACTIVE\n"
                "Answer ONLY from the provided context blocks.\n"
                "If insufficient, reply exactly: [HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]"
            )
        elif self.grounding_strength == "moderate":
            mandate = "MODERATE GROUNDING: Prefer context blocks. Mark any external knowledge clearly."
        else:  # soft
            mandate = "SOFT GUIDANCE: Use context as primary source."

        truth_context = "\n".join(
            f"[CONTEXT_BLOCK_{i:02d}]: {block.strip()}"
            for i, block in enumerate(audited_contexts)
            if block
        )

        prompt = (
            f"SYSTEM_MODEL_TARGET: {self.model_id}\n"
            f"REGULATORY_EXPERT_ID: {self.eu_expert_id}\n"
            f"GOVERNANCE_MANDATE:\n{mandate}\n\n"
            f"VERIFIED_CONTEXT_BLOCKS:\n{truth_context if truth_context else '[EMPTY]'}\n\n"
            f"USER QUERY: {user_query}\n"
            f"RESPONSE BOUNDARY:"
        )

        logger.info(f"Grounded prompt built with {len(audited_contexts)} context blocks")

        return {
            "prompt": prompt,
            "metadata": {
                "model_id": self.model_id,
                "grounding_strength": self.grounding_strength,
                "context_block_count": len(audited_contexts),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "pipeline_version": "2.1.0-prod"
            }
        }
