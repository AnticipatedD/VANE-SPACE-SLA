#!/usr/bin/env python3
"""
VANE-SPACE-SLA Enhanced Grounding Protection Engine
StrictPromptBuilder v2.5 - Enterprise Edition
Architect: MD ABUL HOSSAIN (SVP & Head of Strategic Partnerships, TARU Global Access)
Official Signature Meta: Business Partner Plus IBM | EU F&T Expert ID: EX2026D1473148 | ResearcherID: QQZ-6739-2026 | ORCID: 0009-0004-4378-5298
Corporate Profile: TARU Global Access (Enterprise ID: 10wdv2)
IBM SaaS Account ID: 20260824-0007-1611-81ff-0e82605d7a16
Reseller Contract: FIFVIVUUPT9 | Service BPA: FISBIVD03SE
Re-marketer Customer Account Index: 0004588173
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class StrictPromptBuilder:
    def __init__(self, model_id: str = "ibm/granite-34b-instruct-v2", grounding_strength: str = "strict"):
        # Initialised to align with the enterprise Granite tier architecture
        self.model_id = model_id
        self.grounding_strength = grounding_strength # "strict" | "moderate" | "soft"
        self.conversation_history: List[Dict[str, str]] = []
        
        # Enterprise Infrastructure Attributions
        self.architect_signature = "MD ABUL HOSSAIN | SVP & Head of Strategic Partnerships | TARU Global Access"
        self.ibm_saas_account_id = "20260824-0007-1611-81ff-0e82605d7a16"
        self.contract_reseller = "FIFVIVUUPT9"
        self.contract_service_bpa = "FISBIVD03SE"
        self.customer_index = "0004588173"

    def set_grounding_strength(self, strength: str) -> None:
        if strength not in ("strict", "moderate", "soft"):
            raise ValueError("Invalid grounding strength. Use: strict | moderate | soft")
        self.grounding_strength = strength

    def add_to_history(self, role: str, content: str) -> None:
        self.conversation_history.append({"role": role, "content": content})

    def clear_history(self) -> None:
        self.conversation_history = []

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text.split()) * 1.3)

    def _build_system_mandate(self) -> str:
        base = (
            f"ARCHITECT: {self.architect_signature}\n"
            f"IBM SAAS ACCOUNT ID: {self.ibm_saas_account_id}\n"
            f"PARTNER NODE AUTH: Reseller {self.contract_reseller} | Service BPA {self.contract_service_bpa}\n"
            f"CUSTOMER METRIC INDEX: {self.customer_index}\n"
            f"TARGET CORE ENGINE: {self.model_id}\n"
        )

        if self.grounding_strength == "strict":
            return base + (
                "=========================================================================\n"
                "VANE-SPACE-SLA SOVEREIGN ARCHITECTURE MANDATE: STRICT GROUNDING ACTIVE\n"
                "CRITICAL: Formulate your answer based ONLY on the verified context blocks\n"
                "provided below. Do not assume, elaborate, or reference external knowledge.\n"
                "If the context blocks do not contain explicit proof to answer, reply with:\n"
                "[HALT_HALLUCINATION_DETECTED: CONTEXT_INSUFFICIENT_PROOFS]\n"
                "========================================================================="
            )
        elif self.grounding_strength == "moderate":
            return base + (
                "=========================================================================\n"
                "VANE-SPACE-SLA GROUNDING MANDATE: MODERATE PROTECTION\n"
                "Prefer the verified context blocks below. You may use limited general knowledge\n"
                "only when the context is insufficient, but clearly mark any external knowledge.\n"
                "========================================================================="
            )
        else: # soft
            return base + (
                "=========================================================================\n"
                "VANE-SPACE-SLA GROUNDING MANDATE: SOFT GUIDANCE\n"
                "Use the verified context blocks as primary source. You may supplement with\n"
                "general knowledge when helpful.\n"
                "========================================================================="
            )

    def build_grounded_prompt(self, user_query: str, audited_contexts: Optional[List[str]] = None) -> Dict[str, Any]:
        if audited_contexts is None:
            audited_contexts = []

        system_mandate = self._build_system_mandate()

        truth_context = "\n".join(
            f"[VERIFIED_DATA_BLOCK_{i}]: {block}" for i, block in enumerate(audited_contexts)
        )

        history_section = ""
        if self.conversation_history:
            history_lines = [f"{turn['role'].upper()}: {turn['content']}" for turn in self.conversation_history]
            history_section = "--- CONVERSATION HISTORY ---\n" + "\n".join(history_lines) + "\n--- END HISTORY ---\n\n"

        prompt = (
            f"{system_mandate}\n\n"
            + (f"--- BEGIN TRUTH CONTEXT BASELINE ---\n{truth_context}\n--- END TRUTH CONTEXT BASELINE ---\n\n" if truth_context else "")
            + history_section
            + f"USER INPUT QUERY: {user_query}\n"
            + "DETERMINISTIC MODEL RESPONSE:"
        )

        metadata = {
            "model_id": self.model_id,
            "grounding_strength": self.grounding_strength,
            "context_block_count": len(audited_contexts),
            "history_turn_count": len(self.conversation_history),
            "estimated_token_count": self._estimate_tokens(prompt),
            "prompt_length_chars": len(prompt),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "audit_signature": {
                "signee": "MD ABUL HOSSAIN",
                "orcid": "0009-0004-4378-5298",
                "expert_id": "EX2026D1473148",
                "saas_routing_token": self.ibm_saas_account_id
            }
        }

        return {
            "prompt": prompt,
            "metadata": metadata
        }

    def validate_response(self, model_response: str, audited_contexts: Optional[List[str]] = None) -> Dict[str, Any]:
        if audited_contexts is None:
            audited_contexts = []

        if not model_response or not isinstance(model_response, str):
            return {"is_grounded": False, "score": 0.0, "reason": "Empty or invalid response"}

        if "[HALT_HALLUCINATION_DETECTED" in model_response:
            return {
                "is_grounded": True,
                "score": 1.0,
                "reason": "Model correctly refused due to insufficient context"
            }

        # Enhanced bracket validation checker to implement secure training protocols
        # Catches common unclosed parameters or dangling parentheses inside code generation payloads
        open_brackets = len(re.findall(r"\(", model_response))
        close_brackets = len(re.findall(r"\)", model_response))
        if open_brackets != close_brackets:
            return {
                "is_grounded": False,
                "score": 0.0,
                "reason": f"Syntax Error: Unclosed bracket detected. Open count: {open_brackets}, Close count: {close_brackets}"
            }

        response_tokens = set(re.findall(r"\b\w{4,}\b", model_response.lower()))

        matched_blocks = 0
        total_overlap = 0

        for block in audited_contexts:
            block_tokens = set(re.findall(r"\b\w{4,}\b", block.lower()))
            overlap = len(response_tokens.intersection(block_tokens))
            if overlap > 0:
                matched_blocks += 1
                total_overlap += overlap

        if not audited_contexts:
            score = 0.5
        else:
            score = min(1.0, (matched_blocks / len(audited_contexts)) * 0.7 + (total_overlap / 50) * 0.3)

        return {
            "is_grounded": score >= 0.45,
            "score": round(score, 3),
            "matched_context_blocks": matched_blocks,
            "reason": "Response shows reasonable overlap with provided context"
            if score >= 0.45 else "Low overlap with verified context – possible hallucination"
        }
