#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Main Package
Author: MD ABUL HOSSAIN
Description: Deterministic Multi-Gate Telemetry Validation & Strict Prompt Grounding Toolkit
"""

from vane_space.errors import (
    VaneSpaceException,
    ConfigError,
    TelemetryValidationError,
    VoiceOrchestrationError,
    PromptGroundingError,
)

from vane_space.logging_config import configure_logging, root_logger

from vane_space.telemetry import (
    verify_granite_syntax_gate,
    run_multi_gate_telemetry_check,
)

from vane_space.prompt_builder import StrictPromptBuilder

from vane_space.voice_agents import VoiceDuplexStreamOrchestrator

__version__ = "1.1.0"
__author__ = "MD ABUL HOSSAIN"
__license__ = "MIT"

__all__ = [
    # Exceptions
    "VaneSpaceException",
    "ConfigError",
    "TelemetryValidationError",
    "VoiceOrchestrationError",
    "PromptGroundingError",
    # Logging
    "configure_logging",
    "root_logger",
    # Telemetry
    "verify_granite_syntax_gate",
    "run_multi_gate_telemetry_check",
    # Prompt Builder
    "StrictPromptBuilder",
    # Voice Orchestration
    "VoiceDuplexStreamOrchestrator",
]
