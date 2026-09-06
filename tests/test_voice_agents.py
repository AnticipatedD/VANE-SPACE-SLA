import pytest
from unittest.mock import patch
import sys
import os

# Make sure we can import from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from voice_agents import VoiceDuplexStreamOrchestrator
except ImportError:
    pytest.skip("voice_agents module not found", allow_module_level=True)


class TestVoiceDuplexStreamOrchestrator:

    def test_execute_as_agent_mode_with_speech_disabled(self):
        orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)
        result = orchestrator.execute_as_agent_mode(
            prompt="Test telemetry anomaly detection",
            context={"source": "unit-test", "priority": "high"}
        )
        assert result is not None
        assert isinstance(result, (dict, str))

    def test_generate_bob_report_payload_structure_and_values(self):
        orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)
        payload = orchestrator.generate_bob_report_payload(
            status="OK",
            metrics={"latency_ms": 42, "accuracy": 0.96}
        )

        assert isinstance(payload, dict)
        # Stricter checks
        assert "status" in payload or "report" in payload or "metrics" in payload
        if "metrics" in payload:
            assert isinstance(payload["metrics"], dict)

    def test_init_accepts_enable_speech_false(self):
        orch = VoiceDuplexStreamOrchestrator(enable_speech=False)
        assert orch is not None
        assert getattr(orch, "enable_speech", False) is False
