#!/usr/bin/env python3
"""Test Suite for VANE-SPACE-SLA - Voice Agents Module."""

from voice_orchestrator import VoiceOrchestratorNode

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "extensions-core"))

import voice_agents
from voice_agents import VoiceDuplexStreamOrchestrator


def test_voice_orchestrator_node_allocation() -> None:
    """Asserts that stateful allocations cleanly handle variable load constraints."""
    node = VoiceOrchestratorNode(node_id="test-node-01", capacity=2)

    res1 = node.allocate_channel("session-alpha", {"priority": "high"})
    res2 = node.allocate_channel("session-beta", {"priority": "low"})
    res3 = node.allocate_channel("session-gamma", {})

    assert res1 is True
    assert res2 is True
    assert res3 is False
    assert len(node.active_channels) == 2


def test_voice_duplex_stream_supports_deterministic_local_randomness(monkeypatch) -> None:
    monkeypatch.setattr(voice_agents.time, "sleep", lambda _seconds: None)
    random.seed(1234)
    expected_next_random = random.random()
    random.seed(1234)

    orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)
    first = orchestrator.execute_as_agent_mode(frame_count=2, seed=17)
    second = orchestrator.execute_as_agent_mode(frame_count=2, seed=17)

    assert first == second
    assert len(first) == 2
    assert random.random() == expected_next_random


def test_voice_duplex_stream_rejects_negative_frame_count() -> None:
    orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)

    try:
        orchestrator.execute_as_agent_mode(frame_count=-1)
    except ValueError as exc:
        assert "frame_count" in str(exc)
    else:
        raise AssertionError("negative frame_count must be rejected")


def test_voice_duplex_stream_report_accepts_metrics_alias() -> None:
    orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)
    report = json.loads(
        orchestrator.generate_bob_report_payload(metrics={"frames": 2}, status="PASS")
    )

    assert report["execution_summary"] == {"frames": 2}
    assert report["verification_status"] == "PASS"


def test_voice_duplex_stream_runs_without_speech(monkeypatch) -> None:
    monkeypatch.setattr(voice_agents.time, "sleep", lambda _seconds: None)
    orchestrator = VoiceDuplexStreamOrchestrator(enable_speech=False)

    orchestrator.speak("text-only fallback")

    assert orchestrator.enable_speech is False
    assert orchestrator.engine is None
