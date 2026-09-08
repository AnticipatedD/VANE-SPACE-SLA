#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Custom Exception Types
Author: MD ABUL HOSSAIN
Description: Centralized error handling with typed exception classes
"""


class VaneSpaceException(Exception):
    """Base exception for all VANE-SPACE-SLA errors."""
    pass


class ConfigError(VaneSpaceException):
    """Raised when configuration validation fails."""
    pass


class TelemetryValidationError(VaneSpaceException):
    """Raised when multi-gate telemetry validation detects drift or failure."""
    pass


class VoiceOrchestrationError(VaneSpaceException):
    """Raised when voice duplex stream orchestration encounters an error."""
    pass


class PromptGroundingError(VaneSpaceException):
    """Raised when prompt grounding validation fails."""
    pass
