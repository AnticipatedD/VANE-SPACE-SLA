#!/usr/bin/env python3
"""
VANE-SPACE-SLA — Strict Prompt Grounding Builder (Backward Compatibility)
Author: MD ABUL HOSSAIN
Description: Wrapper module that re-exports from vane_space.prompt_builder
              for backward compatibility with existing code.
"""

from vane_space.prompt_builder import StrictPromptBuilder

__all__ = ["StrictPromptBuilder"]
