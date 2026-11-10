#!/usr/bin/env python3
"""Test Suite for VANE-SPACE-SLA - Voice Agents Module."""

from voice_orchestrator import VoiceOrchestratorNode


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
