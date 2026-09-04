# tests/test_voice_agents.py
"""
Tests for VoiceDuplexStreamOrchestrator.
All speech/audio is disabled so the suite runs on any machine without hardware.
"""

import pytest
from unittest.mock import patch, MagicMock

# Adjust the import path if your file is named differently or lives in a package
try:
    from voice_agents import VoiceDuplexStreamOrchestrator
except ImportError:
    # Fallback if the module is still named differently
    pytest.skip("voice_agents module not found", allow_module_level=True)


class TestVoiceDuplexStreamOrchestrator:

    def test_execute_as_agent_mode_disabled_speech(self):
        """execute_as_agent_mode should work cleanly when speech is disabled."""
        orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)
        result = orchestrator.execute_as_agent_mode(
            prompt="Test telemetry anomaly",
            context={"source": "unit-test"}
        )
        assert result is not None
        assert isinstance(result, (dict, str))

    def test_generate_bob_report_payload(self):
        """generate_bob_report_payload must return a valid dict structure."""
        orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)
        payload = orchestrator.generate_bob_report_payload(
            status="OK",
            metrics={"latency_ms": 42, "accuracy": 0.96}
        )
        assert isinstance(payload, dict)
        assert "status" in payload or "report" in payload or len(payload) > 0

    def test_init_with_speech_disabled(self):
        """Constructor must accept enable_speech=False without error."""
        orch = VoiceDuplexStreamOrchestrator(enable_speech=False)
        assert orch is not None
